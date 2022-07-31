import click


@click.group()
def characters():
    pass


@characters.command()
def listchar():
    click.echo('Called listchar successfully')
