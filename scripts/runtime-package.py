"""Build a source-byte-preserving Agent Skill runtime ZIP from an explicit allowlist."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path,PurePosixPath
import evidence

def sha(data):return hashlib.sha256(data).hexdigest()
def version(data):
    match=re.search(r'^\s+version:\s*[\"\']?([^\"\'\s]+)',data.decode('utf-8'),re.M)
    if not match:raise ValueError('SKILL metadata version missing')
    return match.group(1)
def safe(name):
    p=PurePosixPath(name)
    if not name or '\\' in name or ':' in name or p.is_absolute() or '..' in p.parts or str(p)!=name:
        raise ValueError('unsafe runtime path')
    return p
def original_distribution(relative,root,name,current_version,values):
    safe(relative);path=root/relative
    if path.is_symlink() or not path.resolve().is_relative_to(root) or not path.is_file():raise ValueError('unsafe original distribution authority')
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist();prefix=name+'/'
        if len(set(names))!=len(names) or any(not p.startswith(prefix) for p in names):raise ValueError('original distribution inventory invalid')
        originals={}
        for member in names:
            rel=member[len(prefix):];safe(rel);originals[rel]=archive.read(member)
        if set(originals)!=set(values):raise ValueError('original distribution paths must be preserved, including legal files')
        if version(originals['SKILL.md'])!=current_version:raise ValueError('original distribution version is not current authority')
        if any(originals[p]!=data for p,data in values.items()):raise ValueError('original distribution differs from current source bytes')
    return {'path':relative,'sha256':sha(path.read_bytes()),'files':sorted(originals)}
def inputs(manifest):
    name=manifest['name'];safe(name)
    if '/' in name:raise ValueError('runtime package name must be one directory')
    root=Path(manifest['source_root']).resolve()
    files=manifest.get('files',manifest.get('redistribution'))
    if 'execution' in manifest or 'redistribution' in manifest:
        execution=manifest.get('execution',[]);redistribution=manifest.get('redistribution',[])
        if not execution or 'SKILL.md' not in execution or len(set(execution))!=len(execution) or len(set(redistribution))!=len(redistribution) or not set(execution).issubset(redistribution) or set(files)!=set(redistribution):raise ValueError('execution must be included in exact redistribution closure')
    if not isinstance(files,list) or len(set(files))!=len(files) or 'SKILL.md' not in files:raise ValueError('explicit unique runtime files including SKILL.md required')
    if set(files).intersection(manifest.get("publication",[])) or any(evidence.publication_path(p) for p in files):raise ValueError("Publication files are not Runtime distribution dependencies")
    values={}
    for rel in files:
        safe(rel);p=root/rel
        if any(x.is_symlink() for x in [p,*list(p.parents)[:len(PurePosixPath(rel).parts)-1]]) or not p.resolve().is_relative_to(root) or not p.is_file():raise ValueError('runtime file escapes source or missing')
        values[rel]=p.read_bytes()
    if version(values['SKILL.md'])!=manifest['version']:raise ValueError('stale runtime version')
    if manifest.get('source_distribution'):original_distribution(manifest['source_distribution'],root,name,manifest['version'],values)
    return root,values
def package(manifest,output,extract):
    root,values=inputs(manifest);output=Path(output).resolve();extract=Path(extract).resolve()
    preserve=manifest.get('preserve_source_distribution',False)
    if not isinstance(preserve,bool):raise ValueError('preserve_source_distribution must be boolean')
    if preserve and not manifest.get('source_distribution'):raise ValueError('sealed distribution requires explicit source authority')
    if output.exists() or extract.exists() or output.is_relative_to(root) or extract.is_relative_to(root):raise ValueError('use fresh output/extract outside read-only source')
    output.parent.mkdir(parents=True,exist_ok=True)
    if preserve:
        output.write_bytes((root/manifest['source_distribution']).read_bytes())
    else:
        with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as bundle:
            for rel,data in sorted(values.items()):
                item=zipfile.ZipInfo(manifest['name']+'/'+rel,(1980,1,1,0,0,0));item.external_attr=0o100644<<16;item.compress_type=zipfile.ZIP_DEFLATED
                bundle.writestr(item,data)
    extract.mkdir(parents=True)
    with zipfile.ZipFile(output) as bundle:bundle.extractall(extract)
    receipt={'kind':'minimal-runtime','status':'PASS','name':manifest['name'],'version':manifest['version'],'package':str(output),'sha256':sha(output.read_bytes()),'extract_dir':str(extract),'files':[{'path':p,'bytes':len(data),'sha256':sha(data)} for p,data in sorted(values.items())]}
    if 'execution' in manifest:receipt.update(execution=manifest['execution'],redistribution=manifest['redistribution'])
    if manifest.get('source_distribution'):receipt['source_distribution']=original_distribution(manifest['source_distribution'],root,manifest['name'],manifest['version'],values)
    if preserve:receipt['preserved_source_distribution']=True
    errors=verify(receipt,root)
    if errors:raise ValueError('; '.join(errors))
    return receipt
def verify(receipt,source):
    try:
        if receipt['kind']!='minimal-runtime' or receipt['status']!='PASS':raise ValueError('runtime receipt not PASS')
        name=receipt['name'];safe(name)
        if '/' in name:raise ValueError('invalid package name')
        source=Path(source).resolve();package=Path(receipt['package']);extract=Path(receipt['extract_dir'])/name
        if sha(package.read_bytes())!=receipt['sha256']:raise ValueError('runtime ZIP changed')
        if receipt.get('preserved_source_distribution') and receipt['sha256']!=receipt.get('source_distribution',{}).get('sha256'):raise ValueError('sealed archive byte identity differs from source authority')
        files={r['path']:r for r in receipt['files']}
        if len(files)!=len(receipt['files']) or 'SKILL.md' not in files:raise ValueError('runtime inventory invalid')
        if set(p.relative_to(extract).as_posix() for p in extract.rglob('*') if p.is_file())!=set(files):raise ValueError('fresh extraction contains missing or extra files')
        with zipfile.ZipFile(package) as bundle:
            if len(bundle.namelist())!=len(files) or set(bundle.namelist())!={name+'/'+p for p in files}:raise ValueError('runtime ZIP inventory differs')
            for rel,identity in files.items():
                safe(rel)
                original=source/rel;unpacked=extract/rel
                if not original.resolve().is_relative_to(source) or original.is_symlink() or unpacked.is_symlink():raise ValueError('unsafe runtime input/extract')
                data=bundle.read(name+'/'+rel)
                if len(data)!=identity['bytes'] or sha(data)!=identity['sha256'] or data!=original.read_bytes() or data!=unpacked.read_bytes():raise ValueError('runtime bytes differ: '+rel)
            if version(bundle.read(name+'/SKILL.md'))!=receipt['version']:raise ValueError('stale runtime version')
            if receipt.get('source_distribution'):
                authority=receipt['source_distribution']
                checked=original_distribution(authority['path'],source,name,receipt['version'],{p:bundle.read(name+'/'+p) for p in files})
                if checked!=authority:raise ValueError('original distribution authority changed')
        return []
    except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as exc:return [str(exc)]
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('output',type=Path);p.add_argument('--extract',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
    try:
        r=package(json.loads(a.manifest.read_text(encoding='utf-8')),a.output,a.extract);a.receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(r,ensure_ascii=False));return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:print(json.dumps({'status':'BLOCKED','error':str(exc)}));return 1
if __name__=='__main__':raise SystemExit(main())
