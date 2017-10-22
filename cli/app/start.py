import click
import ConfigParser
from common import const
from utils import common_util
from controller.start_cmd import StartCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


default_api_host = common_util.get_conf('HippoManagerAPI', 'host')
default_api_port = common_util.get_conf('HippoManagerAPI', 'port')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--hippo_id', help='')
@click.option('-i', '--interval', type=int, help='sec')
@click.option('--api_host', help='hippo manager api host, Default: {}'.format(default_api_host))
@click.option('--api_port', help='hippo manager api port, Default: {}'.format(default_api_port))
def start(hippo_id, interval, api_host, api_port):
    if api_host is None:
        api_host = default_api_host
    if api_port is None:
        api_port = default_api_port
    api_url = '{}:{}'.format(api_host, api_port)
    cmd = StartCommand(api_url)
    cmd.execute(hippo_id=hippo_id, interval=interval)


if __name__ == '__main__':
    start()
