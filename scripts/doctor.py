"""Read-only runtime probe. No installation, credential reads or remote writes."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def version(name, args):
    executable=shutil.which(name)
    if not executable:
        return {'status':'BLOCKED','reason':'not_installed'}
    try:
        result=subprocess.run([executable,*args],capture_output=True,text=True,errors='replace',timeout=15)
        lines=(result.stdout or result.stderr).splitlines()
        return {'status':'AVAILABLE' if result.returncode==0 else 'BLOCKED','exit':result.returncode,'version':lines[0][:180] if lines else 'no version output'}
    except (OSError,subprocess.TimeoutExpired):
        return {'status':'BLOCKED','reason':'runtime_failed'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--github-connector',choices=['unverified','read-only','write-verified'],default='unverified',help='Host probe receipt supplied by orchestrator; script cannot inspect host tools')
    args=parser.parse_args()
    probes={'python':{'status':'AVAILABLE','version':sys.version.split()[0]}}
    for name,arguments in [('node',['--version']),('npm',['--version']),('ffmpeg',['-version']),('bash',['--version']),('jq',['--version']),('gh',['--version'])]:
        probes[name]=version(name,arguments)
    probes['pyyaml']={'status':'AVAILABLE' if importlib.util.find_spec('yaml') else 'BLOCKED'}
    snap=ROOT/'node_modules/.bin'/('snap-x.cmd' if sys.platform=='win32' else 'snap-x')
    probes['snap-x']={'status':'BLOCKED','reason':'not_installed'}
    pkg=ROOT/'node_modules/@snap-x/cli/package.json'
    if pkg.exists():
        installed=json.loads(pkg.read_text(encoding='utf-8')).get('version')
        probes['snap-x']={'status':'AVAILABLE' if installed=='0.2.1' and snap.exists() else 'BLOCKED','package_version':installed,'required':'0.2.1'}
    probes['github_connector']={'status':'AVAILABLE' if args.github_connector=='write-verified' else 'BLOCKED','host_receipt':args.github_connector}
    probes['github_auth']={'status':'BLOCKED','reason':'no_verified_write_backend'}
    if probes['gh']['status']=='AVAILABLE':
        try:
            auth=subprocess.run([shutil.which('gh'),'auth','status'],capture_output=True,timeout=15)
            # Do not echo auth output; only report exit status.
            probes['github_auth']={'status':'AVAILABLE' if auth.returncode==0 else 'BLOCKED','exit':auth.returncode}
        except (OSError,subprocess.TimeoutExpired):
            pass
    spec=importlib.util.spec_from_file_location('verify_vendors',ROOT/'scripts/verify-vendors.py')
    verifier=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    errors=verifier.verify()
    probes['vendor_hashes']={'status':'BLOCKED' if errors else 'AVAILABLE','errors':errors}
    manifest=json.loads((ROOT/'references/bindings.json').read_text(encoding='utf-8'))
    phase_status={}
    for bind in manifest['bindings']:
        missing=[n for n in bind['runtime_dependencies'] if probes.get(n,{}).get('status')!='AVAILABLE']
        phase_status[bind['phase']]={'status':'BLOCKED' if missing or errors else 'AVAILABLE','missing':missing,'meaning':'dependencies available; invocation and output validation still required'}
    phase_status['F07']['optional']=True
    phase_status['F10.remote_publish']={'status':'AVAILABLE' if probes['github_connector']['status']=='AVAILABLE' or probes['github_auth']['status']=='AVAILABLE' else 'BLOCKED'}
    print(json.dumps({'probes':probes,'phases':phase_status},ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
