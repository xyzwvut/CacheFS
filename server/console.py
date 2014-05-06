import cmd

class CacheFSConsole(cmd.Cmd):
    intro = 'CacheFS console. Type help or ? to list commands\n'
    prompt = 'cachefs: $'

    def do_status(self, arg):
        """ """
        print("Status")
        pass

    def do_flush(self, arg):
        """ -a --all
            -r --recursive
            [path] [directory]
        """
        print("Flush")
        pass

    def do_pin(self, arg):
        """ -a --all
            -r --recursive
            [path] [directory]
        """
        print("Pin")
        pass

