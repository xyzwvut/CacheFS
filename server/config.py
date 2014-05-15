import os
import configparser

config = configparser.ConfigParser()


def load_config(config_path):
    """ Load configuration specified on the commandline """

    # While under development update the defaults.cfg
    update_default_config()

    # Required defaults are read first.
    config.readfp(open('defaults.cfg'))

    config.readfp(config_path)


def update_default_config():
    """ Update default config file """

    config = configparser.RawConfigParser()
    config.add_section('main')
    config.set('main', 'port', '55555')
    config.set('main', 'console', 'True')

    config.add_section('front')
    config.set('front', 'dir', 'path')

    config.add_section('cache')
    config.set('cache', 'dir', 'path')
    config.set('cache', 'size', '200MB')

    config.add_section('back')
    config.set('back', 'protocol', 'rsync')
    config.set('back', 'user', 'username')
    config.set('back', 'host', 'server-ip')
    config.set('back', 'dir', 'path')

    with open('defaults.cfg', 'w') as configfile:
        config.write(configfile)
