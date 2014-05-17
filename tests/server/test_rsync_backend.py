import pytest

from server.backend import parse_ls_line

def test_parse_ls_file():
    line = '-rw-r--r--           0 2014/05/10 19:38:43 a'
    desc = parse_ls_line(line)

    assert(desc['type'] == 'file')
    assert(desc['perm_u'] == 'rw-')
    assert(desc['perm_g'] == 'r--')
    assert(desc['perm_o'] == 'r--')
    assert(desc['size'] == 0)
    assert(desc['year'] == 2014)
    assert(desc['month'] == 5)
    assert(desc['day'] == 10)
    assert(desc['hour'] == 19)
    assert(desc['min'] == 38)
    assert(desc['sec'] == 43)
    assert(desc['name'] == 'a')
    pass

def test_parse_ls_dir():
    line = 'drwxrwsrwx        4096 2014/05/17 18:22:14 dir'
    desc = parse_ls_line(line)

    assert(desc['type'] == 'dir')
    assert(desc['perm_u'] == 'rwx')
    assert(desc['perm_g'] == 'rws')
    assert(desc['perm_o'] == 'rwx')
    assert(desc['size'] == 4096)
    assert(desc['year'] == 2014)
    assert(desc['month'] == 5)
    assert(desc['day'] == 17)
    assert(desc['hour'] == 18)
    assert(desc['min'] == 22)
    assert(desc['sec'] == 14)
    assert(desc['name'] == 'dir')
    pass

def test_parse_ls_dirs():
    pass

