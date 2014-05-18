import os
import re
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


def parse_ls_line(line):
    """ Parse output printet by rsync list directory
        '-rw-r--r--           0 2014/05/10 19:38:43 a'
    """
    result = re.match(r'(.)(.{3})(.{3})(.{3})\s(.*) (.+)/(.+)/(.+) (.+):(.+):(.+) (.*)$', line)
    if result:
        desc = {}
        if result.group(1) == '-':
            desc['type'] = 'file'
        elif result.group(1) == 'd':
            desc['type'] = 'dir'
        else:
            raise Exception('Unkown line in ls rsync output')

        desc['perm_u'] = result.group(2)
        desc['perm_g'] = result.group(3)
        desc['perm_o'] = result.group(4)
        desc['size']   = int(result.group(5))
        desc['year']   = int(result.group(6))
        desc['month']  = int(result.group(7))
        desc['day']    = int(result.group(8))
        desc['hour']   = int(result.group(9))
        desc['min']    = int(result.group(10))
        desc['sec']    = int(result.group(11))
        desc['name']   = result.group(12)
        return desc
    else:
        return None



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
        out = subprocess.check_output(cmd)
        print(out)

    def push(self, pathname):
        cmd = [ self.rsync, self.args, self.local_path(pathname),
                self.server_path(pathname) ]
        print("push: '{}'".format(' '.join(cmd)))

    def parse_ls_output(self, out):
        """ Parse output producesd by rysnc list-only """
        result = []
        for line in out.decode('utf-8').splitlines():
            # print(line)
            desc = parse_ls_line(line)
            if desc:
                result.append(desc)
        return result

    def ls(self, pathname, recursive):
        """ List directory contents """
        cmd = [self.rsync, '--list-only']
        if recursive:
            cmd.append('-r')
        cmd.append(self.server_path(pathname))

        out = subprocess.check_output(cmd)

        return self.parse_ls_output(out)


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
