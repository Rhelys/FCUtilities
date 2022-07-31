import click


@click.group()
def basics():
    pass


@basics.command()
@basics.argument('fcid')
def fcname():
    click.echo('Called fcname successfully')
