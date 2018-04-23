from abc import ABC
import os

from . import Project, delayed_exit
from ..util import fatal


class PythonProject(Project, ABC):
    _description = 'Python project'

    def __init__(self, cwd):
        super().__init__(cwd)
        self.packages = [dirname for dirname in os.listdir(cwd)
                         if self.exists(dirname, '__init__.py')]
        if not self.packages:
            fatal("No python packages containing __init__.py found")
        self.can_build = self.can_test = self.exists('setup.py')

    @classmethod
    def find(cls):
        return Project.find_one_of(PythonPipenvProject,
                                   PythonPipToolsProject,
                                   PythonRequirementsProject,
                                   PythonSetupProject)

    @property
    def description(self):
        description = self._description
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


class PythonPipenvProject(PythonProject):
    _description = 'Python project using Pipenv'

    @classmethod
    def find(cls):
        return cls.find_containing('Pipfile')


class PythonPipToolsProject(PythonProject):
    _description = 'Python project using pip-tools'

    @classmethod
    def find(cls):
        return cls.find_containing('requirements.in')


class PythonRequirementsProject(PythonProject):
    _description = 'Python project using requirements.txt'

    @classmethod
    def find(cls):
        return cls.find_containing('requirements.txt')


class PythonSetupProject(PythonProject):
    _description = 'Python project'

    @classmethod
    def find(cls):
        return cls.find_containing('setup.py')
