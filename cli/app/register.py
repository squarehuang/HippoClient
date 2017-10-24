# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import socket
import ConfigParser
from utils import common_util
from controller.register_cmd import RegisterCommand
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


default_api_host = common_util.get_conf('HippoManagerAPI', 'host')
default_api_port = common_util.get_conf('HippoManagerAPI', 'port')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-p', '--project_home', required=True)
@click.option('-s', '--service_name', help='Service name, Default: last directory name from ${project_home}')
@click.option('-c', '--run_cmd', help='command for run service, you can use \"{PROJECT_HOME}\" variable to build command (e.g. "sh {PROJECT_HOME}/bin/message_client.py")')
@click.option('--host', help='Project server host, Default: {}'.format(socket.gethostname()))
@click.option('--api_host', help='hippo manager api host, Default: {}'.format(default_api_host))
@click.option('--api_port', help='hippo manager api port, Default: {}'.format(default_api_port))
def register(host, project_home, service_name, run_cmd, api_host, api_port):
    if api_host is None:
        api_host = default_api_host
    if api_port is None:
        api_port = default_api_port
    api_url = '{}:{}'.format(api_host, api_port)
    cmd = RegisterCommand(api_url)
    cmd.execute(host=host, project_home=project_home,
                service_name=service_name, run_cmd=run_cmd)


if __name__ == '__main__':
    register()
