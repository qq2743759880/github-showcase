"""Export release gate: vendored secret scanning (in-process), privacy/license policy,
and Showcase quality gates (asset consumption, reader surface, comprehension, self-dogfood)."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote,urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence

ROOT=Path(__file__).resolve().parents[1]

ASSET_EXTS={'.png','.jpg','.jpeg','.svg','.mmd','.gif','.webp'}
DOC_EXTS={'.md'}
SKIP_PARTS={'.git','.mimosa','.cache','node_modules','.venv','__pycache__','.pytest_cache','usage'}
FIRST_SCREEN_BANNED=[re.compile(r'[0-9a-f]{32,64}'),re.compile(r'Generic V0\.'),re.compile(r'puppeteer',re.I),re.compile(r'node_modules'),re.compile(r'\bfixture\b',re.I),re.compile(r'vendor entity',re.I),re.compile(r'\baudit\b',re.I),re.compile(r'run-\d{3}'),re.compile(r'\.mimosa')]
LINK_RE_MD=re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_RE_IMG=re.compile(r'<img[^>]+src="([^"]+)"')

def _load_scanner():
    spec=importlib.util.spec_from_file_location('secret_scanner_engine',ROOT/'vendor/secret-scanner/skills/secret-scanner/engine.py')
    module=importlib.util.module_from_spec(spec)
    sys.modules['secret_scanner_engine']=module
    spec.loader.exec_module(module)
    return module

def _tree_paths(export,allow_git_dirs=False):
    for path in export.rglob('*'):
        if path.is_symlink() or not path.is_file():
            continue
        rel=path.relative_to(export)
        special={p for p in rel.parts if p in SKIP_PARTS}
        if special:
            continue
        yield path,rel

def verified_fixtures(findings,texts,policy,engine):
    """Only exact reviewed synthetic basic-auth findings, never directory ignores."""
    approvals=policy.get('secret_fixture_exemptions',[])
    if not isinstance(approvals,list):return [],list(findings),['fixture exemptions must be a list']
    required={'path','rule_id','fixture_sha256','line_sha256','line','column','classification','purpose'}
    accepted=[];blocking=[];errors=[];used=set()
    from hashlib import sha256
    for item in approvals:
        if not isinstance(item,dict) or set(item)!=required:
            errors.append('invalid fixture exemption schema');continue
        name=item['path']
        if not isinstance(name,str) or '\\' in name or ':' in name or name.startswith('/') or '..' in Path(name).parts or Path(name).as_posix()!=name or not (name.startswith(('tests/','test/','fixtures/security/')) and Path(name).suffix in {'.py','.js','.mjs','.ts'}) or item['classification']!='security-test-fixture' or item['rule_id']!='basic-auth-url' or not isinstance(item['purpose'],str) or not item['purpose'].strip() or type(item['line']) is not int or type(item['column']) is not int or item['line']<1 or item['column']<1 or any(not isinstance(item[k],str) or not re.fullmatch('[a-f0-9]{64}',item[k]) for k in ('fixture_sha256','line_sha256')):
            errors.append('unsupported or invalid fixture exemption');continue
    rule=next(r for r in engine.RULES if r.id=='basic-auth-url')
    for finding in findings:
        approved=None
        if finding.rule_id=='basic-auth-url' and finding.path in texts:
            lines=texts[finding.path].splitlines()
            # Scanner chunks long lines. Never infer approval locations across
            # that transformation; long-line findings stay blocked.
            if all(len(s)<=3500 for s in lines) and 0<finding.line<=len(lines):
                line=lines[finding.line-1]
                for match in rule.pattern.finditer(line):
                    if match.start(1)+1!=finding.column:continue
                    value=match.group(1);url=urlparse(value.rstrip("\"')],;}"))
                    synthetic=url.scheme=='https' and url.username in {'user','test_key_user'} and url.password in {'secret','pass','test_key_password'} and url.hostname in {'example.com','example.invalid','fixture.trycloudflare.com','example.ngrok.dev'}
                    if not synthetic:continue
                    for i,item in enumerate(approvals):
                        if not isinstance(item,dict) or set(item)!=required:continue
                        if item['path']==finding.path and item['rule_id']==finding.rule_id and item['classification']=='security-test-fixture' and isinstance(item['purpose'],str) and item['purpose'].strip() and item['line']==finding.line and item['column']==finding.column and item['line_sha256']==sha256(line.encode()).hexdigest() and item['fixture_sha256']==sha256(value.encode()).hexdigest() and finding.path.startswith(('tests/','test/','fixtures/security/')):
                            approved=i;break
        if approved is None:blocking.append(finding)
        else:accepted.append(finding);used.add(approved)
    for i in range(len(approvals)):
        if i not in used:errors.append('fixture exemption is stale/unmatched or disallowed')
    return accepted,blocking,errors

def check(export,policy,allow_git_dirs=False):
    errors=[]
    if policy.get('license_status') != 'PASS':
        errors.append('license review not PASS')
    if policy.get('authorization') not in {'APPROVED','NOT_AUTHORIZED'}:
        errors.append('authorization must be explicit')
    literals=policy.get('private_literals')
    if not isinstance(literals,list) or not all(isinstance(s,str) and s for s in literals):
        errors.append('privacy review requires explicit private_literals (empty list allowed)')
        literals=[]
    for path in export.rglob('*'):
        if path.is_symlink():
            errors.append('linked export path')
            continue
        if not path.is_file():
            continue
        relative=path.relative_to(export)
        special={p for p in relative.parts if p in SKIP_PARTS}
        if allow_git_dirs and special=={'.git'}:
            continue  # Inspect working export without scanning private Git metadata.
        if special:
            errors.append('regenerated/private directory in export: '+relative.as_posix())
            continue
        value=path.read_bytes()
        if any(literal.encode('utf-8') in value for literal in literals):
            errors.append('private literal in export: '+relative.as_posix())
    engine=_load_scanner()
    findings=[];texts={}
    # The upstream directory walker skips vendor/. A release tree must scan all
    # approved text files, including third-party source and long/minified lines.
    for path,relative in _tree_paths(export,allow_git_dirs):
        if path.suffix.lower() in engine.BINARY_EXT:
            continue
        value=path.read_bytes()
        if b'\0' in value[:8192]:
            continue
        text=value.decode('utf-8',errors='replace')
        texts[relative.as_posix()]=text
        lines=[]
        for line in text.splitlines():
            if len(line)<=3500:
                lines.append(line)
            else:
                lines.extend(line[i:i+3500] for i in range(0,len(line),3000))
        findings.extend(engine.scan_text('\n'.join(lines),relative.as_posix(),3.5,True))
    secret_exit=1 if findings else 0
    exempted,blocking,fixture_errors=verified_fixtures(findings,texts,policy,engine)
    errors.extend(fixture_errors)
    if blocking:
        errors.append('vendored secret scanner rejected export (%d blocking findings)'%len(blocking))
    return {'F09':'BLOCK' if errors else 'PASS','F10':'STOP' if errors else 'LOCAL_PACKAGE_ALLOWED','remote_publish':'STOP' if errors or policy.get('authorization')!='APPROVED' else 'AUTHORIZED_PENDING_REMOTE_READBACK','errors':sorted(set(errors)),'secret_scanner_exit':secret_exit,'secret_findings':len(findings),'raw_findings':[f.to_dict() for f in findings],'exempted_fixture_findings':[f.to_dict() for f in exempted],'blocking_findings':[f.to_dict() for f in blocking],'raw_findings_count':len(findings),'exempted_fixture_findings_count':len(exempted),'blocking_findings_count':len(blocking)}

def _scan_tree(export,allow_git_dirs=False):
    assets=[];docs=[]
    for path,rel in _tree_paths(export,allow_git_dirs):
        if path.suffix.lower() in ASSET_EXTS:
            assets.append(rel)
        elif path.suffix.lower() in DOC_EXTS and path.stat().st_size<=2_000_000:
            docs.append((rel,path.read_text(encoding='utf-8',errors='replace')))
    return assets,docs

def _visible_links(text):
    # Literal templates/code examples are not rendered document links.
    text=re.sub(r'```.*?```|<!--.*?-->','',text,flags=re.S)
    return list(LINK_RE_MD.finditer(text))+list(LINK_RE_IMG.finditer(text))

def _reader_docs(export,allow_git_dirs=False):
    _,docs=_scan_tree(export,allow_git_dirs)
    indexed={rel.as_posix():(rel,text) for rel,text in docs}
    pending=['README.md']; visited=set(); result=[]
    while pending:
        name=pending.pop()
        if name in visited or name not in indexed:
            continue
        visited.add(name)
        rel,text=indexed[name]; result.append((rel,text))
        for match in _visible_links(text):
            target=match.group(1).split('#')[0].split('?')[0]
            if target.startswith(('http://','https://','mailto:')):
                continue
            resolved=os.path.normpath(os.path.join(str(rel.parent),target)).replace('\\','/')
            if resolved in indexed:
                pending.append(resolved)
    return result

def check_orphan_assets(export,allow_git_dirs=False):
    """Asset Consumption Gate：树内未被任何 md 引用的视觉资产 = ORPHAN_ASSET_FAIL。"""
    assets,_=_scan_tree(export,allow_git_dirs)
    docs=_reader_docs(export,allow_git_dirs)
    referenced=set()
    for rel,text in docs:
        for match in _visible_links(text):
            target=match.group(1).split('#')[0].split('?')[0]
            if target.startswith(('http://','https://','mailto:')):
                continue
            referenced.add(os.path.normpath(os.path.join(str(rel.parent),target)).replace('\\','/'))
    orphaned=[]
    for rel in assets:
        if rel.as_posix() not in referenced:
            orphaned.append(rel.as_posix())
    return orphaned

def check_broken_links(export,allow_git_dirs=False):
    docs=_reader_docs(export,allow_git_dirs)
    existing={rel.as_posix() for path,rel in _tree_paths(export,allow_git_dirs)}
    existing.update(p.relative_to(export).as_posix() for p in export.rglob('*') if p.is_dir() and not any(part in SKIP_PARTS for part in p.relative_to(export).parts))
    broken=[]
    for rel,text in docs:
        base=rel.parent
        for match in _visible_links(text):
            target=match.group(1).split('#')[0].split('?')[0]
            if not target or target.startswith(('http://','https://','mailto:')):
                continue
            if not (re.search(r'\.[A-Za-z0-9]{1,6}$',target) or target.endswith('/')):
                continue  # 括号注释等非路径形态（如 「(默认，仅此一值)」）不算链接
            resolved=os.path.normpath(os.path.join(str(base),target)).replace('\\','/')
            if resolved not in existing:
                broken.append(rel.as_posix()+' -> '+target)
    return sorted(set(broken))

def check_reader_surface(export,allow_git_dirs=False):
    """User Surface / Maintainer Surface 分层：README 第一屏禁止维护者信息。"""
    readme=export/'README.md'
    if not readme.is_file():
        return ['READER_SURFACE_FAIL: README.md missing']
    text=readme.read_text(encoding='utf-8',errors='replace')
    first_screen=text.split('\n## ')[0]
    return ['READER_SURFACE_FAIL: first screen contains maintainer info: '+p.pattern for p in FIRST_SCREEN_BANNED if p.search(first_screen)]

def check_comprehension_receipt(receipt,export=None):
    """Reader Comprehension Gate：独立 Fresh Reviewer 五题收据。"""
    if not receipt or not Path(receipt).is_file():
        return ['READER_COMPREHENSION_FAIL: receipt missing']
    try:
        evidence.comprehension(receipt,export)
    except (OSError,ValueError,TypeError,KeyError) as exc:
        return ['READER_COMPREHENSION_FAIL: '+str(exc)]
    return []

def check_self_dogfood_receipt(receipt,export=None):
    if not receipt or not Path(receipt).is_file():
        return ['SELF_DOGFOOD_MISSING: receipt file not found']
    try:
        evidence.self_dogfood(receipt,export,ROOT)
    except (OSError,ValueError,TypeError,KeyError) as exc:
        return ['SELF_DOGFOOD_MISSING: '+str(exc)]
    return []

def check_routed_assets(export,allow_git_dirs=False,policy=None):
    """被路由的 visual phase 必须产出约定资产（hero/architecture/workflow/capability）。"""
    routed=(policy or {}).get('routed_assets') or {}
    missing=[]
    for phase,rel in sorted(routed.items()):
        if not (export/rel).is_file():
            missing.append(phase+' missing '+rel)
    return missing

def check_archify_deliveries(export,policy):
    """Require native full delivery and bind both public IR and HTML bytes."""
    if not {'F03','F04'}.intersection(policy.get('routed_assets',{})):
        return []
    deliveries=policy.get('archify_deliveries',[])
    if not deliveries:
        return ['routed diagram requires Archify native finalize evidence']
    errors=[]
    decomposition=policy.get('archify_decomposition')
    if decomposition:
        try:
            spec=importlib.util.spec_from_file_location('coverage_contract',ROOT/'scripts/archify-routing.py');archify=importlib.util.module_from_spec(spec);spec.loader.exec_module(archify)
            original=json.loads(Path(decomposition['original_source']).read_text(encoding='utf-8'))
            if archify.native_attempts(decomposition['single_view_attempts'],original,decomposition['semantic_review'])!='SEMANTIC_DECOMPOSITION':raise ValueError('single view passed; do not split')
            ledger=json.loads(Path(decomposition['coverage_ledger']).read_text(encoding='utf-8'))
            views={}
            for view in decomposition['views']:
                name=view['name'];path=(export/archify.relative(view['source'])).resolve()
                if name in views or not path.is_relative_to(export.resolve()):raise ValueError('duplicate/unsafe required view')
                views[name]=json.loads(path.read_text(encoding='utf-8'))
                preview=(export/archify.relative(view['preview'])).resolve()
                if not preview.is_relative_to(export.resolve()) or not preview.is_file():raise ValueError('required canonical preview missing')
                if not any(d.get('source')==view['source'] and d.get('html')==view['html'] for d in deliveries):raise ValueError('required view lacks native delivery')
            expected=archify.coverage(original,views)
            if any(ledger.get(k)!=v for k,v in expected.items()):raise ValueError('decomposition coverage ledger changed/incomplete')
            errors.extend(archify.consumption_errors(export,decomposition['views']))
        except (OSError,ValueError,KeyError,TypeError) as exc:errors.append('semantic decomposition: '+str(exc))
    for item in deliveries:
        try:
            receipt=json.loads(Path(item['finalize_summary']).read_text(encoding='utf-8'))
            if receipt.get('command')!='finalize' or receipt.get('status')!='pass' or receipt.get('ok') is not True or receipt.get('quality')!='showcase' or receipt.get('diagnostics'):
                raise ValueError('native showcase finalize did not pass')
            if any(receipt.get('gates',{}).get(k)!='pass' for k in ['validate','deliver','check','browser-check']):
                raise ValueError('native finalize gate incomplete')
            for public,identity in [('source','specification'),('html','artifact')]:
                path=(export/item[public]).resolve()
                binding=receipt[identity]
                original=Path(binding['path'])
                if not path.is_relative_to(export.resolve()) or not path.is_file() or not original.is_file():
                    raise ValueError('native/public diagram file absent or outside export')
                for candidate in [path,original]:
                    if candidate.stat().st_size!=binding['bytes'] or evidence.sha256(candidate)!=binding['sha256']:
                        raise ValueError('native/public diagram bytes changed')
        except (OSError,ValueError,KeyError,TypeError) as exc:
            errors.append(str(exc))
    return errors

def workflow_write_permissions(text):
    """Parse actual root/job permission scopes; never infer Actions defaults."""
    import yaml  # Existing optional YAML dependency; missing parser blocks publication.
    class UniqueLoader(yaml.BaseLoader):
        def construct_mapping(self,node,deep=False):
            keys=[self.construct_object(k,deep=deep) for k,_ in node.value]
            if len(set(keys))!=len(keys):raise ValueError('duplicate YAML mapping keys')
            return super().construct_mapping(node,deep=deep)
    workflow=yaml.load(text,Loader=UniqueLoader)
    if not isinstance(workflow,dict) or 'permissions' not in workflow:raise ValueError('explicit workflow permissions required')
    jobs=workflow.get('jobs',{})
    if not isinstance(jobs,dict) or any(not isinstance(job,dict) for job in jobs.values()):raise ValueError('invalid workflow jobs')
    scopes=[workflow['permissions']]+[j['permissions'] for j in jobs.values() if 'permissions' in j]
    writes=False
    for scope in scopes:
        if scope in ('read-all','write-all'):
            writes=writes or scope=='write-all';continue
        if not isinstance(scope,dict) or any(not isinstance(k,str) or v not in {'read','write','none'} for k,v in scope.items()):raise ValueError('static explicit permission map required')
        writes=writes or 'write' in scope.values()
    return writes

def check_publication(export,policy,paths):
    purposes=policy.get('publication_purposes',{})
    if not isinstance(purposes,dict) or set(purposes)!=set(paths) or any(not isinstance(v,str) or not v.strip() for v in purposes.values()):return ['every Publication file requires one explicit publication purpose']
    errors=[]
    private_parts={'evidence','receipts','trace','logs','node_modules','visual-source','__pycache__'}
    for name in paths:
        path=export/name
        if private_parts.intersection(p.lower() for p in Path(name).parts) or path.suffix.lower() in {'.log','.receipt'}:
            errors.append('private evidence/log in Publication: '+name);continue
        try:
            text=path.read_text(encoding='utf-8')
            if re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]|/(?:Users|home)/[^/\s]+/',text):raise ValueError('developer-machine absolute path')
            for url in re.findall(r'https://(?:raw\.githubusercontent\.com/[^\s\"\'<>{}]+|github\.com/[^\s\"\'<>{}]+/releases/download/[^\s\"\'<>{}]+)',text):
                channels=policy.get('release_channels') or {}
                identities=[policy.get('release_artifact')]+[channels.get(k) for k in ['stable','preview']]
                if not any(isinstance(item,dict) and not check_immutable_artifact({'release_artifact':{**item,'url':url}}) for item in identities):raise ValueError('publication artifact URL requires matching immutable release_artifact or release_channels identity')
            if Path(name).parts[:2]==('.github','workflows'):
                if path.suffix.lower() not in {'.yml','.yaml'}:raise ValueError('Actions workflow must be YAML')
                if workflow_write_permissions(text) and policy.get('publication_authorization')!='APPROVED':raise ValueError('remote write permissions require explicit publication_authorization APPROVED')
            elif path.suffix.lower()=='.json':
                data=json.loads(text)
                if not isinstance(data,dict):raise ValueError('publication metadata must be an object')
                if any(k in data for k in ['receipt','trace_path','export_digest','check_receipt','stdout','stderr','passed','tool_sha256','batch']) or data.get('kind') in {'skill-fidelity','reader-comprehension','fresh-clone','self-dogfood','minimal-runtime'}:raise ValueError('private verification receipt')
                if {'release_tag','artifact_url'}.intersection(data):
                    artifact=policy.get('release_artifact')
                    if not artifact or any(key in data and data[key]!=artifact.get(field) for key,field in [('release_tag','version'),('artifact_url','url')]):raise ValueError('actual publication tag/URL must match release_artifact')
                for contract in [data,policy]:
                    failures=check_immutable_artifact(contract)+check_release_channels(contract)
                    if failures:raise ValueError('; '.join(failures))
        except (OSError,UnicodeError,ValueError,TypeError,KeyError,ImportError) as exc:
            errors.append('Publication '+name+': '+str(exc))
        except Exception as exc:
            # YAML parser errors are rejected without emitting the file's secret contents.
            errors.append('Publication '+name+': invalid YAML ('+type(exc).__name__+')')
    return errors

def check_distribution_surface(export,policy):
    if policy.get('project_form')!='agent-skill':return []
    surface=policy.get('distribution_surface',{})
    if not isinstance(surface,dict):return ['distribution_surface must be an object']
    fields=['execution','redistribution','runtime','showcase','publication','evidence']
    for field in fields:
        values=surface.get(field,[])
        if not isinstance(values,list) or any(not isinstance(p,str) or not p or '\\' in p or ':' in p or p.startswith('/') or '..' in Path(p).parts or Path(p).as_posix()!=p for p in values):return ['surface paths must be canonical relative file lists: '+field]
        if len(set(values))!=len(values):return ['duplicate paths in '+field]
    runtime=surface.get('runtime',[]);showcase=surface.get('showcase',[]);publication=surface.get('publication',[])
    execution=surface.get('execution',[]);redistribution=surface.get('redistribution',[])
    if not execution or 'SKILL.md' not in execution or not set(execution).issubset(redistribution) or set(redistribution)!=set(runtime):return ['declare execution closure separately; redistribution must include execution and equal packaged runtime']
    if not runtime or 'SKILL.md' not in runtime or not showcase or surface.get('evidence',[]):return ['explicit runtime/showcase surface required; build evidence must remain private']
    allowed=runtime+showcase+publication
    if len(set(allowed))!=len(allowed):return ['distribution surfaces overlap']
    misplaced=[p for p in runtime+showcase if evidence.publication_path(p)]
    if misplaced:return ['Publication paths cannot be Runtime or user Showcase: '+', '.join(misplaced)]
    actual={r.as_posix() for _,r in _tree_paths(export,True)}
    if actual!=set(allowed):return ['unclassified/missing public files: '+', '.join(sorted(actual.symmetric_difference(allowed)))]
    forbidden={'package-lock.json','yarn.lock','pnpm-lock.yaml'}
    noise=[p for p in showcase if Path(p).name in forbidden or any(part in {'visual-source','trace','receipts','node_modules'} for part in Path(p).parts)]
    errors=['build/repro evidence in Showcase: '+', '.join(noise)] if noise else []
    return errors+check_publication(export,policy,publication)

def check_readme_profile(export,policy):
    profile=policy.get('readme_profile')
    if not profile:return ['Agent Skill README profile missing'] if policy.get('project_form')=='agent-skill' else []
    try:
        text=(export/'README.md').read_text(encoding='utf-8');errors=[]
        if profile.get('workflow_is_product'):
            preview=profile['workflow_preview'];url=profile['interactive_url']
            links=_visible_links(text)
            images=[m.start() for m in links if m.group(1)==preview]
            interactive=[m.start() for m in links if m.group(1)==url]
            boundaries=[text.index(profile[k]) for k in ['install_anchor','task_anchor']]
            if not images or not interactive or max(min(images),min(interactive))>=min(boundaries):errors.append('core workflow preview/interactive entry must precede install and tasks')
        return errors
    except (OSError,KeyError,ValueError,TypeError) as exc:return ['README profile incomplete: '+str(exc)]

def check_immutable_artifact(policy):
    artifact=policy.get('release_artifact')
    if not artifact:return ['versioned runtime artifact identity missing'] if policy.get('runtime_artifact') and policy.get('project_form')=='agent-skill' else []
    try:
        version=artifact['version'];url=urlparse(artifact['url']);parts=[unquote(p) for p in url.path.split('/') if p]
        if url.scheme!='https' or not version or not parts:raise ValueError('versioned HTTPS artifact URL required')
        if url.hostname=='raw.githubusercontent.com' and len(parts)>=4:ref=parts[2]
        elif url.hostname=='github.com' and len(parts)>=6 and parts[2:4]==['releases','download']:ref=parts[4]
        else:raise ValueError('artifact must use a versioned Release asset or repository ref URL')
        if ref in {artifact.get('default_branch','main'),'main','master','HEAD','latest'}:raise ValueError('historical release artifact uses a mutable reference')
        if ref!=version and not re.fullmatch(r'[0-9a-fA-F]{40}',ref):raise ValueError('artifact ref must equal release version or a complete commit')
        return []
    except (KeyError,TypeError,ValueError) as exc:return [str(exc)]

def check_release_channels(policy):
    channels=policy.get('release_channels')
    if channels is None:return []
    try:
        stable=channels['stable'];preview=channels['preview'];errors=[]
        if channels.get('default_install')!='stable':errors.append('preview must not replace default stable installation')
        if preview.get('prerelease') is not True:errors.append('preview must be an explicit prerelease')
        if stable['version']==preview['version']:errors.append('stable and preview must have distinct version identities')
        for item in [stable,preview]:errors.extend(check_immutable_artifact({'release_artifact':item}))
        return errors
    except (KeyError,TypeError,ValueError) as exc:return ['release channel contract invalid: '+str(exc)]

def check_license_integrity(export,policy):
    contract=policy.get('license_identifier')
    if not contract:return ['authoritative license identifier contract missing'] if policy.get('project_form')=='agent-skill' else []
    try:
        identifier=contract['identifier'];source=(export/contract['source']).resolve();errors=[]
        if not identifier or not source.is_relative_to(export.resolve()):raise ValueError('invalid authoritative license source')
        match=re.search(r'^license:\s*[\"\']?([^\r\n\"\']+)',source.read_text(encoding='utf-8'),re.M)
        if not match or match.group(1).strip()!=identifier:raise ValueError('declared license identifier differs from authoritative entry')
        if not contract['documents']:raise ValueError('license-facing documents required')
        for name in contract['documents']:
            path=(export/name).resolve()
            if not path.is_relative_to(export.resolve()):raise ValueError('license document escapes export')
            text=path.read_text(encoding='utf-8');tokens=re.findall(r'(?<!`)`([^`\r\n]+)`(?!`)',text)
            if identifier not in tokens:errors.append('exact license identifier missing or replaced in '+name)
            for field in re.findall(r'^(?:SPDX-License-Identifier|license)\s*[:=]\s*([^\r\n]+)',text,re.M|re.I):
                if field.strip().strip('`\"\'')!=identifier:errors.append('license declaration differs in '+name)
        return errors
    except (OSError,KeyError,TypeError,ValueError) as exc:return ['license identifier integrity: '+str(exc)]

def check_minimal_runtime(export,policy):
    if policy.get('project_form')!='agent-skill':return []
    try:
        receipt=json.loads(Path(policy['minimal_runtime_receipt']).read_text(encoding='utf-8'))
        if policy.get('source_distribution') and receipt.get('source_distribution',{}).get('path')!=policy['source_distribution']:return ['original distribution path/byte authority missing from minimal runtime receipt']
        spec=importlib.util.spec_from_file_location('runtime_package',ROOT/'scripts/runtime-package.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        if set(policy['distribution_surface']['runtime'])!={r['path'] for r in receipt['files']}:return ['runtime surface differs from package']
        artifact=policy.get('runtime_artifact')
        if artifact:
            module.safe(artifact)
            path=export/artifact
            if not path.resolve().is_relative_to(export.resolve()) or path.is_symlink() or path.read_bytes()!=Path(receipt['package']).read_bytes():return ['published runtime artifact differs from verified package']
        return module.verify(receipt,export)
    except (OSError,ValueError,KeyError,TypeError) as exc:return ['minimal runtime evidence missing/invalid: '+str(exc)]

def check_public_copy(export,policy):
    spec=importlib.util.spec_from_file_location('public_copy',ROOT/'scripts/public-copy.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.check(export,policy)

def run_showcase_gate(export,policy,comprehension_receipt=None,self_dogfood_receipt=None,require_self_dogfood=False,allow_git_dirs=False,fresh_clone_receipt=None,fidelity_receipt=None,expected_commit=None):
    result=check(export,policy,allow_git_dirs=allow_git_dirs)
    gates=[]
    copy_errors=check_public_copy(export,policy)
    result['public_copy']={'status':'PUBLIC_COPY_FAIL' if copy_errors else 'PASS','errors':copy_errors}
    if copy_errors:gates.append('PUBLIC_COPY_FAIL')
    for name,failures in [('IMMUTABLE_ARTIFACT_FAIL',check_immutable_artifact(policy)),('RELEASE_CHANNEL_FAIL',check_release_channels(policy)),('LICENSE_IDENTIFIER_FAIL',check_license_integrity(export,policy))]:
        if failures:gates.append(name);result[name.lower()]=failures
    for name,checker in [('DISTRIBUTION_SURFACE_FAIL',check_distribution_surface),('README_PROFILE_FAIL',check_readme_profile),('MINIMAL_RUNTIME_FAIL',check_minimal_runtime)]:
        failures=checker(export,policy)
        if failures:
            gates.append(name);result[name.lower()]=failures
    if policy.get('project_kind') not in {'code','mixed','docs','design','knowledge-base'}:
        gates.append('PROJECT_KIND_MISSING')
    orphaned=check_orphan_assets(export,allow_git_dirs=allow_git_dirs)
    if orphaned:
        gates.append('ORPHAN_ASSET_FAIL')
        result['orphan_assets']=orphaned
    broken=check_broken_links(export,allow_git_dirs=allow_git_dirs)
    if broken:
        gates.append('BROKEN_LINKS_FAIL')
        result['broken_links']=broken
    result['reader_surface']=check_reader_surface(export,allow_git_dirs=allow_git_dirs)
    if result['reader_surface']:
        gates.append('READER_SURFACE_FAIL')
    cr=check_comprehension_receipt(comprehension_receipt,export)
    if cr:
        gates.append('READER_COMPREHENSION_FAIL')
        result['reader_comprehension']=cr
    if require_self_dogfood:
        sd=check_self_dogfood_receipt(self_dogfood_receipt,export)
        if sd:
            gates.append('SELF_DOGFOOD_MISSING')
            result['self_dogfood']=sd
    missing=check_routed_assets(export,allow_git_dirs=allow_git_dirs,policy=policy)
    if missing:
        gates.append('ROUTED_ASSET_MISSING')
        result['routed_asset_missing']=missing
    diagram_errors=check_archify_deliveries(export,policy)
    if diagram_errors:
        gates.append('ARCHIFY_DELIVERY_FAIL')
        result['archify_delivery_errors']=diagram_errors
    if policy.get('project_kind') in {'code','mixed'}:
        try:
            evidence.fresh_clone(fresh_clone_receipt,export,policy.get('source_release',{}),expected_commit)
        except (OSError,ValueError,TypeError,KeyError,evidence.subprocess.CalledProcessError) as exc:
            gates.append('FRESH_CLONE_FAIL')
            result['fresh_clone_error']=str(exc)
    try:
        receipt=evidence.read_receipt(fidelity_receipt,'skill-fidelity')
        if receipt.get('export_digest') != evidence.tree_digest(export):
            raise ValueError('fidelity receipt is stale')
        base=Path(fidelity_receipt).resolve().parent
        trace=(base/receipt.get('trace_path','')).resolve()
        if not receipt.get('trace_path') or not trace.is_relative_to(base) or not trace.is_file():
            raise ValueError('fidelity trace missing')
        spec=importlib.util.spec_from_file_location('release_fidelity',ROOT/'scripts/skill-fidelity.py')
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        checked=module.validate(trace,export)
        if checked['status']!='PASS' or checked['trace_sha256']!=receipt.get('trace_sha256') or checked['scores']!=receipt.get('scores'):
            raise ValueError('fidelity workflow evidence changed or failed')
        required={'readme-skill'}
        if 'F03' in policy.get('routed_assets',{}): required.add('c4-architecture')
        if 'F06' in policy.get('routed_assets',{}): required.add('snap-x')
        if {'F03','F04'}.intersection(policy.get('routed_assets',{})): required.add('archify')
        if not required.issubset(checked['scores']):
            raise ValueError('routed producer workflow missing from fidelity trace')
    except (OSError,ValueError,TypeError,KeyError) as exc:
        gates.append('SKILL_FIDELITY_FAIL')
        result['fidelity_error']=str(exc)
    result['gates']=sorted(set(gates))
    result['READY_FOR_APPROVAL']=not gates and result['F09']=='PASS'
    result['remote_publish']='STOP' if not result['READY_FOR_APPROVAL'] or policy.get('authorization')!='APPROVED' else 'AUTHORIZED_PENDING_REMOTE_READBACK'
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path)
    parser.add_argument('--policy',type=Path,required=True)
    parser.add_argument('--comprehension-receipt',type=Path,default=None)
    parser.add_argument('--self-dogfood-receipt',type=Path,default=None)
    parser.add_argument('--require-self-dogfood',action='store_true')
    parser.add_argument('--allow-git-dirs',action='store_true')
    parser.add_argument('--showcase-gate',action='store_true',help='run full showcase gates (consumption/surface/comprehension) in addition to F09/F10')
    parser.add_argument('--fresh-clone-receipt',type=Path)
    parser.add_argument('--fidelity-receipt',type=Path)
    args=parser.parse_args()
    export=args.export.resolve()
    if not export.is_dir():
        parser.error('export root must be a directory')
    try:
        policy=json.loads(args.policy.read_text(encoding='utf-8'))
        if not isinstance(policy,dict):
            raise ValueError('policy must be an object')
        if args.showcase_gate:
            result=run_showcase_gate(export,policy,comprehension_receipt=args.comprehension_receipt,self_dogfood_receipt=args.self_dogfood_receipt,require_self_dogfood=args.require_self_dogfood,allow_git_dirs=args.allow_git_dirs,fresh_clone_receipt=args.fresh_clone_receipt,fidelity_receipt=args.fidelity_receipt)
        else:
            result=check(export,policy,allow_git_dirs=args.allow_git_dirs)
    except (OSError,ValueError) as exc:
        result={'F09':'BLOCK','F10':'STOP','errors':[str(exc)]}
    print(json.dumps(result,ensure_ascii=False))
    return result['F09']!='PASS' or (args.showcase_gate and not result.get('READY_FOR_APPROVAL'))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
