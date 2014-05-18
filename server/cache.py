import os

from contrib.humanfriendly import parse_size, format_size


class File:
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name
        self.size = None

    def pathname(self):
        return os.sep.join(self.directory.pathname(), self.name)


class Directory:
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.entries = {}
        pass

    def pathname(self):
        """ Walk all directoris up """
        return os.path.join(self.parent.rel_pathname, name)

    def add_entry(self, new_entry):
        self.entries[new_entry.name] = new_entry

    def find(self, name):
        self.entries.get(name, None)


def get_tree_stats(directory):
    """ Walk a directory tree and collect stats """
    total_size = 0
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
        total_files += len(filenames)
    return total_files, total_size


def split_path(self, pathname):
    """ Split pathname into directories and filename """
    directories = []
    path = pathname

    while True:
        (path, last) = os.path.split(path)
        if path is None:
            break
        directories.insert(0, last)
    return directories


class Cache:
    """
     Cache keeps track what's in the frontend
    """
    def __init__(self, config, backend):
        # Sanitize
        directory = os.path.expanduser(config['dir'])
        self.size_allowed = parse_size(config['size'])

        if not os.access(directory, os.R_OK | os.W_OK):
            raise Exception('Can not access Cache directory {}'.format(directory))

        self.backend = backend
        self.directory = directory
        self.files, self.size = get_tree_stats(self.directory)
        pass

    def update_stats(self):
        self.files, self.total_size = get_tree_stats(self.directory)
        pass

    def status(self):
        self.update_stats()
        s = {'size': self.size,
             'allowed_size': format_size(self.size_allowed),
             'files': self.files}
        return s

    def lls(self, pathname, recursive):
        assert not recursive, 'Recursive listing not supported'
        print('Cache: lls {}'.format(pathname))
        pass

    def rls(self, pathname, recursive):
        print('Cache: rls {}'.format(pathname))
        result = self.backend.ls(pathname, recursive)
        # Update tree
        # self.update_tree(pathname, recursive, result)
        pass

    def fetch(self, pathname, all, recursive):
        print('Cache: lookup {}'.format(pathname))
        self.backend.get(pathname)
        pass

    def pin(self, pathname):
        print('Cache: pin {}'.format(pathname))
        pass

    def unpin(self, pathname):
        print('Cache: unpin {}'.format(pathname))

        if not lookup(pathname):
            return
        pass

    def flush(self):
        print('Cache: flush')
        pass

    def shutdown(self):
        print('Cache: shutdown')
        pass
