"""Diagnose phase capabilities without installing tools or probing credentials."""
import argparse,importlib.util,json,os,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def probe(name,args,tools):
    exe=tools.get(name) or shutil.which(name)
    if not exe:return {'status':'MISSING','reason':'Configure tools.'+name+' or PATH'}
    try:
        r=subprocess.run([exe,*args],capture_output=True,text=True,timeout=20,errors='replace');lines=(r.stdout or r.stderr).splitlines()
        return {'status':'AVAILABLE' if r.returncode==0 else 'MISSING','executable':str(exe),'exit':r.returncode,'version':lines[0][:150] if lines else ''}
    except (OSError,subprocess.TimeoutExpired) as exc:return {'status':'MISSING','reason':str(exc)}
def browser(tools):
    configured=tools.get('browser') or os.environ.get('ARCHIFY_CHROME') or os.environ.get('PUPPETEER_EXECUTABLE_PATH')
    if configured:
        found=shutil.which(configured) or (configured if Path(configured).is_file() else None)
        return {'status':'AVAILABLE' if found else 'MISSING','executable':found,'source':'runtime config or environment'}
    candidates=[shutil.which(n) for n in ['chromium','chromium-browser','google-chrome','google-chrome-stable','chrome']]
    if sys.platform=='win32':
        for key in ['ProgramFiles','ProgramFiles(x86)','LOCALAPPDATA']:
            if os.environ.get(key):
                for app in ['Google/Chrome','Chromium','Microsoft/Edge']:candidates.append(str(Path(os.environ[key])/app/'Application'/('msedge.exe' if app=='Microsoft/Edge' else 'chrome.exe')))
    elif sys.platform=='darwin':candidates.append('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    found=next((p for p in candidates if p and Path(p).is_file()),None)
    return {'status':'AVAILABLE' if found else 'MISSING','executable':found,'source':'platform capability discovery; real browser check still required'}
def diagnose(root=ROOT,plan=None,runtime_config=None,publish=False):
    root=Path(root).resolve();tools=(runtime_config or {}).get('tools',{})
    all_phases=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((root/'references/phases').glob('*.json'))]
    selected=(plan or {}).get('phases',[])
    probes={'python':{'status':'AVAILABLE','classification':'Required','executable':sys.executable,'version':sys.version.split()[0]}}
    for name in ['node','git','ffmpeg','gh']:
        probes[name]=probe(name,['-version'] if name=='ffmpeg' else ['--version'],tools);probes[name]['classification']='Optional' if name=='gh' else 'Phase-specific'
    if probes['node']['status']=='AVAILABLE':
        try:
            if int(probes['node']['version'].lstrip('v').split('.')[0])<24:probes['node'].update(status='MISSING',reason='Node >=24 required')
        except ValueError:probes['node'].update(status='MISSING',reason='unrecognized Node version')
    probes['browser']={**browser(tools),'classification':'Phase-specific'};probes['chrome-or-chromium']=probes['browser'];probes['mermaid-browser']=probes['browser']
    node=probes['node'].get('executable')
    for name,entry in [('snap-x','scripts/snap-x.mjs'),('mermaid-cli','scripts/render-c4.mjs')]:
        r=probe('node',[str(root/entry),'--version'],tools) if node else {'status':'MISSING','reason':'Node unavailable'};r['classification']='Phase-specific';probes[name]=r
    probes['archify']={'status':'AVAILABLE' if (root/'vendor/archify/bin/archify.mjs').is_file() and node else 'MISSING','classification':'Phase-specific','meaning':'locked CLI present; native finalize still required'}
    probes['github-backend']={'status':probes['gh']['status'],'classification':'Required' if publish else 'Optional','meaning':'gh presence only; access not probed; an authorized connector or git/browser backend can be supplied independently'}
    spec=importlib.util.spec_from_file_location('doctor_vendor',root/'scripts/verify-vendors.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);errors=v.verify(root)
    phases={p['phase']:{'status':'BLOCKED' if errors or any(probes.get(n,{}).get('status')!='AVAILABLE' for n in p['runtime_dependencies']) else 'AVAILABLE','missing':[n for n in p['runtime_dependencies'] if probes.get(n,{}).get('status')!='AVAILABLE']} for p in (selected or all_phases)}
    blocked=bool(errors) or any(phases[p['phase']]['status']=='BLOCKED' for p in selected) or (publish and probes['github-backend']['status']!='AVAILABLE')
    return {'status':'BLOCKED' if blocked else 'READY','probes':probes,'vendor_errors':errors,'phases':phases,'selected_phases':[p['phase'] for p in selected],'remote_publish':'NOT_PROBED_LOCAL_ONLY' if not publish else 'ACCESS_UNVERIFIED','meaning':'Only selected phase dependencies block local runs.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',type=Path);p.add_argument('--runtime-config',type=Path);p.add_argument('--publish',action='store_true');a=p.parse_args()
    r=diagnose(ROOT,json.loads(a.plan.read_text(encoding='utf-8')) if a.plan else None,json.loads(a.runtime_config.read_text(encoding='utf-8')) if a.runtime_config else None,a.publish);print(json.dumps(r,ensure_ascii=False,indent=2));return r['status']=='BLOCKED'
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');sys.exit(main())
