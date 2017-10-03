import click
from controller.restart_cmd import RestartCommand


@click.command()
@click.option('--hippo_id', help='')
@click.option('-i', '--interval', type=int, help='sec')
def restart(hippo_id, interval):
    cmd = RestartCommand()
    cmd.execute(hippo_id=hippo_id, interval=interval)


if __name__ == '__main__':
    restart()
