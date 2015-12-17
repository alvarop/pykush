#!python
''' Python interface for Yepkit's USB Switched Hub

    Currently tested and working on Ubuntu.

    Usage: pykush.py -d <1,2,3,a> to disable ports
           pykush.py -u <1,2,3,a> to enable ports
'''

import pykush
import argparse


def main():
    ports = ['1', '2', '3', 'a']

    parser = argparse.ArgumentParser()

    parser.add_argument('-u', choices=ports, help='Port to turn on.')
    parser.add_argument('-d', choices=ports, help='Port to turn off')

    args, unknown = parser.parse_known_args()

    if args.u or args.d:
        ykush = pykush.PYKUSH()
        if args.u:
            if args.u == 'a':
                ykush.enable_all()
            else:
                ykush.enable(int(args.u))

        if args.d:
            if args.d == 'a':
                ykush.disable_all()
            else:
                ykush.disable(int(args.d))
    else:
        print('Usage: pykush.py -d <1,2,3,a> to disable ports')
        print('       pykush.py -u <1,2,3,a> to enable ports')


if __name__ == '__main__':
    main()
