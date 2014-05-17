import os
import subprocess

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
        self.local = os.path.expanduser(local)
        self.remote = remote
        self.args = '-av'
        self.rsync = '/usr/bin/rsync'
    pass

    def local_path(self, pathname):
        return os.path.join(self.local, pathname)

    def server_path(self, pathname):
        login = '{user}@{host}:'.format(user=self.user, host=self.host)
        return login + os.path.join(os.path.sep, login, self.remote, pathname)

    def get(self, pathname):
        cmd = [ self.rsync, self.args, self.server_path(pathname),
                self.local_path(pathname) ]
        print("get: '{}'".format(' '.join(cmd)))

    def push(self, pathname):
        cmd = [ self.rsync, self.args, self.local_path(pathname),
                self.server_path(pathname) ]
        print("push: '{}'".format(' '.join(cmd)))

    def ls(self, pathname, recursive):
        """ List directory contents """
        assert recursive == False, 'Recurive listing not implemented'

        cmd = [self.rsync, self.server_path(pathname)]
        print("ls: '{}'".format(' '.join(cmd)))

        out = subprocess.check_output(cmd)
        print(out)


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
