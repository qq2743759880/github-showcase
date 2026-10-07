"""Package current execution/legal/verification closure without the product showcase."""
import argparse,hashlib,importlib.util,json,re,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def classify(name):
    if name in {'LICENSE','THIRD_PARTY_NOTICES.md'} or any(token in Path(name).name.upper() for token in ['LICENSE','NOTICE','OFL']):
        category,consumer='LEGAL_ONLY','Redistribution copyright / license obligations'
    elif name.startswith('tests/'):
        category,consumer='VERIFICATION_ONLY','Clean-install unittest discovery; not generation execution'
    elif name.startswith('vendor/') and '/examples/' in name:
        category,consumer='NATIVE_EXAMPLE_REQUIRED','Locked original Skill type/scenario/localization authoring references and CLI proof examples'
    elif name.startswith('vendor/'):
        category,consumer='VENDOR_NATIVE_REQUIRED','Locked original integrated / reviewer / optional method or native CLI import/resource closure'
    elif name in {'SKILL.md','vendors.lock.json','references/project-contract.md','references/bindings.json','references/core-contracts.json','scripts/doctor.py','scripts/verify-vendors.py'}:
        category,consumer='ALWAYS_RUNTIME','Entry, route contracts or installation integrity and dependency diagnosis'
    else:
        category,consumer='PHASE_RUNTIME','Selected phase instructions, adapter, wrapper, gate, packaging or pinned dependency installation'
    return {'classification':category,'consumer':consumer}
def inventory(root=ROOT):
    root=Path(root).resolve();paths={'SKILL.md','LICENSE','THIRD_PARTY_NOTICES.md','vendors.lock.json','package.json','package-lock.json','requirements-verification.txt','adapters/template/adapter.md','manifests/runtime-deps.json'}
    for directory,patterns in [('references',['*.md','*.json']),('scripts',['*.py','*.mjs']),('tests',['test_*.py'])]:
        for pattern in patterns:paths.update(p.relative_to(root).as_posix() for p in (root/directory).rglob(pattern) if '__pycache__' not in p.parts)
    lock=json.loads((root/'vendors.lock.json').read_text(encoding='utf-8'));paths.update(name for vendor in lock['vendors'] for name in vendor['files'])
    for name in paths:
        p=root/name
        if any(part in {'.git','.mimosa','node_modules','.cache','usage','research','vNext'} for part in Path(name).parts) or p.is_symlink() or not p.resolve().is_relative_to(root) or not p.is_file():raise ValueError('missing/unsafe portable member: '+name)
    return sorted(paths)
def build(root,output,extract):
    root=Path(root).resolve();output=Path(output).resolve();extract=Path(extract).resolve()
    if output.exists() or extract.exists() or output.is_relative_to(root) or extract.is_relative_to(root):raise ValueError('fresh artifact and extract outside source required')
    spec=importlib.util.spec_from_file_location('portable_vendor',root/'scripts/verify-vendors.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);errors=v.verify(root)
    if errors:raise ValueError('; '.join(errors))
    members=inventory(root);classes={p:classify(p) for p in members};legal=[p for p in members if classes[p]['classification']=='LEGAL_ONLY'];verification=[p for p in members if classes[p]['classification']=='VERIFICATION_ONLY']
    entry=(root/'SKILL.md').read_text(encoding='utf-8');name=re.search(r'^name:\s*(\S+)',entry,re.M).group(1);version=re.search(r'^\s*version:\s*(\S+)',entry,re.M).group(1).strip(chr(34)+chr(39))
    manifest={'schema_version':1,'name':name,'version':version,'execution':[p for p in members if p not in legal+verification],'redistribution':members,'verification':verification,'classifications':classes,'showcase':[],'publication':[],'build_evidence':[],'files':[{'path':p,'bytes':(root/p).stat().st_size,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in members],'closure_basis':{'owned':'entry, contracts, phases, adapter template and deterministic scripts','vendor':'exact current vendors.lock union with full methods and original legal files','verification':'product regression sources only; no historical fixtures/results','dependencies':'pinned package/optional YAML requirements; installed binaries and caches excluded; mixed YAML/verification requirements have a real phase installation consumer'}}
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for p,data in [(p,(root/p).read_bytes()) for p in members]+[('portable-manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())]:
            item=zipfile.ZipInfo(name+'/'+p,(1980,1,1,0,0,0));item.external_attr=0o100644<<16;item.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(item,data)
    extract.mkdir(parents=True)
    with zipfile.ZipFile(output) as archive:archive.extractall(extract)
    for item in manifest['files']:
        if hashlib.sha256((extract/name/item['path']).read_bytes()).hexdigest()!=item['sha256']:raise ValueError('fresh extraction differs')
    return {'status':'PASS','artifact':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'extract_root':str(extract/name),'manifest':manifest,'limits':'Integrity only; L1/L2 need real relocated target execution; L3 needs another machine/OS.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);p.add_argument('--extract',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
    try:r=build(a.root,a.output,a.extract);a.receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in r.items() if k!='manifest'}));return 0
    except (OSError,ValueError,KeyError) as exc:print(json.dumps({'status':'BLOCKED','error':str(exc)}));return 1
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');sys.exit(main())
