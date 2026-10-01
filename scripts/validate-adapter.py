"""Validate a project adapter; never execute its commands."""
import argparse
import json
from pathlib import Path
import re
import sys

def load(path):
    text = path.read_text(encoding='utf-8')
    if path.suffix == '.json':
        return json.loads(text)
    match = re.search(r'```yaml\s*\n(.*?)\n```', text, re.S)
    if not match:
        raise ValueError('Markdown adapter must contain a YAML block')
    try:
        import yaml
    except ImportError:
        raise ValueError('YAML adapters require PyYAML; JSON adapters need only stdlib')
    return yaml.safe_load(match.group(1))

def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ['adapter must be an object']
    required = ['project_roots','facts_source','public_narrative','architecture_spec','workflow_spec','metrics','demo_scenario','publication_policy','domain_profiles','run_ledger']
    errors.extend('missing ' + key for key in required if key not in data)
    roots = data.get('project_roots')
    if not isinstance(roots, list) or not roots:
        errors.append('project_roots must be a nonempty list')
        roots = []
    valid_types = {'code','docs','knowledge-base','design','mixed'}
    for root in roots:
        if not isinstance(root, dict) or not isinstance(root.get('path'), str) or not root.get('path') or root.get('root_type') not in valid_types:
            errors.append('invalid project root')
    policy = data.get('publication_policy', {})
    if not isinstance(policy, dict) or policy.get('authorization') not in {'NOT_AUTHORIZED','APPROVED'}:
        errors.append('publication authorization must be explicit')
    source = data.get('source_release', {})
    code = any(isinstance(r,dict) and r.get('root_type') in {'code','mixed'} for r in roots)
    if code:
        if not isinstance(source, dict):
            return errors + ['source_release must be an object']
        if source.get('include_code') is not True:
            errors.append('code/mixed projects require include_code=true')
        for key in ['entry_points','excluded']:
            if not isinstance(source.get(key), list) or not source.get(key):
                errors.append('source_release requires nonempty ' + key)
        for entry in source.get('entry_points', []):
            if not isinstance(entry,str) or entry.startswith(('/', '\\')) or '..' in Path(entry).parts or re.match(r'^[A-Za-z]:',entry):
                errors.append('entry_points must use safe project-relative paths')
        verify = source.get('fresh_clone_verify', {})
        if not isinstance(verify,dict):
            return errors + ['fresh_clone_verify must be an object']
        for key in ['runtime_deps_cmd','run_cmd','check_cmd']:
            if not isinstance(verify.get(key), str) or not verify[key].strip():
                errors.append('fresh_clone_verify requires ' + key)
        if not isinstance(verify.get('verification_deps_cmd'),str):
            errors.append('verification_deps_cmd must be explicit (empty only if no extra dependencies)')
        if 'deps_cmd' in verify:
            errors.append('legacy deps_cmd is ambiguous; split runtime and verification dependencies')
        if not isinstance(verify.get('setup_steps',[]),list):
            errors.append('setup_steps must be a list')
    metrics = data.get('metrics', [])
    if not isinstance(metrics,list):
        errors.append('metrics must be a list')
    else:
        for metric in metrics:
            if not isinstance(metric,dict) or any(k not in metric for k in ['label','value','evidence','as_of']) or not metric.get('evidence'):
                errors.append('every metric requires evidence and as_of')
    return errors

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('adapter', type=Path)
    args=parser.parse_args()
    try:
        errors=validate(load(args.adapter))
    except (ValueError,OSError) as exc:
        errors=[str(exc)]
    print(json.dumps({'status':'FAIL' if errors else 'PASS','errors':errors}, ensure_ascii=False))
    return bool(errors)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
