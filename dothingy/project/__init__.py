from abc import ABC, abstractmethod
from contextlib import contextmanager
import subprocess
import os
import sys
import threading
import click

from ..util import walk_up

local = threading.local()


@contextmanager
def delayed_exit():
    local.exit_code = 0
    yield
    if local.exit_code != 0:
        sys.exit(local.exit_code)
    delattr(local, 'exit_code')


class Project(ABC):
    def __init__(self, cwd):
        self.cwd = cwd

    def cmd(self, cmd, cwd=None, env=None, echo=True, shell=None):
        if echo:
            echo_command(cmd, cwd, env)
        if cwd is not None:
            cwd = self.path(cwd)
        else:
            cwd = self.cwd
        if env is not None:
            env = dict(os.environ, **env)
        if shell is None:
            shell = ' ' in cmd
        proc = subprocess.run(cmd, cwd=cwd, shell=shell, env=env)
        if proc.returncode != 0:
            if hasattr(local, 'exit_code'):
                if local.exit_code == 0:
                    local.exit_code = proc.returncode
            else:
                sys.exit(proc.returncode)

    def path(self, *path):
        return os.path.join(self.cwd, *path)

    def exists(self, *path):
        return os.path.exists(self.path(*path))

    def has_action(self, action):
        return getattr(type(self), action) != getattr(Project, action)

    def fail(self, message):
        click.echo(message)
        sys.exit(1)

    def build(self):
        self.fail("Sorry! I don't know how to build your project")

    def deploy(self):
        self.fail("Sorry! I don't know how to deploy your project")

    def lint(self, fix):
        self.fail("Sorry! I don't know how to lint your project")

    def test(self):
        self.fail("Sorry! I don't know how to test your project")

    def check(self):
        if not (self.has_action('lint') or self.has_action('test')):
            self.fail("Sorry! I don't know how to check your project")

        with delayed_exit():
            if self.has_action('lint'):
                self.lint(fix=False)
            if self.has_action('test'):
                self.test()

    @classmethod
    @abstractmethod
    def find(cls):
        from .autotools import AutotoolsProject
        from .meson import MesonProject
        from .python import PythonProject

        project = Project.find_one_of(AutotoolsProject,
                                      MesonProject,
                                      PythonProject)

        if project is None:
            print("Sorry! I don't recognize your project type")
            sys.exit(1)

        return project

    @classmethod
    def find_containing(cls, *filenames):
        for root, files in walk_up(os.getcwd()):
            if any(filename in files for filename in filenames):
                return cls(root)
            if '.git' in files:
                break
        return None

    @staticmethod
    def find_one_of(*classes):
        for cls in classes:
            project = cls.find()
            if project is not None:
                return project
        return None


def echo_command(cmd, cwd, env):
    if isinstance(cmd, list):
        cmd = ' '.join(maybe_quote_arg(arg) for arg in cmd)
    if env is not None:
        cmd = (' '.join(key + '=' + value for key, value in env.items()) +
               ' ' + cmd)
    if cwd is not None:
        cmd = 'cd {} && {}'.format(cwd, cmd)
    click.secho('$ ' + cmd, fg='white', bold=True)


def maybe_quote_arg(arg):
    if ' ' not in arg:
        return arg
    elif '"' in arg:
        return "'" + arg + "'"
    return '"' + arg + '"'
