import click
from controller.start_cmd import StartCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--hippo_id', help='')
@click.option('-i', '--interval', type=int, help='sec')
def start(hippo_id, interval):
    cmd = StartCommand()
    cmd.execute(hippo_id=hippo_id, interval=interval)


if __name__ == '__main__':
    start()
