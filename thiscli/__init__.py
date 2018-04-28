"""Standardized project tool for running common tasks"""

import click
from .project import Project
from .click_colors import HelpColorsGroup

pass_project = click.make_pass_decorator(Project)

projects_help_section = (
    'Supported Projects',
    '\b\n' +
    '\n'.join([project.description for project in Project.all_projects()])
)


@click.group(cls=HelpColorsGroup, invoke_without_command=True,
             post_sections=[projects_help_section])
@click.option('--dry-run', is_flag=True,
              help='Show what commands would be run without '
              'actually running them.')
@click.pass_context
def cli(ctx, dry_run):
    """Standardized project tool for running common tasks"""
    ctx.obj = Project.find()
    ctx.obj.dry_run = dry_run

    if ctx.invoked_subcommand is None:
        ctx.obj.info()


@cli.command()
@click.option('--production', '--prod', '--release', 'env',
              flag_value='production')
@click.option('--development', '--dev', '--debug', 'env',
              flag_value='development')
@pass_project
def build(project, env):
    project.build(env)


@cli.command()
@click.option('--env', metavar='ENV',
              help='staging/production/development/etc')
@click.option('--production', '--prod', '--release', 'env',
              flag_value='production')
@click.option('--development', '--dev', '--debug', 'env',
              flag_value='development')
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
