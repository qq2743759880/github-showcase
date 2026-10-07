"""Content bindings for local evidence; receipts never authorize remote writes."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

SKIP = {'.git', '.mimosa', '.cache', 'node_modules', '.venv', '__pycache__', '.pytest_cache'}

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def tree_digest(root, skip_usage=False):
    root = Path(root).resolve()
    rows = []
    for directory,dirs,files in os.walk(root,followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP and not (skip_usage and d == 'usage')]
        for name in dirs+files:
            path=Path(directory)/name
            if path.is_symlink():
                raise ValueError('linked evidence path: '+path.relative_to(root).as_posix())
        for name in files:
            path=Path(directory)/name
            rows.append([path.relative_to(root).as_posix(),sha256(path)])
    rows.sort(key=lambda row:row[0])
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()

def read_receipt(path, kind):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('kind') != kind or data.get('status') != 'PASS':
        raise ValueError('invalid ' + kind + ' receipt')
    return data

def comprehension(path, export):
    data = read_receipt(path, 'reader-comprehension')
    readme = Path(export) / 'README.md'
    if data.get('readme_sha256') != sha256(readme):
        raise ValueError('comprehension receipt is stale')
    answers = data.get('answers', [])
    text = readme.read_text(encoding='utf-8')
    if data.get('independent') is not True or not data.get('reviewer') or len(answers) != 5:
        raise ValueError('five independent answers required')
    if {a.get('question') for a in answers} != {'what', 'problem', 'input', 'output', 'difference'}:
        raise ValueError('comprehension questions incomplete')
    for answer in answers:
        if not answer.get('answer') or not answer.get('quote') or answer['quote'] not in text:
            raise ValueError('comprehension answer lacks README evidence')
    return data

def self_dogfood(path, export, product):
    data = read_receipt(path, 'self-dogfood')
    if data.get('export_digest') != tree_digest(export) or data.get('product_digest') != tree_digest(product, skip_usage=True):
        raise ValueError('self-dogfood receipt is stale')
    if not data.get('run_id') or not data.get('fidelity_receipt'):
        raise ValueError('self-dogfood run/fidelity evidence required')
    base=Path(path).resolve().parent
    receipt=(base/data['fidelity_receipt']).resolve()
    if not receipt.is_relative_to(base) or not receipt.is_file() or data.get('fidelity_sha256')!=sha256(receipt):
        raise ValueError('self-dogfood fidelity receipt missing or changed')
    fidelity=read_receipt(receipt,'skill-fidelity')
    trace=(receipt.parent/fidelity.get('trace_path','')).resolve()
    if not trace.is_relative_to(base) or not trace.is_file() or fidelity.get('export_digest')!=data['export_digest'] or fidelity.get('trace_sha256')!=sha256(trace):
        raise ValueError('self-dogfood fidelity trace differs')
    if json.loads(trace.read_text(encoding='utf-8')).get('run_id')!=data['run_id']:
        raise ValueError('self-dogfood run differs from fidelity run')
    return data

def _git(root,*args):
    return subprocess.run(['git','-C',str(root),*args],capture_output=True,check=True).stdout

def export_commit(export):
    top=Path(_git(export,'rev-parse','--show-toplevel').decode('utf-8').strip()).resolve()
    if top!=Path(export).resolve():
        raise ValueError('code export must be its own committed repository')
    return _git(export,'rev-parse','HEAD').decode().strip()

def tracked_digest(root):
    rows=[]
    for name in _git(root,'ls-files','-z').split(b'\0'):
        if name:
            relative=name.decode('utf-8'); path=(Path(root)/relative).resolve()
            if not path.is_relative_to(Path(root).resolve()) or not path.is_file():
                raise ValueError('missing/unsafe cloned source')
            rows.append([relative,sha256(path)])
    rows.sort(key=lambda row:row[0])
    return hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def fresh_clone(path, export, source_release, expected_commit=None):
    data = read_receipt(path, 'fresh-clone')
    if data.get('export_digest') != tree_digest(export) or not data.get('commit'):
        raise ValueError('fresh-clone receipt is stale')
    base = Path(path).resolve().parent
    expected_commit=expected_commit or export_commit(export)
    clone=(base/data.get('clone_dir','')).resolve()
    if not data.get('clone_dir') or not clone.is_relative_to(base) or clone==Path(export).resolve():
        raise ValueError('separate local clone evidence required')
    if data['commit']!=expected_commit or export_commit(clone)!=expected_commit:
        raise ValueError('fresh-clone commit does not match final export')
    if tracked_digest(clone)!=tree_digest(export):
        raise ValueError('fresh-clone tracked source differs from final export')
    steps = data.get('steps', [])
    kinds = {'clone', 'runtime-install', 'setup', 'start', 'verification-install', 'tests'}
    if {s.get('kind') for s in steps} != kinds:
        raise ValueError('fresh-clone steps incomplete')
    for step in steps:
        if step.get('exit_code') != 0 or not step.get('command'):
            raise ValueError('fresh-clone step failed')
        log = (base / step.get('log', '')).resolve()
        if not log.is_relative_to(base) or not log.is_file() or step.get('log_sha256') != sha256(log):
            raise ValueError('fresh-clone log missing or changed')
    for entry in source_release.get('entry_points', []):
        target = (Path(export) / entry).resolve()
        if not target.is_relative_to(Path(export).resolve()) or not target.is_file():
            raise ValueError('source entry missing: ' + entry)
    if source_release.get('include_code') is not True or not source_release.get('entry_points'):
        raise ValueError('source release incomplete')
    return data


def publication_path(name):
    """Conventional CI/config paths have publication identity in every consumer."""
    parts=Path(name).parts
    return parts[:2]==('.github','workflows') or (len(parts)==2 and parts[0]=='.github' and name.endswith('.json'))
