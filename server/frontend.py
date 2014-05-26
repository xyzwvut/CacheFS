import os
import sys
import errno
import threading

from contrib.fusepy.fuse import FUSE, FuseOSError, Operations

class MockCache:
    def __init__(self, directory):
        self.root = directory
        print('MockCache at {}'.format(self.root))

    def lookup(self, partial):
        """ Lookup file and return reference """
        if partial.startswith('/'):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        #print('MockCache:lookup: {} as {}'.format(partial, path))
        return path

    def pin(self, partial):
        """ Lock file into cache """
        # TODO: increase refcount
        return lookup(partial)

    def unpin(self, partial):
        # TODO: decrease refcount
        return

    def flush(self, partial):
        # TODO: push file to server
        return

    def lsdir(self, partial):
        dirents = ['.', '..']
        local = self.lookup(partial)
        if os.path.isdir(local):
            dirents.extend(os.listdir(local))
        return dirents


class Frontend(Operations):
    def __init__(self, cache):
        self.cache = cache

    # Filesystem methods
    # ==================

    # path is the partial path from the mountpoint

    def access(self, path, mode):
        print("fuse: op: access, path: '{}', mode '{}'".format(path, mode))
        local_path = self.cache.lookup(path)
        if not os.access(local_path, mode):
            raise FuseOSError(errno.EACCES)
        return

    def chmod(self, path, mode):
        print("fuse: op: chmod, path: '{}', mode '{}'".format(path, mode))
        raise SystemExit('Exception')
        pass

    def chown(self, path, uid, gid):
        print("fuse: op: chown, path: '{}', uid: '{}' gid: '{}'".format(path, uid, gid))
        raise SystemExit('Exception')
        pass

    def getattr(self, path, fh=None):
        print("fuse: op: getattr, path: '{}'".format(path))

        local_path = self.cache.lookup(path)
        st = os.lstat(local_path)
        d = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        return d

    def readdir(self, path, fh):
        print("fuse: op: readdir, path: '{}'".format(path))
        dirents = self.cache.lsdir(path)
        for r in dirents:
            yield r

    def readlink(self, path):
        print("fuse: op: readlink, path: '{}'".format(path))
        #pathname = os.readlink(self._full_path(path))
        raise SystemExit('Exception')
        pass
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        print("fuse: op: mknod, path: '{}', mode: '{}', dev: '{}'".format(path, mode, dev))
        raise SystemExit('Exception')
        pass
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        print("fuse: op: rmdir, path: '{}'".format(path))
        raise SystemExit('Exception')
        pass
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        print("fuse: op: rkdir, path: '{}', mode '{}'".format(path, mode))
        raise SystemExit('Exception')
        pass
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        # TODO: Is this called with another path than the mountpoint?
        local = self.cache.lookup(path)
        if not path == '/':
            print("fuse: op: statfs, path: '{}'".format(path))
            print('Full_path: {}'.format(local))

        stv = os.statvfs(local)
        d = dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

        if not path == '/':
            print(d)
        return d

    def unlink(self, path):
        print("fuse: op: unlink, path: '{}'".format(path))
        raise SystemExit('Exception')
        pass
        return os.unlink(self._full_path(path))

    def symlink(self, target, name):
        print("fuse: op: symlink, target: '{}', name: '{}'".format(target, name))
        raise SystemExit('Exception')
        pass
        return os.symlink(self._full_path(target), self._full_path(name))

    def rename(self, old, new):
        print("fuse: op: rename, old: '{}', new: '{}'".format(old, new))
        raise SystemExit('Exception')
        pass
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        print("fuse: op: link, target: '{}', name: '{}'".format(target, name))
        raise SystemExit('Exception')
        pass
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        print("fuse: op: utimes, path: '{}', times: '{}'".format(path, times))
        #return os.utime(self._full_path(path), times)
        raise SystemExit('Exception')
        pass

    # File methods
    # ============

    def open(self, path, flags):
        print("fuse: op: open, path: '{}', flags: '{}'".format(path, flags))
        local = self.cache.pin(path)
        return os.open(local, flags)

    def create(self, path, mode, fi=None):
        print("fuse: op: create, path: '{}', mode: '{}'".format(path, mode))
        #full_path = self._full_path(path)
        #return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)
        raise Exception('Exception')
        pass

    def read(self, path, length, offset, fh):
        print("fuse: op: read, path: '{}', len: '{}', offset: '{}'".format(path, length, offset))
        #os.lseek(fh, offset, os.SEEK_SET)
        #return os.read(fh, length)
        raise Exception('Exception')
        pass

    def write(self, path, buf, offset, fh):
        print("fuse: op: write, path: '{}', offset: '{}'".format(path, offset))
        #os.lseek(fh, offset, os.SEEK_SET)
        #return os.write(fh, buf)
        raise Exception('Exception')
        pass

    def truncate(self, path, length, fh=None):
        print("fuse: op: truncate, path: '{}', length: '{}'".format(path, length))
        local = self.cache.pin(path)
        with open(local, 'r+') as f:
            f.truncate(length)
        self.cache.flush(path)
        self.cache.unpin(path)
        raise Exception('Exception')
        pass

    def flush(self, path, fh):
        print("fuse: op: flush, path: '{}'".format(path))
        os.fsync(fh)
        self.cache.flush(path)
        return

    def release(self, path, fh):
        print("fuse: op: release, path: '{}'".format(path))
        # TODO: Dereference open counter
        os.close(fh)
        self.cache.unpin(path)
        return

    def fsync(self, path, fdatasync, fh):
        print("fuse: op: fsync, path: '{}'".format(path))
        self.cache.flush(path)
        pass

def main(front_dir, back_dir):
    front_dir = os.path.expanduser(front_dir)
    back_dir = os.path.expanduser(back_dir)

    cache = MockCache(back_dir)
    FUSE(Frontend(cache), front_dir, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1] )
