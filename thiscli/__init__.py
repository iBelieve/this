"""Universal do-thingy for running common project tasks"""

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
@click.option('--env', metavar='ENV',
              help='staging/production/development/etc')
@click.option('--production', '--prod', 'env', flag_value='production')
@click.option('--development', '--dev', 'env', flag_value='development')
@pass_project
def run(project, env):
    project.run(env)


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
