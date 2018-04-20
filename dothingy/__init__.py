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
@pass_project
def deploy(project):
    project.deploy()


@cli.command()
@click.option('--fix', is_flag=True,
              help='Fix lint errors instead of reporting them')
@pass_project
def lint(project, fix):
    project.lint(fix=fix)


@cli.command()
@pass_project
def test(project):
    project.test()


@cli.command()
@pass_project
def check(project):
    project.check()
