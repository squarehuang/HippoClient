import click
from controller.stop_cmd import StopCommand


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--hippo_id', help='')
def stop(hippo_id):
    cmd = StopCommand()
    cmd.execute(hippo_id=hippo_id)


if __name__ == '__main__':
    stop()
