from abc import ABC, abstractmethod
import subprocess
import os
import sys
import click

from ..util import walk_up


class Project(ABC):
    def __init__(self, cwd):
        self.cwd = cwd

    def run(self, cmd, env=None, echo=True, shell=None):
        if env is not None:
            env = dict(os.environ, **env)
        if shell is None:
            shell = ' ' in cmd
        if echo:
            echo_command(cmd, env)
        proc = subprocess.run(cmd, cwd=self.cwd, shell=shell, env=env)
        if proc.returncode != 0:
            sys.exit(proc.returncode)

    def build(self):
        print("Sorry! I don't know how to build your project")

    def deploy(self):
        print("Sorry! I don't know how to deploy your project")

    @classmethod
    @abstractmethod
    def find(cls):
        from .python import PythonProject

        project = Project.find_one_of(PythonProject)

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


def echo_command(cmd, env):
    if isinstance(cmd, list):
        cmd = ' '.join(maybe_quote_arg(arg) for arg in cmd)
    if env is not None:
        cmd = (' '.join(key + '=' + value for key, value in env.items()) +
               ' ' + cmd)
    click.secho('$ ' + cmd, fg='white', bold=True)


def maybe_quote_arg(arg):
    if ' ' not in arg:
        return arg
    elif '"' in arg:
        return "'" + arg + "'"
    return '"' + arg + '"'
