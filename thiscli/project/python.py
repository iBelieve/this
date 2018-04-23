from abc import ABC, abstractmethod
import os

from . import Project, delayed_exit
from ..util import fatal


class PythonEnv(ABC):
    @abstractmethod
    def has_package(self, name):
        pass


class PythonPipenv(PythonEnv):
    description = 'Pipenv'

    def __init__(self, project):
        with open(project.path('Pipfile')) as f:
            self.pipfile = f.read()

    def has_package(self, name):
        return (name + ' = ') in self.pipfile


class PythonPipTools(PythonEnv):
    description = 'pip-tools'

    def __init__(self, project):
        with open(project.path('requirements.in')) as f:
            self.requirements = f.read()

    def has_package(self, name):
        return name in self.requirements


class PythonRequirements(PythonEnv):
    description = 'requirements.txt'

    def __init__(self, project):
        with open(project.path('requirements.txt')) as f:
            self.requirements = f.read()

    def has_package(self, name):
        return name in self.requirements


class PythonProject(Project):
    def __init__(self, cwd):
        super().__init__(cwd)

        self.has_setup = self.exists('setup.py')

        self.packages = [dirname for dirname in os.listdir(cwd)
                         if self.exists(dirname, '__init__.py')]
        if not self.packages:
            fatal("No python packages containing __init__.py found")

        if self.exists('Pipfile'):
            self.env = PythonPipenv(self)
        elif self.exists('requirements.in'):
            self.env = PythonPipTools(self)
        elif self.exists('requirements.txt'):
            self.env = PythonRequirements(self)
        else:
            self.env = None

        self.can_build = self.has_setup
        self.can_test = self.has_setup or self.has_package('pytest')
        self.can_deploy = self.has_setup or self.can_deploy

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

        if self.has_setup:
            if 'using' in description:
                description += ' and setup.py'
            else:
                description += ' using setup.py'
        return description

    def has_package(self, name):
        if self.env:
            return self.env.has_package(name)
        else:
            return False

    def build(self):
        if self.has_setup:
            self.cmd('python setup.py build')
        else:
            super().build()

    def test(self):
        if self.has_setup:
            self.cmd('python setup.py test')
        elif self.has_package('pytest'):
            self.cmd('pytest')
        else:
            super().test()

    def deploy(self, env):
        if self.has_setup:
            self.cmd('python setup.py sdist upload')
        else:
            super().deploy()

    def lint(self, fix):
        if fix:
            self.cmd('autopep8 --recursive --in-place ' +
                     ' '.join(self.packages))
        with delayed_exit():
            self.cmd('flake8 ' + ' '.join(self.packages))
            self.cmd('pylint ' + ' '.join(self.packages))
            if self.exists('setup.py'):
                self.cmd('python setup.py check')
