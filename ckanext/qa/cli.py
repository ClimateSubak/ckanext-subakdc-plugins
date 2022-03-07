import click

from ckanext.qa.qa_no_resources import QaNoResourcesTask

@click.group()
def qa():
    pass

@click.command()
def run():
    QaNoResourcesTask().run()

qa.add_command(run)

def get_commands():
    return [qa]