#!/usr/bin/env python3

import argparse
import os
import subprocess

SCRIPTS_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(SCRIPTS_DIR, os.pardir, 'config')


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('query_jsons', nargs='*',
                        help='json5 files containing query specifications')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbose output, may be use more than once')
    args = parser.parse_args()

    if args.verbose:
        print('Getting latest Johns Hopkins data.')
    subprocess.run([os.path.join(SCRIPTS_DIR, 'get_jh_data.py')])

    if args.verbose:
        print('Updating databases.')
    for query_json in args.query_jsons:
        if args.verbose:
            print(query_json)
        command = [os.path.join(SCRIPTS_DIR, 'query_jh.py'),
                   '--query', os.path.join(CONFIG_DIR, query_json)]
        for _ in range(args.verbose):
            command.extend(['-v'])
        subprocess.run(command)


if __name__ == '__main__':
    main()
