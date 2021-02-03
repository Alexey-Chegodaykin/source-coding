import time
import argparse

from archivator import Archivator
from dearchivator import Dearchivator


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', type=str, dest='path', help='Path to target file')
    parser.add_argument('-type', type=int, dest='type', help='0 - archivate, 1 - dearchivate')
    parser.add_argument('-fmt', type=str, dest='fmt', required=False, default='.txt', help='Format file of dearchivating')
    args = parser.parse_args()

    if args.type == 0:
        arch = Archivator()
        start = time.time()
        arch.archivate(path_input_file=args.path)
        end = time.time()
        print(f'Runtime of the archivate is {round(end - start, 2)} s.')
    elif args.type == 1:
        dearch = Dearchivator()
        start = time.time()
        dearch.dearchivate(path_input_file=args.path, target_format=args.fmt)
        end = time.time()
        print(f'Runtime of the dearchivate is {round(end - start, 2)} s.')
    else:
        raise Exception('Selected type does not support')
