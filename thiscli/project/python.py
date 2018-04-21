from abc import ABC
import os

from . import Project, delayed_exit
from ..util import fatal


class PythonProject(Project, ABC):
    def __init__(self, cwd):
        super().__init__(cwd)
        self.packages = [dirname for dirname in os.listdir(cwd)
                         if self.exists(dirname, '__init__.py')]
        if not self.packages:
            fatal("No python packages containing __init__.py found")

    @classmethod
    def find(cls):
        return Project.find_one_of(PythonSetupProject,
                                   PythonPipenvProject)

    def lint(self, fix):
        if fix:
            self.cmd('autopep8 --recursive --in-place ' +
                     ' '.join(self.packages))
        with delayed_exit():
            self.cmd('flake8 ' + ' '.join(self.packages))
            for package in self.packages:
                self.cmd(f'pylint {package}')


class PythonSetupProject(PythonProject):
    @classmethod
    def find(cls):
        return cls.find_containing('setup.py')

    def build(self):
        self.cmd('python setup.py build')

    def test(self):
        self.cmd('python setup.py test')

    def lint(self, fix):
        with delayed_exit():
            super().lint(fix)
        self.cmd('python setup.py check')


class PythonPipenvProject(PythonProject):
    @classmethod
    def find(cls):
        return cls.find_containing('Pipfile')

    def build(self):
        return super().build()

    def test(self):
        return super().test()
