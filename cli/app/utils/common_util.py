import os
import ConfigParser
from common import const


def gen_path(folder, file):
    '''
        generate path from app_home
    '''
    cwd = os.path.dirname(os.path.realpath(__file__))
    app_home = os.path.sep.join(cwd.split(os.path.sep)[:-3])
    paths = [app_home, folder]
    path_prefix = os.path.join(*paths)
    path = os.path.join(path_prefix, file)
    return path


def get_conf(section, name):
    #  init config
    config = ConfigParser.ConfigParser()
    path = gen_path(folder='etc', file=const.CONFIG_NAME)
    config.read(path)
    # default_api_host = config.get('HippoManagerAPI', 'host')
    # default_api_port = config.get('HippoManagerAPI', 'port')
    return config.get(section, name)
