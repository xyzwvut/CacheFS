#!/usr/bin/env python

# Tests for the 'humanfriendly' module.
#
# Author: Peter Odding <peter.odding@paylogic.eu>
# Last Change: June 27, 2013
# URL: https://humanfriendly.readthedocs.org

# Standard library modules.
import math
import os
import pytest

# The module we are testing.
import contrib.humanfriendly as humanfriendly

class TestHumanFriendly():

    def test_format_timespan(self):
        minute = 60
        hour = minute * 60
        day = hour * 24
        week = day * 7
        year = week * 52
        assert '0 seconds' == humanfriendly.format_timespan(0)
        assert '0.54 seconds' == humanfriendly.format_timespan(0.54321)
        assert '1 second' == humanfriendly.format_timespan(1)
        assert '3.14 seconds' == humanfriendly.format_timespan(math.pi)
        assert '1 minute' == humanfriendly.format_timespan(minute)
        assert '1 minute and 20 seconds' == humanfriendly.format_timespan(80)
        assert '2 minutes'== humanfriendly.format_timespan(minute * 2)
        assert '1 hour' == humanfriendly.format_timespan(hour)
        assert '2 hours' == humanfriendly.format_timespan(hour * 2)
        assert '1 day' == humanfriendly.format_timespan(day)
        assert '2 days' == humanfriendly.format_timespan(day * 2)
        assert '1 week' == humanfriendly.format_timespan(week)
        assert '2 weeks' == humanfriendly.format_timespan(week * 2)
        assert '1 year' == humanfriendly.format_timespan(year)
        assert '2 years' == humanfriendly.format_timespan(year * 2)
        assert '1 year, 2 weeks and 3 days' == humanfriendly.format_timespan(year + week * 2 + day * 3 + hour * 12)

    def test_parse_date(self):
        assert (2013, 6, 17, 0, 0, 0) == humanfriendly.parse_date('2013-06-17')
        assert (2013, 6, 17, 2, 47, 42) == humanfriendly.parse_date('2013-06-17 02:47:42')
        try:
            humanfriendly.parse_date('2013-06-XY')
            assert False
        except Exception as e:
            assert isinstance(e, humanfriendly.InvalidDate)

    def test_format_size(self):
        assert '0 bytes' == humanfriendly.format_size(0)
        assert '1 byte' == humanfriendly.format_size(1)
        assert '42 bytes' == humanfriendly.format_size(42)
        assert '1 KB' == humanfriendly.format_size(1024 ** 1)
        assert '1 MB' == humanfriendly.format_size(1024 ** 2)
        assert '1 GB' == humanfriendly.format_size(1024 ** 3)
        assert '1 TB' == humanfriendly.format_size(1024 ** 4)
        assert '1 PB' == humanfriendly.format_size(1024 ** 5)

    def test_parse_size(self):
        assert 42 == humanfriendly.parse_size('42')
        assert 1024 == humanfriendly.parse_size('1k')
        assert 1024 == humanfriendly.parse_size('1 KB')
        assert 1024 == humanfriendly.parse_size('1 kilobyte')
        assert 1024 ** 3 == humanfriendly.parse_size('1 GB')
        try:
            humanfriendly.parse_size('1z')
            assert False
        except Exception as e:
            assert isinstance(e, humanfriendly.InvalidSize)

    def test_round_number(self):
        assert '1' == humanfriendly.round_number(1)
        assert '1' == humanfriendly.round_number(1.0)
        assert '1.00' == humanfriendly.round_number(1, keep_width=True)
        assert '3.14' == humanfriendly.round_number(3.141592653589793)

    def test_format_path(self):
        abspath = os.path.join(os.environ['HOME'], '.vimrc')
        assert os.path.join('~', '.vimrc') == humanfriendly.format_path(abspath)

