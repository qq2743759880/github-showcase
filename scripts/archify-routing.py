"""Showcase provenance routing and semantic coverage; native Archify stays unchanged."""
import argparse,copy,hashlib,json,re,subprocess
from pathlib import Path,PurePosixPath
from urllib.parse import urlparse

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def relative(name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts or str(PurePosixPath(name))!=name:raise ValueError('canonical relative path required')
    return name
def provenance(adapter):
    root=Path(adapter['project_roots'][0]['path']).resolve()
    result={'provenance_mode':'LOCAL_CONTENT_BOUND','project_root':str(root),'provenance_reason':'local scope or repository evidence not approved/available'}
    intent=adapter.get('archify_provenance',{})
    if len(adapter['project_roots'])!=1 or not (intent.get('repository_evidence_required') is True and intent.get('origin_approved') is True and adapter['publication_policy']['authorization']=='APPROVED'):return result
    def git(*args):
        p=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=10)
        if p.returncode:raise ValueError('repository identity unavailable')
        return p.stdout.strip()
    try:
        if Path(git('rev-parse','--show-toplevel')).resolve()!=root:return result
        if git('status','--porcelain'):return result
        revision=git('rev-parse','HEAD');origin=git('remote','get-url','origin');url=urlparse(origin)
        if not re.fullmatch('[a-fA-F0-9]{40}',revision) or url.scheme!='https' or url.username or url.password or url.query or url.fragment or url.hostname not in {'github.com','gitee.com'} or not re.fullmatch(r'/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',url.path):return result
        result.update(provenance_mode='REPOSITORY_BACKED',provenance_reason='approved real repository identity',repository={'url':origin,'revision':revision,'link_mode':intent.get('link_mode','local-only')})
    except (OSError,ValueError,subprocess.TimeoutExpired):pass
    return result
def content_evidence(root,claims):
    root=Path(root).resolve();sources=[]
    if not isinstance(claims,list) or not claims:raise ValueError('inspected claims required')
    for item in claims:
        name=relative(item['path']);path=root/name
        if not path.resolve().is_relative_to(root) or any(p.is_symlink() for p in [path,*list(path.parents)[:len(PurePosixPath(name).parts)-1]]) or not path.is_file():raise ValueError('source missing or outside approved root')
        if not all(isinstance(item.get(k),str) and item[k].strip() for k in ('supports','purpose')):raise ValueError('claimed fact and inspection purpose required')
        sources.append({**item,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return {'provenance_mode':'LOCAL_CONTENT_BOUND','canonical_project_root':str(root),'sources':sources}
def local_candidate(candidate,reason='local-scope'):
    if reason not in {'local-scope','missing-origin','repository-identity-unavailable','repository-provenance-unavailable'}:raise ValueError('only provenance-only failure can change mode')
    def clean(value):
        if isinstance(value,list):return [clean(v) for v in value]
        if isinstance(value,dict):return {k:clean(v) for k,v in value.items() if k!='sources'}
        return value
    result=clean(copy.deepcopy(candidate));result.setdefault('meta',{}).pop('repository',None)
    return result
def finalize_arguments(kind,source,html,route):
    args=['finalize',kind,str(source),str(html),'--quality','showcase','--json']
    if route['provenance_mode']=='REPOSITORY_BACKED':args+=['--repo-root',route['project_root']]
    elif route['provenance_mode']!='LOCAL_CONTENT_BOUND':raise ValueError('unknown provenance mode')
    return args
def escalation(attempts,semantic_complete):
    if attempts and attempts[-1].get('status')=='pass':return 'DELIVER_SINGLE'
    if semantic_complete is not True or len(attempts)!=4:raise ValueError('complete semantic review and initial + two focused repairs + measured retry required')
    for receipt in attempts:
        codes=[d.get('code','') for d in receipt.get('diagnostics',[])]
        if receipt.get('status') not in {'fail','failed'} or receipt.get('diagnosticSummary',{}).get('truncated') or not codes or any(not code.startswith(('layout/','geometry/','composition/','workflow/')) or not any(w in code.lower() for w in ('corridor','crossing','overlap','viewport','readability','geometry','layout','explicit-pin-conflict')) for code in codes):raise ValueError('failure is not exclusively presentation complexity')
    return 'SEMANTIC_DECOMPOSITION'

def native_attempts(paths,original,review):
    """Check recorded native failures; semantic completeness remains a review."""
    if review.get('status')!='COMPLETE' or review.get('original_sha256')!=digest(original) or not isinstance(review.get('purpose'),str) or not review['purpose'].strip():raise ValueError('current content-bound semantic review required')
    receipts=[]
    for path in paths:
        receipt=json.loads(Path(path).read_text(encoding='utf-8'))
        if receipt.get('command')!='finalize' or receipt.get('quality')!='showcase':raise ValueError('native showcase attempt required')
        binding=receipt['specification'];source=Path(binding['path']);raw=source.read_bytes()
        if len(raw)!=binding['bytes'] or hashlib.sha256(raw).hexdigest()!=binding['sha256'] or semantics(json.loads(raw))!=semantics(original):raise ValueError('attempt source changed or semantics lost')
        receipts.append(receipt)
    return escalation(receipts,True)

NODE_GEOMETRY={'col','x','y','width','height','yOffset','sources'}
EDGE_GEOMETRY={'via','route','fromSide','toSide','channelX','channelY','labelAt','labelDx','labelDy','labelSegment','width','bias','sources'}
def semantics(graph):
    nodes={n['id']:{k:v for k,v in n.items() if k not in NODE_GEOMETRY} for n in graph['nodes']}
    if len(nodes)!=len(graph['nodes']):raise ValueError('duplicate semantic node')
    edges={digest({k:v for k,v in e.items() if k not in EDGE_GEOMETRY}):{k:v for k,v in e.items() if k not in EDGE_GEOMETRY} for e in graph['edges']}
    if len(edges)!=len(graph['edges']) or any(e['from'] not in nodes or e['to'] not in nodes for e in graph['edges']):raise ValueError('duplicate edge or missing endpoint')
    conditions={digest({'edge':key,'label':e['label']}):{'edge':key,'label':e['label']} for key,e in edges.items() if e.get('label')}
    conditions.update({digest({'node':key,'tag':n['tag']}):{'node':key,'tag':n['tag']} for key,n in nodes.items() if n.get('tag')})
    return {'nodes':nodes,'edges':edges,'conditions':conditions}
def coverage(original,views):
    origin=semantics(original);seen={k:{} for k in origin};parts={};extra=[]
    if not views:raise ValueError('required views missing')
    for name,graph in views.items():
        part=semantics(graph);parts[name]={k:list(v.values()) for k,v in part.items()}
        for kind,items in part.items():
            for key,value in items.items():
                if origin[kind].get(key)!=value:extra.append(kind+':'+key)
                seen[kind][key]=value
    missing=[kind+':'+key for kind,items in origin.items() for key in items if key not in seen[kind]]
    if missing or extra:raise ValueError('semantic coverage missing/changed: '+json.dumps({'missing':missing,'extra':extra}))
    return {'original_sha256':digest(original),'original_nodes':list(origin['nodes'].values()),'original_edges':list(origin['edges'].values()),'original_conditions':list(origin['conditions'].values()),'views':parts,'missing':[]}
def consumption_errors(export,views):
    # Reuse the existing Markdown visibility/README reachability contract.
    import importlib.util
    s=importlib.util.spec_from_file_location('coverage_reader',Path(__file__).with_name('release-gate.py'));gate=importlib.util.module_from_spec(s);s.loader.exec_module(gate)
    links=set()
    for rel,text in gate._reader_docs(Path(export)):
        for match in gate._visible_links(text):
            import os
            links.add(os.path.normpath(str(rel.parent/match.group(1).split('#')[0].split('?')[0])).replace('\\','/'))
    return ['required view not consumed: '+relative(v[k]) for v in views for k in ('source','html','preview') if relative(v[k]) not in links]
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    e=sub.add_parser('evidence');e.add_argument('root',type=Path);e.add_argument('claims',type=Path);e.add_argument('output',type=Path)
    c=sub.add_parser('coverage');c.add_argument('original',type=Path);c.add_argument('views',type=Path);c.add_argument('output',type=Path)
    a=p.parse_args()
    if a.action=='evidence':result=content_evidence(a.root,json.loads(a.claims.read_text(encoding='utf-8')))
    else:
        names=json.loads(a.views.read_text(encoding='utf-8'));graphs={n:json.loads(Path(f).read_text(encoding='utf-8')) for n,f in names.items()}
        result=coverage(json.loads(a.original.read_text(encoding='utf-8')),graphs)
        result['source_files']={n:{'path':str(Path(f).resolve()),'sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest()} for n,f in names.items()}
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':'PASS','output':str(a.output)}))
if __name__=='__main__':main()
