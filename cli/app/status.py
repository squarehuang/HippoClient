import click
import ConfigParser
from common import const
from utils import common_util
from controller.status_cmd import StatusCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


default_api_host = common_util.get_conf('HippoManagerAPI', 'host')
default_api_port = common_util.get_conf('HippoManagerAPI', 'port')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--id', help='hippo id')
@click.option('--api_host', default=default_api_host, help='hippo manager api host, Default: {}'.format(default_api_host))
@click.option('--api_port', default=default_api_port, help='hippo manager api port, Default: {}'.format(default_api_port))
@click.option('-a', '--all_mode', is_flag=True, help='Get cluster status, Default: active')
@click.option('-n', '--node_mode', is_flag=True, help='Get node (api_host) status')
@click.option('-u', '--user', help='filter by register user')
@click.option('--client_ip',  help='filter by client server IP')
def status(id, all_mode, node_mode, api_host, api_port, user, client_ip):

    api_url = '{}:{}'.format(api_host, api_port)

    cmd = StatusCommand(api_url)
    if id != None:
        cmd.execute(id=id)
    elif node_mode == True:
        cmd.execute_node(user=user, client_ip=client_ip)
    else:
        cmd.execute_cluster(user=user, client_ip=client_ip)


if __name__ == '__main__':
    status()
