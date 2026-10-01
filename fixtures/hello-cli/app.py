"""A small, dependency-free command line example for export verification."""
import argparse

def greeting(name):
    name=name.strip()
    if not name:
        raise ValueError('name must not be empty')
    return f'Hello, {name}!'

def main():
    parser=argparse.ArgumentParser(description='Print a greeting locally.')
    parser.add_argument('name',nargs='?',default='world')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check:
        print('configuration OK; no external services required')
        return 0
    try:
        print(greeting(args.name))
    except ValueError as error:
        parser.error(str(error))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
