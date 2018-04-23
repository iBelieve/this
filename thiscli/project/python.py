from abc import ABC
import os

from . import Project, delayed_exit
from ..util import fatal


class PythonEnv:
    pass


class PythonPipenv(PythonEnv):
    description = 'Pipenv'


class PythonPipTools(PythonEnv):
    description = 'requirements.txt'


class PythonRequirements(PythonEnv):
    description = 'requirements.txt'


class PythonProject(Project, ABC):
    def __init__(self, cwd):
        super().__init__(cwd)

        self.packages = [dirname for dirname in os.listdir(cwd)
                         if self.exists(dirname, '__init__.py')]
        if not self.packages:
            fatal("No python packages containing __init__.py found")

        if self.exists('Pipfile'):
            self.env = PythonPipenv()
        elif self.exists('requirements.in'):
            self.env = PythonPipTools()
        elif self.exists('requirements.txt'):
            self.env = PythonRequirements()
        else:
            self.env = None

        self.can_build = self.can_test = self.exists('setup.py')

    @classmethod
    def find(cls):
        return cls.find_containing('setup.py',
                                   'requirements.txt',
                                   'requirements.in',
                                   'Pipenv')

    @property
    def description(self):
        description = 'Python project'
        if self.env:
            description += ' using ' + self.env.description

        if self.exists('setup.py'):
            if 'using' in description:
                description += ' and setup.py'
            else:
                description += ' using setup.py'
        return description

    def build(self):
        if self.exists('setup.py'):
            self.cmd('python setup.py build')
        else:
            super().build()

    def test(self):
        if self.exists('setup.py'):
            self.cmd('python setup.py test')
        else:
            super().test()

    def lint(self, fix):
        if fix:
            self.cmd('autopep8 --recursive --in-place ' +
                     ' '.join(self.packages))
        with delayed_exit():
            self.cmd('flake8 ' + ' '.join(self.packages))
            self.cmd('pylint ' + ' '.join(self.packages))
            if self.exists('setup.py'):
                self.cmd('python setup.py check')
