import click
import ConfigParser
from common import const
from utils import common_util
from controller.status_cmd import StatusCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


default_api_host = common_util.get_conf('HippoManagerAPI', 'host')
default_api_port = common_util.get_conf('HippoManagerAPI', 'port')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--hippo_id', help='')
@click.option('--api_host', help='hippo manager api host, Default: {}'.format(default_api_host))
@click.option('--api_port', help='hippo manager api port, Default: {}'.format(default_api_port))
@click.option('-a', '--all_mode', is_flag=True, help='Get cluster status')
@click.option('-n', '--node_mode', is_flag=True, help='Get node (api_host) status')
def status(hippo_id, all_mode, node_mode, api_host, api_port):
    if api_host is None:
        api_host = default_api_host
    if api_port is None:
        api_port = default_api_port
    api_url = '{}:{}'.format(api_host, api_port)

    cmd = StatusCommand(api_url)
    if hippo_id != None:
        cmd.execute(hippo_id=hippo_id)
    elif node_mode == True:
        cmd.execute_node()
    else:
        cmd.execute_cluster()


if __name__ == '__main__':
    status()
