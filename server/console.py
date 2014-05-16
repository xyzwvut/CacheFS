import argparse
import cmd

class CacheFSConsole(cmd.Cmd):
    intro = 'CacheFS console. Type help or ? to list commands\n'
    prompt = 'cachefs: $ '

    def __init__(self, cache):
        cmd.Cmd.__init__(self)
        self.cache = cache

    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt as e:
            print('')
            # Resume command loop
            # self.cmdloop()
            return True

    def do_exit(self, arg):
        """ Quit the server """
        print('Ending server')
        return True

    def do_status(self, arg):
        """ Print status information """
        print('Status')
        s = self.cache.status()
        print('files: {files}'.format(**s))
        print('size : {size}/{allowed_size}'.format(**s))
        pass

    def do_lls(self, arg):
        """
            Local list directroy contents
            -r --recursive
            [path]
        """
        print('lls: arg {}'.format(arg))
        parser = argparse.ArgumentParser(prog='lls')
        parser.set_defaults(recursive=False)
        parser.add_argument('path', help='path to local file/directory to show')
        parser.add_argument('-r', '--recursive', dest='recursive',
                            action='store_true',
                            help='include subdirectories')
        try:
            args = parser.parse_args(arg.split())
        except SystemExit:
            return False

        self.cache.lls(args.path, args.recursive)
        pass

    def do_rls(self, arg):
        """
            Remote list directroy contents
            -r --recursive
            [path]
        """
        print('rls: arg {}'.format(arg))
        parser = argparse.ArgumentParser(prog='rls')
        parser.set_defaults(recursive=False)
        parser.add_argument('path', help='path to remote file/directory to show')
        parser.add_argument('-r', '--recursive', dest='recursive',
                            action='store_true',
                            help='include subdirectories')
        try:
            args = parser.parse_args(arg.split())
        except SystemExit:
            return False

        self.cache.rls(args.path, args.recursive)
        pass

    def do_fetch(self, arg):
        """ -a --all
            -r --recursive
            [path] [directory]
        """
        print('Fetch: arg {}'.format(arg))
        parser = argparse.ArgumentParser(prog='fetch')
        parser.set_defaults(all=False, recursive=False)
        parser.add_argument('path', help='path to file/directory to flush')
        parser.add_argument('-a', '--all', dest='all', action='store_true',
                            help='include everything')
        parser.add_argument('-r', '--recursive', dest='recursive',
                            action='store_true',
                            help='include subdirectories')

        try:
            args = parser.parse_args(arg.split())
        except SystemExit:
            return False

        self.cache.fetch(args.path, args.all, args.recursive)
        pass

    def do_flush(self, arg):
        """ -a --all
            -r --recursive
            [path] [directory]
        """
        print('Flush: arg {}'.format(arg))
        parser = argparse.ArgumentParser(prog='flush')
        parser.set_defaults(all=False, recursive=False)
        parser.add_argument('path', help='path to file/directory to flush')
        parser.add_argument('-a', '--all', dest='all', action='store_true',
                            help='include everything')
        parser.add_argument('-r', '--recursive', dest='recursive',
                            action='store_true',
                            help='include subdirectories')

        try:
            args = parser.parse_args(arg)
        except SystemExit:
            return False

        # self.cache.flush(args.path, args.all, args.recursive)
        pass

    def do_pin(self, arg):
        """ -a --all
            -r --recursive
            [path] [directory]
        """
        print('Pin: arg {}'.format(arg))
        parser = argparse.ArgumentParser()
        parser.set_defaults(all=False, recursive=False)
        parser.add_argument('path', help='path to file/directory to flush')
        parser.add_argument('-a', '--all', dest='all', action='store_true',
                            help='include everything')
        parser.add_argument('-r', '--recursive', dest='recursive',
                            action='store_true',
                            help='include subdirectories')

        try:
            args = parser.parse_args(arg)
        except SystemExit:
            return False

        # Fetch
        # self.cache.pin(args.path, args.all, args.recursive)
        pass

