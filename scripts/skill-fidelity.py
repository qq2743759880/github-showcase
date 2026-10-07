"""Validate observable core workflow evidence, separate from semantic review."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence

ROOT = Path(__file__).resolve().parents[1]

def validate(trace_path, export, root=ROOT):
    trace_path = Path(trace_path).resolve()
    base = trace_path.parent
    trace = json.loads(trace_path.read_text(encoding='utf-8'))
    registry = json.loads((root / 'references/core-contracts.json').read_text(encoding='utf-8'))
    errors = []
    scores = {}
    route = trace.get('routed_core', [])
    calls = trace.get('calls', [])
    if not route or {c.get('skill') for c in calls} != set(route) or len(calls) != len(set(route)):
        errors.append('each routed core requires exactly one workflow call')
    for call in calls:
        name = call.get('skill')
        contract = registry.get(name)
        if not contract:
            errors.append('not an integrated core: ' + str(name))
            continue
        obligations = contract['obligations']
        records = call.get('obligations', {})
        valid = []
        for obligation in obligations:
            record = records.get(obligation, {})
            proofs = record.get('evidence', [])
            okay = bool(record.get('observation') and proofs)
            for proof in proofs:
                path = (base / proof.get('path', '')).resolve()
                if not path.is_relative_to(base) or not path.is_file() or proof.get('sha256') != evidence.sha256(path):
                    okay = False
            if okay:
                valid.append(obligation)
            else:
                errors.append(name + ': missing/changed evidence for ' + obligation)
        loaded = call.get('loaded_resources', [])
        if contract['entry'] not in loaded:
            errors.append(name + ': original entry not loaded')
        for resource in loaded:
            path = (root / resource).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                errors.append(name + ': invalid loaded resource')
        outputs = call.get('outputs', [])
        if not outputs:
            errors.append(name + ': no final consumer')
        for output in outputs:
            path = (Path(export) / output.get('path', '')).resolve()
            consumer = (Path(export) / output.get('consumer', '')).resolve()
            if not path.is_relative_to(Path(export).resolve()) or not path.is_file() or output.get('sha256') != evidence.sha256(path):
                errors.append(name + ': output missing/changed')
            if not consumer.is_relative_to(Path(export).resolve()) or not consumer.is_file():
                errors.append(name + ': consumer missing')
            elif path != consumer and output.get('link') not in consumer.read_text(encoding='utf-8'):
                errors.append(name + ': output not consumed')
        scores[name] = {'covered': len(valid), 'total': len(obligations), 'observable_coverage': round(100 * len(valid) / len(obligations), 1)}
    return {'kind': 'skill-fidelity', 'status': 'FAIL' if errors else 'PASS', 'export_digest': evidence.tree_digest(export),
            'trace_sha256': evidence.sha256(trace_path), 'scores': scores, 'errors': errors,
            'limits': 'Checks content-bound observable obligations; semantic fidelity requires independent review of artifacts and source contract.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace', type=Path)
    parser.add_argument('export', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = validate(args.trace, args.export)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output_parent=args.output.resolve().parent
        if not args.trace.resolve().is_relative_to(output_parent):
            raise ValueError('trace must be beneath receipt directory')
        result['trace_path']=args.trace.resolve().relative_to(output_parent).as_posix()
        text=json.dumps(result,ensure_ascii=False,indent=2)
        args.output.write_text(text, encoding='utf-8')
    print(text)
    return result['status'] != 'PASS'

if __name__ == '__main__':
    sys.exit(main())
