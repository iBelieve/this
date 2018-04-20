import click
from .project import Project

pass_project = click.make_pass_decorator(Project)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Project.find()


@cli.command()
@pass_project
def build(project):
    project.build()


@cli.command()
def deploy():
    click.echo('Dropped the database')
