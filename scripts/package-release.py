"""Package a verified local Skill export using the product's own archive gate."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--policy',type=Path,required=True)
    parser.add_argument('--comprehension-receipt',type=Path,required=True)
    parser.add_argument('--fidelity-receipt',type=Path,required=True)
    parser.add_argument('--fresh-clone-receipt',type=Path,required=True)
    parser.add_argument('--self-dogfood-receipt',type=Path,required=True)
    args=parser.parse_args()
    if not (args.export/'SKILL.md').is_file():
        parser.error('Skill export must include SKILL.md')
    spec=importlib.util.spec_from_file_location('archive_package',ROOT/'scripts/package-project.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    result=module.package(args.export.resolve(),args.output,json.loads(args.policy.read_text(encoding='utf-8')),
        args.comprehension_receipt,args.fidelity_receipt,args.fresh_clone_receipt,args.self_dogfood_receipt,True)
    print(json.dumps(result))
    return 0

if __name__=='__main__':
    sys.exit(main())
