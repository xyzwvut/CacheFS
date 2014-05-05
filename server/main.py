#!/usr/bin/env python2.7

import argparse
import sys
import os

def accessible_directory(path):
    """Check if given path is an readable and writable directory"""
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("{0} is not a valid directory".format(path))
    if os.access(path, os.R_OK | os.W_OK):
        return path
    else:
        raise argparse.ArgumentTypeError("{0} is not a accessible".format(path))


def parse_cmdline(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbosity', action='count',
                        help='increase verbosity of debug output')
    parser.add_argument('-p', '--port', type=int, default=5555,
                        help='port number (default: 5555)')
    parser.add_argument('front-dir', type=accessible_directory,
                        help='frontend directory')
    parser.add_argument('backend-dir', type=accessible_directory,
                        help='backend directory')

    args = parser.parse_args(argv)
    return args

def main(argv):
    args = parse_cmdline(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
