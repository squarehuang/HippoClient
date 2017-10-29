# -*- coding: utf-8 -*-

from __future__ import print_function
import click
import ConfigParser
from common import const
from utils import common_util
from controller.remove_cmd import RemoveCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


default_api_host = common_util.get_conf('HippoManagerAPI', 'host')
default_api_port = common_util.get_conf('HippoManagerAPI', 'port')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--id', help='hippo id', required=True)
@click.option('-f', '--force', is_flag=True, help='force stop and deregister if service is running')
@click.option('-d', '--del_service', is_flag=True, help='delete service plugin from project')
@click.option('--api_host', default=default_api_host, help='hippo manager api host, Default: {}'.format(default_api_host))
@click.option('--api_port', default=default_api_port, help='hippo manager api port, Default: {}'.format(default_api_port))
def remove(id, force, del_service, api_host, api_port):

    api_url = '{}:{}'.format(api_host, api_port)
    cmd = RemoveCommand(api_url)
    cmd.execute(id=id, force=force, del_service=del_service)


if __name__ == '__main__':
    remove()
