"""Export the current locked Snap-X dependency closure and portable rebuild helpers."""
import argparse
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

def export(destination):
    destination = destination.resolve()
    for part in [destination, *destination.parents]:
        if part.is_symlink() or part.is_junction():
            raise ValueError('linked output path')
    lock = json.loads((ROOT / 'package-lock.json').read_text(encoding='utf-8'))
    packages = lock['packages']
    entry = 'node_modules/@snap-x/cli'
    selected = {}
    pending = [entry]
    while pending:
        key = pending.pop()
        if key in selected:
            continue
        record = packages[key]
        selected[key] = record
        for name in {**record.get('dependencies', {}), **record.get('optionalDependencies', {})}:
            parent = PurePosixPath(key)
            while True:
                candidate = str(parent / 'node_modules' / name)
                if candidate in packages:
                    pending.append(candidate)
                    break
                if str(parent) == '.':
                    raise ValueError('unresolved locked dependency: ' + name)
                parent = parent.parent
    destination.mkdir(parents=True, exist_ok=True)
    package = {'name': 'showcase-visual-source', 'private': True, 'type': 'module',
               'engines': {'node': '>=22.15.0'},
               'dependencies': {'@snap-x/cli': packages[entry]['version']}}
    original = json.loads((ROOT / 'package.json').read_text(encoding='utf-8'))
    if original.get('overrides'):
        package['overrides'] = original['overrides']
    if (destination / 'package.json').exists():
        previous = json.loads((destination / 'package.json').read_text(encoding='utf-8'))
        for name in ['name', 'scripts']:
            if name in previous:
                package[name] = previous[name]
    closure = {'name': package['name'], 'lockfileVersion': lock['lockfileVersion'], 'requires': True,
               'packages': {'': package, **dict(sorted(selected.items()))}}
    (destination / 'package.json').write_text(json.dumps(package, indent=2) + '\n', encoding='utf-8')
    (destination / 'package-lock.json').write_text(json.dumps(closure, indent=2) + '\n', encoding='utf-8')
    (destination / 'windows-esm.mjs').write_bytes((ROOT / 'scripts/windows-esm.mjs').read_bytes())
    (destination / 'LICENSE').write_bytes((ROOT / 'LICENSE').read_bytes())
    (destination / 'snap.mjs').write_text("""import {spawnSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {readFileSync} from 'node:fs';
const here=path.dirname(fileURLToPath(import.meta.url));
const expected=JSON.parse(readFileSync(path.join(here,'package-lock.json'),'utf8')).packages['node_modules/@snap-x/cli'].version;
const actual=JSON.parse(readFileSync(path.join(here,'node_modules/@snap-x/cli/package.json'),'utf8')).version;
if(actual!==expected) throw new Error('Installed renderer differs from lock');
const hooks=process.platform==='win32'?['--import',pathToFileURL(path.join(here,'windows-esm.mjs')).href]:[];
const result=spawnSync(process.execPath,[...hooks,path.join(here,'node_modules/@snap-x/cli/bin.mjs'),...process.argv.slice(2)],{stdio:'inherit',cwd:here,env:{...process.env,SNAP_X_CACHE_DIR:path.join(here,'.cache')}});
if(result.error) throw result.error;
process.exit(result.status??2);
""", encoding='utf-8')
    return {'status': 'PASS', 'packages': len(selected), 'cli': packages[entry]['version'],
            'core': selected['node_modules/@snap-x/core']['version']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.destination)))
