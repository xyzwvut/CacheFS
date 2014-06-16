import pytest
import random
import string
import os
import stat
import shutil

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

    def remove_file(self, pathname):
        """Remove pathname from directory"""
        # TODO: Make sure pathname has pefix of directory
        assert(pathname.startswith(self.directory))
        self.names.remove(pathname)

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
        assert(os.path.exists(pathname))

    def test_create_x_file(self):
        """Create executable file"""
        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        assert(os.path.exists(pathname))

    def test_delete_file(self):
        """Create a file, delete it"""
        pathname = self.directory.get_file()
        open(pathname, 'w').close()
        assert(os.path.exists(pathname))
        os.remove(pathname)
        assert(not os.path.exists(pathname))
        self.directory.remove_file(pathname)

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

    def test_remove_files(self):
        for pathname in self.directory.names:
            os.remove(pathname)
            assert(not os.path.exists(pathname))

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


    def copy_file(self, size):
        src = self.directory.get_file()
        dst = self.directory.get_file()
        s = os.urandom(size * 8)
        r = None
        with open(src, 'wb') as f:
            f.write(s)
        shutil.copy2(src, dst)
        with open(dst, 'rb') as f:
            r = f.read()

        assert(s == r)

    def test_copy_file_100bytes(self):
        self.copy_file(100)

    def test_copy_file_1kb(self):
        self.copy_file(1024)

    def test_copy_file_1mb(self):
        self.copy_file(1024 * 1024)



class TestMultipleFiles():
    pass

class TestDirectory():
    pass

class TestMultipleDirectories():
    pass

