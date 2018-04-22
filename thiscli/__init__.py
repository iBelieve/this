"""Universal do-thingy for running common project tasks"""

import click
from .project import Project

pass_project = click.make_pass_decorator(Project)


@click.group(invoke_without_command=True)
@click.option('--dry-run', is_flag=True,
              help='show what commands would be run without ' +
              'actually running them')
@click.pass_context
def cli(ctx, dry_run):
    ctx.obj = Project.find()
    ctx.obj.dry_run = dry_run

    if ctx.invoked_subcommand is None:
        ctx.obj.info()


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
@click.option('--env', metavar='ENV',
              help='staging/production/development/etc')
@click.option('--production', '--prod', 'env', flag_value='production')
@click.option('--development', '--dev', 'env', flag_value='development')
@pass_project
def deploy(project, env):
    project.deploy(env)


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
