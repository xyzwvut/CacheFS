import pytest
import random
import string
import os
import stat

#
# Module constructed in a way it can be used in pytest
# and started via main.py application.
#
class Volume:
    def __init__(self, pathname):
        self.root = pathname
        self.directory = Directory(self, pathname)


class Directory:
    def __init__(self, volume, directory):
        assert(os.path.exists(directory))
        assert(os.path.isdir(directory))
        self.directory = directory
        self.volume    = volume
        self.len_filename = 8
        self.names = []

    def random_string(self):
        """Get a random string to construct a filename"""
        base_set = string.ascii_uppercase + string.digits
        s = ''.join(random.choice(base_set) for _ in range(self.len_filename))
        return s

    def get_file(self):
        """Get a filename"""
        s = self.random_string()
        pathname = os.path.join(self.directory, s)

        self.names.append(pathname)
        return pathname

    def get_subdir(self):
        """Get a sub-directory"""
        assert(false)


class TestFile():
    """ Test operations on single file"""
    def setup(self):
        self.vol = Volume(pytest.config.getoption('--front-dir'))
        self.directory = self.vol.directory

    def test_create_w_file(self):
        """Create executable file"""
        pathname = self.directory.get_file()
        open(pathname, 'w').close()

    def test_create_x_file(self):
        """Create executable file"""
        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        return pathname

    #
    # Add permission
    #
    def test_mk_u_x_file(self):
        """Make file executable"""
        mode = stat.S_IFREG | stat.S_IXUSR

        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        assert(os.stat(pathname).st_size == 0)

        os.chmod(pathname, mode)
        assert(os.stat(pathname).st_mode == mode)


    def test_mk_u_r_file(self):
        """Make file readbale"""
        mode = stat.S_IFREG | stat.S_IRUSR

        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        assert(os.stat(pathname).st_size == 0)

        os.chmod(pathname, mode)
        assert(os.stat(pathname).st_mode == mode)


    def test_mk_u_w_file(self):
        """Make file writeable"""
        mode = stat.S_IFREG | stat.S_IWUSR

        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        assert(os.stat(pathname).st_size == 0)

        os.chmod(pathname, mode)
        assert(os.stat(pathname).st_mode == mode)


    def test_mk_u_rwx_file(self):
        """Make file writeable"""
        mode = stat.S_IFREG | stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR

        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        assert(os.stat(pathname).st_size == 0)

        os.chmod(pathname, mode)
        assert(os.stat(pathname).st_mode == mode)


    def test_mk_g_rwx_file(self):
        """Make file writeable"""
        mode = stat.S_IFREG | stat.S_IXGRP | stat.S_IWGRP | stat.S_IRGRP

        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        assert(os.stat(pathname).st_size == 0)

        os.chmod(pathname, mode)
        assert(os.stat(pathname).st_mode == mode)

    #
    # Check permissions
    #
    def test_chk_x_file(pathname):
        """Check file executable"""
        pass

    def test_chk_r_file(pathname):
        """Check file readable"""
        pass

    def test_chk_w_file(pathname):
        """Check file writable"""
        pass

    #
    # Write data
    def test_write_file(self):
        pathname = self.directory.get_file()
        s = "Foo"
        with open(pathname, 'w') as f:
            f.write(s)
        assert(os.stat(pathname).st_size == len(s))


    def test_verify_write_file(self):
        pathname = self.directory.get_file()
        s = "Foo"
        r = None
        with open(pathname, 'w') as f:
            f.write(s)
        with open(pathname, 'r') as f:
            r = f.read()

        assert(os.stat(pathname).st_size == len(s))
        assert(s == r)


class TestMultipleFiles():
    pass

class TestDirectory():
    pass

class TestMultipleDirectories():
    pass

