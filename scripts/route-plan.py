"""Select capability roles without loading unrouted vendor instructions."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('adapter_validator', ROOT / 'scripts/validate-adapter.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
spec = importlib.util.spec_from_file_location('archify_routing', ROOT / 'scripts/archify-routing.py')
archify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archify)

def plan(adapter, requested=None, root=ROOT):
    errors = validator.validate(adapter)
    if errors:
        raise ValueError('; '.join(errors))
    code = any(r['root_type'] in {'code', 'mixed'} for r in adapter['project_roots'])
    phases = requested or ['F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F08', 'F09', 'F10']
    selected = []
    skipped = {}
    for phase in dict.fromkeys(phases):
        if phase == 'F03' and (not code or not adapter.get('architecture_spec', {}).get('nodes')):
            skipped[phase] = 'No evidenced software architecture; do not invent containers'
            continue
        if phase == 'F04' and not adapter.get('workflow_spec', {}).get('chains'):
            skipped[phase] = 'No evidenced workflow'
            continue
        if phase == 'F05' and not (adapter.get('metrics') or adapter.get('domain_profiles')):
            skipped[phase] = 'No metrics or evidenced capability categories'
            continue
        if phase == 'F07' and adapter.get('demo_scenario', {}).get('status') != 'APPROVED_MEDIA':
            skipped[phase] = 'No approved real media'
            continue
        path = root / 'references/phases' / (phase + '.json')
        if not path.is_file():
            raise ValueError('unknown phase ' + phase)
        item=json.loads(path.read_text(encoding='utf-8'))
        if phase in {'F03','F04'}:
            item.update(archify.provenance(adapter))
        selected.append(item)
    # Evidence discovery cannot be skipped when the supplied fact set is unverified.
    if not adapter['facts_source'].get('preverified') and not any(p['phase'] == 'F01' for p in selected):
        selected.insert(0, json.loads((root / 'references/phases/F01.json').read_text(encoding='utf-8')))
    return {'schema_version': 2, 'project': adapter.get('project'), 'phases': selected, 'skipped': skipped,
            'load_policy': 'Read each selected workflow first; load its vendor and step reference only at execution',
            'remote_publish': 'STOP' if adapter['publication_policy']['authorization'] != 'APPROVED' else 'REQUIRES_REMOTE_READBACK'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('adapter', type=Path)
    parser.add_argument('--phases', nargs='+')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = plan(validator.load(args.adapter), args.phases)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text)

if __name__ == '__main__':
    main()
