"""Compose the vendored secret scanner with export privacy/license policy checks."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def check(export,policy):
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
        if any(p in {'.git','.mimosa','.cache','node_modules','.venv','__pycache__'} for p in relative.parts):
            errors.append('regenerated/private directory in export')
        if path.stat().st_size>2_000_000:
            continue
        value=path.read_bytes()
        if any(literal.encode('utf-8') in value for literal in literals):
            errors.append('private literal in export: '+relative.as_posix())
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
    scan=subprocess.run([sys.executable,str(ROOT/'vendor/secret-scanner/skills/secret-scanner/engine.py'),str(export),'--json','--include-tests'],capture_output=True,text=True,errors='replace',env=env)
    if scan.returncode != 0:
        errors.append('vendored secret scanner rejected export' if scan.returncode==1 else 'vendored secret scanner failed')
    return {'F09':'BLOCK' if errors else 'PASS','F10':'STOP' if errors else 'LOCAL_PACKAGE_ALLOWED','remote_publish':'STOP' if errors or policy.get('authorization')!='APPROVED' else 'AUTHORIZED_PENDING_REMOTE_READBACK','errors':sorted(set(errors)),'secret_scanner_exit':scan.returncode}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path)
    parser.add_argument('--policy',type=Path,required=True)
    args=parser.parse_args()
    export=args.export.resolve()
    if not export.is_dir():
        parser.error('export root must be a directory')
    try:
        policy=json.loads(args.policy.read_text(encoding='utf-8'))
        if not isinstance(policy,dict):
            raise ValueError('policy must be an object')
        result=check(export,policy)
    except (OSError,ValueError) as exc:
        result={'F09':'BLOCK','F10':'STOP','errors':[str(exc)]}
    print(json.dumps(result,ensure_ascii=False))
    return result['F09']!='PASS'

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
