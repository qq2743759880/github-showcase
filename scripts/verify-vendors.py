"""Verify the exact vendored file set and SHA256 lock, fail closed."""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]

def verify(root=ROOT):
    lock=root/'vendors.lock.json'
    if not lock.exists():
        return ['vendors.lock.json missing']
    data=json.loads(lock.read_text(encoding='utf-8'))
    entities=data.get('vendors',[])
    errors=[]
    if not entities:
        errors.append('vendor closure is empty')
    expected=set()
    for entity in entities:
        for key in ['name','phase','role','upstream','revision','entry','files','hashes','license','modifications']:
            if key not in entity:
                errors.append('missing vendor field '+key)
        if entity.get('entry') not in entity.get('files',[]):
            errors.append('entry not locked: '+entity.get('name','?'))
        if set(entity.get('files',[])) != set(entity.get('hashes',{})):
            errors.append('file/hash mismatch: '+entity.get('name','?'))
        for name in entity.get('files',[]):
            path=root/name
            if not name.startswith('vendor/') or '..' in Path(name).parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                errors.append('unsafe vendor path '+name)
                continue
            expected.add(name)
            if not path.is_file():
                errors.append('missing '+name)
            elif hashlib.sha256(path.read_bytes()).hexdigest() != entity['hashes'].get(name):
                errors.append('hash mismatch '+name)
    generated={'node_modules','__pycache__','.cache','.venv'}
    actual={p.relative_to(root).as_posix() for p in (root/'vendor').rglob('*') if p.is_file() and not any(part in generated for part in p.relative_to(root/'vendor').parts)}
    errors.extend('unlocked file '+name for name in sorted(actual-expected))
    return errors

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        errors=verify()
    except (OSError,ValueError,KeyError) as exc:
        errors=[str(exc)]
    print(json.dumps({'status':'FAIL' if errors else 'PASS','errors':errors},ensure_ascii=False))
    sys.exit(bool(errors))
