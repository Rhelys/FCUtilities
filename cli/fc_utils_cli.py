import click
from commands.characters import listchar


@click.group()
def cli():
    pass


cli.add_command(listchar)

if __name__ == '__main__':
    cli()
