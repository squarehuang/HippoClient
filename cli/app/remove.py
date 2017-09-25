# -*- coding: utf-8 -*-


# step1. call build.sh remove service # --all

# step2. call coordinate (stop) # --force

# step3. call coordinate (remove)


from __future__ import print_function
import click


@click.command()
@click.option('-h', '--host', default='localhost', help='Server host, Default: localhost')
@click.option('-s', '--service_name', help='Service name')
@click.option('--instance_id', help='')
@click.option('-p', '--project_home', required=True)
@click.option('-f', '--force', help='')
@click.option('-d', '--del_service', help='Delete service plugin from project')
def remove(host, service_name, instance_id, project_home, force, del_service):
    print("host : {}".format(host))
    print("service_name : {}".format(service_name))
    print("project_home : {}".format(project_home))

    pass


if __name__ == '__main__':
    remove()
