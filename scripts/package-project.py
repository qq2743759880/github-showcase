"""Gate and archive a clean exported project Git commit, without Skill metadata."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def package(export, output, policy, comprehension_receipt=None, fidelity_receipt=None, fresh_clone_receipt=None, self_dogfood_receipt=None, require_self_dogfood=False):
    # Scan an isolated git archive so private .git metadata is never exported.
    def git(*args):
        return subprocess.run(['git','-C',str(export),*args],capture_output=True,check=True)
    if git('status','--porcelain','--untracked-files=all').stdout.strip():
        raise ValueError('export repository must be clean, including untracked files')
    if git('rev-parse','--show-toplevel').stdout.decode().strip().replace('\\','/') != export.as_posix():
        raise ValueError('export must be its own repository root')
    commit=git('rev-parse','HEAD').stdout.decode().strip()
    blocked={'.git','.mimosa','.cache','node_modules','.venv','__pycache__','.pytest_cache','usage'}
    for name in git('ls-files','-z').stdout.split(b'\0'):
        if name and blocked.intersection(Path(name.decode('utf-8')).parts):
            raise ValueError('regenerated/private directory in tracked export')
    if any(row.startswith((b'120000 ',b'160000 ')) for row in git('ls-files','--stage','-z').stdout.split(b'\0')):
        raise ValueError('linked files or submodules require an explicit export')
    output=output.resolve()
    if output.is_relative_to(export):
        raise ValueError('output must be outside export repository')
    if output.exists():
        raise ValueError('output already exists')
    output.parent.mkdir(parents=True,exist_ok=True)
    import zipfile
    with tempfile.TemporaryDirectory(prefix='project-stage-',dir=output.parent) as temp:
        archive=Path(temp)/'project.zip'
        git('archive','--format=zip','--output='+str(archive),'HEAD')
        staged=Path(temp)/'export'
        with zipfile.ZipFile(archive) as bundle:
            for name in bundle.namelist():
                if Path(name).is_absolute() or '..' in Path(name).parts:
                    raise ValueError('unsafe archive path')
            bundle.extractall(staged)
        spec=importlib.util.spec_from_file_location('release_gate',ROOT/'scripts/release-gate.py')
        gate=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        result=gate.run_showcase_gate(staged,policy,comprehension_receipt=comprehension_receipt,
            fidelity_receipt=fidelity_receipt,fresh_clone_receipt=fresh_clone_receipt,
            self_dogfood_receipt=self_dogfood_receipt,require_self_dogfood=require_self_dogfood,expected_commit=commit)
        if result['F09']!='PASS' or not result['READY_FOR_APPROVAL']:
            raise ValueError('F09 BLOCK; F10 STOP: '+', '.join(result['errors']+result['gates']))
        output.write_bytes(archive.read_bytes())
    return {'status':'PACKAGE_PASS','commit':commit,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'remote_publish':result['remote_publish']}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--policy',type=Path,required=True)
    parser.add_argument('--comprehension-receipt',type=Path,required=True)
    parser.add_argument('--fidelity-receipt',type=Path)
    parser.add_argument('--fresh-clone-receipt',type=Path)
    parser.add_argument('--self-dogfood-receipt',type=Path)
    parser.add_argument('--require-self-dogfood',action='store_true')
    args=parser.parse_args()
    try:
        result=package(args.export.resolve(),args.output,json.loads(args.policy.read_text(encoding='utf-8')),args.comprehension_receipt,args.fidelity_receipt,args.fresh_clone_receipt,args.self_dogfood_receipt,args.require_self_dogfood)
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:
        print(json.dumps({'status':'BLOCKED','error':str(exc)}))
        return 1
    print(json.dumps(result))
    return 0

if __name__=='__main__':
    sys.exit(main())
