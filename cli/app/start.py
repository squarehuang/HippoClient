

import click


@click.command()
@click.option('-h', '--host', default='localhost', help='Server host, Default: localhost')
@click.option('-s', '--service_name', help='Service name')
@click.option('--instance_id', help='')
@click.option('-i', '--interval', help='')
def start(host, service_name, instance_id, interval):
    print("start...")
    print("host : {}".format(host))
    print("service_name : {}".format(service_name))
    print("instance_id : {}".format(instance_id))
    print("interval : {}".format(interval))
    pass


if __name__ == '__main__':
    start()
