import click
import ConfigParser
from common import const
from utils import common_util
from controller.stop_cmd import StopCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


default_api_host = common_util.get_conf('HippoManagerAPI', 'host')
default_api_port = common_util.get_conf('HippoManagerAPI', 'port')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--hippo_id', help='', required=True)
@click.option('--api_host', help='hippo manager api host, Default: {}'.format(default_api_host))
@click.option('--api_port', help='hippo manager api port, Default: {}'.format(default_api_port))
def stop(hippo_id, api_host, api_port):
    if api_host is None:
        api_host = default_api_host
    if api_port is None:
        api_port = default_api_port
    api_url = '{}:{}'.format(api_host, api_port)
    cmd = StopCommand(api_url)
    cmd.execute(hippo_id=hippo_id)


if __name__ == '__main__':
    stop()
