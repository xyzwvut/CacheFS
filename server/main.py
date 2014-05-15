#!/usr/bin/env python3

import argparse
import sys
import os

import config
import backend

from console import CacheFSConsole
from cache import Cache


def accessible_directory(path):
    """ Check if given path is an readable and writable directory """
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("{0} is not a valid directory".format(path))
    if os.access(path, os.R_OK | os.W_OK):
        return path
    else:
        raise argparse.ArgumentTypeError("{0} is not a accessible".format(path))


def parse_cmdline(argv):
    parser = argparse.ArgumentParser()
    parser.set_defaults(show_console=False)
    parser.add_argument('config', type=argparse.FileType('r'),
                        help='path to configfile')
    parser.add_argument('-v', '--verbosity', action='count',
                        help='increase verbosity of debug output')
    parser.add_argument('-p', '--port', type=int, default=None,
                        help='port number (default: 5555)')
    parser.add_argument('-c', '--with-console', dest='show_console',
                        action='store_true',
                        help='Show interactive console')

    args = parser.parse_args(argv)
    return args


def apply_cmdline_overwrites(args):
    """ Update configs with overwrites from commandline """
    if args.port:
        config.config.set('main', 'port', args.port)

    if args.show_console:
        config.config.set('main', 'console', 'True')


def main(argv):
    args = parse_cmdline(argv)

    config.load_config(args.config)

    apply_cmdline_overwrites(args)

    # TODO: Path not expaned used before cache sanity-checked it
    back = backend.create(config.config['back'], config.config['cache']['dir'])
    cache = Cache(config.config['cache'], back)

    if config.config.getboolean('main', 'console'):
        CacheFSConsole(cache).cmdloop()

    cache.shutdown()


if __name__ == '__main__':
    main(sys.argv[1:])
