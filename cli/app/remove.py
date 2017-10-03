# -*- coding: utf-8 -*-

from __future__ import print_function
import click

from controller.remove_cmd import RemoveCommand


@click.command()
@click.option('--hippo_id', help='')
@click.option('-f', '--force', is_flag=True, help='')
@click.option('-d', '--del_service', is_flag=True, help='Delete service plugin from project')
def remove(hippo_id, force, del_service):

    cmd = RemoveCommand()
    cmd.execute(hippo_id=hippo_id, force=force, del_service=del_service)


if __name__ == '__main__':
    remove()
