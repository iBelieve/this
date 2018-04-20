import os

from . import Project, delayed_exit


class PythonProject(Project):
    def __init__(self, cwd):
        super().__init__(cwd)
        self.packages = [dirname for dirname in os.listdir(cwd)
                         if self.exists(dirname, '__init__.py')]

    @classmethod
    def find(cls):
        return Project.find_one_of(PythonSetupProject,
                                   PythonPipenvProject)


class PythonSetupProject(PythonProject):
    @classmethod
    def find(cls):
        return cls.find_containing('setup.py')

    def build(self):
        self.cmd('python setup.py build')

    def lint(self, fix=False):
        if fix:
            self.cmd('autopep8 --recursive --in-place .')
        with delayed_exit():
            self.cmd('flake8')
            for package in self.packages:
                self.cmd(f'pylint {package}')


class PythonPipenvProject(PythonProject):
    @classmethod
    def find(cls):
        return cls.find_containing('Pipenv')
