import os

from contrib.humanfriendly import parse_size, format_size


class File:
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name
        self.size = None
        print('File({}, {})'.format(directory.pathname(), name))

    def pathname(self):
        return os.sep.join(self.directory.pathname(), self.name)


class Directory:
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.entries = {}
        self.log()
        pass

    def log(self):
        if self.parent is None:
            path = '-'
        else:
            path = self.parent.pathname()
        print('Dir({}, {})'.format(path, self.name))

    def pathname(self):
        """ Walk all directoris up """
        if self.parent is None:
            return self.name
        else:
            return os.path.join(self.parent.pathname(), self.name)

    def add_entry(self, new_entry):
        self.entries[new_entry.name] = new_entry

    def find(self, name):
        return self.entries.get(name, None)


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


def split_path(pathname):
    """ Split pathname into directories and filename """
    directories = []
    path = pathname
    print("path {}".format(path))

    while True:
        path, folder = os.path.split(path)

        if folder != "":
            directories.append(folder)
        else:
            if path != "":
                directories.append(path)
            break

    directories.reverse()
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
        self.root = Directory(None, 'root')

        self.load_tree()
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

    def load_tree(self):
        """ Load the tree of available files """

        # We have the full pathname in the listing
        results = self.backend.ls('.', recursive=True)

        for result in results:
            print("--------------------------------")
            print(result['raw'])
            path = split_path(result['name'])
            print(path)

            # Why is this not necessary anymore?
            # if path[-1] == '.':
            #    continue

            if result['type'] == 'file':
                e = self.root
                parent = self.root
                # Last element is the file
                for dirname in path[:-1]:
                    e = parent.find(dirname)
                    if e is None:
                        e = Directory(parent, dirname)
                        parent.add_entry(e)
                        parent = e
                # TODO: Assert walk successful
                f = e.find(path[-1])
                if f is None:
                    # File not known, create
                    f = File(e, path[-1])
                    e.add_entry(f)
        
            elif result['type'] == 'dir':
                e = self.directory
                parent = self.directory
                for dirname in path:
                    e = parent.find(dirname)
                    if e is None:
                        e = Directory(parent, dirname)
                        parent.add_entry(d)
                        parent = d
                # TODO: Assert walk successful
            else:
                assert False, 'Unknown ls entry type'
        pass

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
