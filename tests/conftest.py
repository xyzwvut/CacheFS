#!/usr/bin/env python2.7

from __future__ import print_function

import pytest
import sys
import os


def a_dir(path):
    """Check if a given path is a r/w-able directory"""
    if not os.path.isdir(path):
        raise Exception("Not a valid directory {}".format(path))
    if (os.path.isdir(path) and
        os.access(path, os.F_OK or os.W_OK or os.R_OK)):
        return path
    else:
        raise Exception("No RW rights on directory {}".format(path))

def pytest_addoption(parser):
    """py.test support for command line options"""
    parser.addoption('--front-dir', type=a_dir, default=None,
                     help='frontend directory')
    parser.addoption('--backing-dir', type=a_dir, default=None,
                     help='backing directory')
    parser.addoption('--cache-dir', type=a_dir, default=None,
                     help='cache directory')

