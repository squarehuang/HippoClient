import os
import ConfigParser
import socket
from termcolor import colored, cprint

from common import const


def gen_path(folder, file):
    '''
        generate path from app_home
    '''
    cwd = os.path.dirname(os.path.realpath(__file__))
    app_home = os.path.sep.join(cwd.split(os.path.sep)[:-4])
    paths = [app_home, folder]
    path_prefix = os.path.join(*paths)
    path = os.path.join(path_prefix, file)
    return path


def get_conf(section, name):
    #  init config
    config = ConfigParser.ConfigParser()
    path = gen_path(folder='etc', file=const.CONFIG_NAME)
    config.read(path)
    return config.get(section, name)


def get_ip():
    ipaddr = socket.gethostbyname(socket.gethostname())
    return ipaddr


def print_by_file(filepath, color='white'):

    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            cprint('{}'.format(line.strip()), color)
            line = fp.readline()
            cnt += 1


get_ip()
