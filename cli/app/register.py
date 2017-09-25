# -*- coding: utf-8 -*-

# step1. call build.sh (check install plugin | install plugin)

# step2. call build.sh (check create service | create service)

# step3. call coordinate (register)

from __future__ import print_function
from __future__ import unicode_literals

import click


@click.command()
@click.option('-h', '--host', default='localhost', help='Server host, Default: localhost')
@click.option('-s', '--service_name', help='Service name')
@click.option('-p', '--project_home', required=True)
def register(host, service_name, project_home):
    print("host : {}".format(host))
    print("service_name : {}".format(service_name))
    print("project_home : {}".format(project_home))

    pass


if __name__ == '__main__':
    register()
