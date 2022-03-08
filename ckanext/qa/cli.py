import click

from ckanext.qa.qa import QaTaskRunner
from ckanext.qa.qa_no_resources import QaNoResourcesTask

@click.group()
def qa():
    pass

@click.command()
def run():
    """
    Runs all tasks over all packages
    
    Run using `ckan qa run` in the CKAN container
    """
    tasks = [ QaNoResourcesTask ]
    runner = QaTaskRunner(tasks)
    runner.run()

qa.add_command(run)

def get_commands():
    return [qa]