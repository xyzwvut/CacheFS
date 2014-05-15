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
        size = humanfriendly.parse_size(config['size'])
        print(size)

        if not os.access(directory, os.R_OK | os.W_OK):
            raise Exception('Can not access Cache directory {}'.format(directory))

        self.size = size
        self.backend = backend
        self.directory = directory
        self.pathnames = {}
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

