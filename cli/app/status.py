import click


@click.command()
@click.option('-h', '--host', default='localhost', help='Server host, Default: localhost')
@click.option('-s', '--service_name', help='Service name')
@click.option('--instance_id', help='')
@click.option('-a', '--all_mode', is_flag=True, help='Get cluster status')
@click.option('-n', '--node_mode', is_flag=True, help='Get node status')
def status(host, service_name, instance_id, all_mode, node_mode):
    print("status...")
    print("host : {}".format(host))
    print("service_name : {}".format(service_name))
    print("instance_id : {}".format(instance_id))
    print("all_mode : {}".format(all_mode))
    print("node_mode : {}".format(node_mode))


if __name__ == '__main__':
    status()
