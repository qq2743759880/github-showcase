"""Package tracked release files through the vendored skill-creator tool."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import os

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    result=subprocess.run(['git','-C',str(ROOT),'ls-files','-z'],capture_output=True,check=True)
    names=[n.decode('utf-8') for n in result.stdout.split(b'\0') if n]
    if not names or 'SKILL.md' not in names:
        raise ValueError('release files must be committed before packaging')
    environment={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8'}
    # Temporary staging is beneath the caller's approved output, never in user-home caches.
    with tempfile.TemporaryDirectory(prefix='package-',dir=output) as directory:
        stage=Path(directory)/'github-project-showcase'
        stage.mkdir()
        for name in names:
            relative=Path(name)
            if any(p in {'.git','.mimosa','.cache','node_modules','__pycache__','.venv','usage'} for p in relative.parts):
                raise ValueError('regenerated/private directory tracked: '+name)
            source=ROOT/relative
            if source.is_symlink() or not source.resolve().is_relative_to(ROOT.resolve()):
                raise ValueError('unsafe tracked file: '+name)
            target=stage/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
        scan=subprocess.run([sys.executable,str(ROOT/'vendor/secret-scanner/skills/secret-scanner/engine.py'),str(stage),'--json'],capture_output=True,text=True,errors='replace',env=environment)
        if scan.returncode != 0:
            print('F09 BLOCK: package secret scan did not pass')
            return 1
        creator=ROOT/'vendor/skill-creator/skills/skill-creator'
        result=subprocess.run([sys.executable,'-m','scripts.package_skill',str(stage),str(output)],cwd=creator,capture_output=True,text=True,errors='replace',env=environment)
        if result.returncode:
            print(result.stdout)
            print(result.stderr)
            return result.returncode
        print('PACKAGE_PASS: '+str(output/'github-project-showcase.skill'))
    return 0

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
