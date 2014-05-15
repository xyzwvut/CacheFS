import os

class ScpBackend:
    def __init__(self, local, remote):
        self.local  = local
        self.remote = remote

    def get(self, pathname):
        cmdline = 'scp sb@nas:/{}/{} /{}/{}'.format(self.remote, pathname,
                                                    self.local, pathname)
        os.system(cmdline)

    def push(self, pathname):
        pass


class RsyncBackend:
    """To:
       rsync -av user@nas:/path/file file
       From:
       rsync -av file user@nas:/path/file
    """
    def __init__(self, local, user, host, remote):
        self.user = user
        self.host = host
        self.local = local
        self.remote = remote
        self.args = 'av'
    pass

    def local_path(self, pathname):
        return os.path.join(self.local, pathname)

    def server_path(self, pathname):
        login = '{user}@{host}:'.format(user=self.user, host=self.host)
        return os.path.join(login, self.remote, pathname)

    def cmdline(self, parameters):
        return 'rsync {args} {src} {dst}'.format(**parameters)

    def get(self, pathname):
        parameters = { 'args': self.args,
                       'src': self.server_path(pathname),
                       'dst': self.local_path(pathname) }

        print("get: '{}'".format(self.cmdline(parameters)))

    def push(self, pathname):
        parameters = { 'args': self.args,
                       'src': self.local_path(pathname),
                       'dst': self.server_path(pathname) }

        print("push: '{}'".format(self.cmdline(parameters)))


def create(config, local_dir):
    """ Create backend by config description """
    directory = config['dir']
    protocol = config['protocol']

    if protocol == "rsync":
        remote = config['dir']
        host = config['host']
        user = config['user']
        return RsyncBackend(local_dir, user, host, remote)
    else:
        raise Exception("Unkown backend '{}'".format(protocol))
