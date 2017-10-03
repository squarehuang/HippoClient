# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import socket
from controller.register_cmd import RegisterCommand
import click


@click.command()
@click.option('--host', help='Server host, Default: {}'.format(socket.gethostname()))
@click.option('-p', '--project_home', required=True)
@click.option('-s', '--service_name', help='Service name')
@click.option('-c', '--run_cmd', help='command for run service')
def register(host, project_home, service_name, run_cmd):
    cmd = RegisterCommand()
    cmd.execute(host=host, project_home=project_home,
                service_name=service_name, run_cmd=run_cmd)


if __name__ == '__main__':
    register()
