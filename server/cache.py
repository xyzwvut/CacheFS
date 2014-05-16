import os

import humanfriendly

class File:
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name

    def pathname():
        return os.sep.join(self.directory.pathname(), self.name)



class Directory:
    def __init__(self, parent, name):
        self.name = name
        pass

    def full_pathname():
        """ Walk all directories up and concatenate them """
        pass



class Cache:
    """
     Cache keeps track what's in the frontend
    """
    def __init__(self, config, backend):
        # Sanitize
        directory = os.path.expanduser(config['dir'])
        #size = humanfriendly.parse_size(config['size'])
        self.size_allowed = config['size']

        if not os.access(directory, os.R_OK | os.W_OK):
            raise Exception('Can not access Cache directory {}'.format(directory))

        self.backend = backend
        self.directory = directory
        self.initialize_stats()
        pass

    def initialize_stats(self):
        total_size = 0
        total_files = 0
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
            total_files += len(filenames)
        self.size = total_size
        self.files = total_files

    def status(self):
        s = { 'size': self.size,
              'allowed_size': self.size_allowed,
              'files': self.files, }
        return s

    def lls(self, pathname, recursive):
        assert recursive == False, 'Recursive listing not supported'
        print('Cache: lls {}'.format(pathname))
        pass

    def rls(self, pathname, recursive):
        assert recursive == False, 'Recursive listing not supported'
        print('Cache: rls {}'.format(pathname))
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

