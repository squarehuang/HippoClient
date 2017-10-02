import click
from controller.stop_cmd import StopCommand


@click.command()
@click.option('--hippo_id', help='')
def stop(hippo_id):
    cmd = StopCommand()
    cmd.execute(hippo_id=hippo_id)


if __name__ == '__main__':
    stop()
