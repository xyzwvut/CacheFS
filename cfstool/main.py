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


def command_status(args):
    """Get status information"""
    pass


def command_flush(args):
    """Flush cache back onto the server"""
    print args
    pass


def command_pin(args):
    """Pin file/directory into the cache"""
    print args
    pass


def parse_cmdline(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbosity', action='count',
                        help='increase verbosity of debug output')
    parser.add_argument('-p', '--port', type=int, default=5555,
                        help='server port number (default: 5555)')

    subparsers = parser.add_subparsers()

    parser_status = subparsers.add_parser('status')
    parser_status.set_defaults(func=command_status)

    parser_flush = subparsers.add_parser('flush')
    parser_flush.set_defaults(func=command_flush, all=False, recursive=False)
    parser_flush.add_argument('path', help='path to file/directory to flush')
    parser_flush.add_argument('-a', '--all', dest='all', action='store_true',
                              help='include everything')
    parser_flush.add_argument('-r', '--recursive', dest='recursive',
                              action='store_true',
                              help='include subdirectories')

    parser_pin = subparsers.add_parser('pin')
    parser_pin.set_defaults(func=command_pin, recursive=False)
    parser_pin.add_argument('path', help='path to file/directory to pin')
    parser_pin.add_argument('-r', '--recursive', dest='recursive',
                            action='store_true',
                            help='include subdirectories')

    args = parser.parse_args(argv)
    return args


def main(argv):
    args = parse_cmdline(argv)

    if args.func:
        args.func(args)

if __name__ == '__main__':
    main(sys.argv[1:])
