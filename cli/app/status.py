import click
from controller.status_cmd import StatusCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--host', default='localhost', help='Server host, Default: localhost')
@click.option('-s', '--service_name', help='Service name')
@click.option('--hippo_id', help='')
@click.option('-a', '--all_mode', is_flag=True, help='Get cluster status')
@click.option('-n', '--node_mode', is_flag=True, help='Get node status')
def status(host, service_name, hippo_id, all_mode, node_mode):
    cmd = StatusCommand()
    if hippo_id != None:
        cmd.execute(hippo_id=hippo_id)
    elif node_mode == True:
        cmd.execute_node()
    elif all_mode == True:
        cmd.execute_cluster()


if __name__ == '__main__':
    status()
