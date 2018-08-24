from abc import ABC, abstractmethod
import os

from . import Project, delayed_exit
from .nodejs import NodejsProject
from ..util import fatal
from ..tmux import Tmux


class PythonEnv(ABC):
    def __init__(self, project):
        self.project = project

    @abstractmethod
    def has_package(self, name):
        pass

    @abstractmethod
    def ensure_deps(self):
        pass

    @abstractmethod
    def cmd(self, cmd):
        pass


class PythonPipenv(PythonEnv):
    description = 'Pipenv'

    def __init__(self, project):
        super().__init__(project)
        with open(project.path('Pipfile')) as f:
            self.pipfile = f.read()

    def ensure_deps(self):
        pass

    def has_package(self, name):
        return (name + ' = ') in self.pipfile

    def cmd(self, cmd):
        self.project.cmd('pipenv run ' + cmd)


class PythonVirtualenv(PythonEnv):
    def get_virtualenv(self):
        if 'VIRTUAL_ENV' in os.environ:
            return None

        return {'VIRTUAL_ENV': self.project.path('.venv'),
                'PATH': '{}/bin:{}'.format(self.project.path('.venv'),
                                           os.environ.get('PATH'))}

    def ensure_deps(self):
        if 'VIRTUAL_ENV' not in os.environ and not self.project.exists('.venv'):
            self.project.cmd('virtualenv .venv')
            self.install_deps()

    @abstractmethod
    def install_deps():
        pass

    def cmd(self, cmd):
        env = self.get_virtualenv()
        env_echo = '(virtualenv)' if env else ''
        self.project.cmd(cmd, env=env, env_echo=env_echo)


class PythonPipTools(PythonVirtualenv):
    description = 'pip-tools'

    def __init__(self, project):
        super().__init__(project)
        with open(project.path('requirements.in')) as f:
            self.requirements = f.read()

    def install_deps(self):
        self.cmd('pip install pip-tools')
        self.cmd('pip-sync')

    def has_package(self, name):
        return name in self.requirements


class PythonRequirements(PythonVirtualenv):
    description = 'requirements.txt'

    def __init__(self, project):
        super().__init__(project)
        with open(project.path('requirements.txt')) as f:
            self.requirements = f.read()

    def install_deps(self):
        self.cmd('pip install -r requirements.txt')

    def has_package(self, name):
        return name in self.requirements


class PythonProject(Project):
    description = 'Python'

    def __init__(self, cwd):
        super().__init__(cwd)

        self.packages = [dirname for dirname in os.listdir(cwd)
                         if self.exists(dirname, '__init__.py')]
        self.non_test_packages = [package for package in self.packages
                                  if package != 'tests']
        self.main_package = next((package for package in self.packages
                                  if self.exists(package, '__main__.py')), None)
        if not self.packages:
            fatal("No python packages containing __init__.py found")

        if self.exists('package.json'):
            self.npm = NodejsProject(cwd)
        else:
            self.npm = next((NodejsProject(self.path(dirname))
                             for dirname in os.listdir(cwd)
                             if self.exists(dirname, 'package.json')), None)

        if self.exists('Pipfile'):
            self.env = PythonPipenv(self)
        elif self.exists('requirements.in'):
            self.env = PythonPipTools(self)
        elif self.exists('requirements.txt'):
            self.env = PythonRequirements(self)
        else:
            self.env = None

        self.has_setup = self.exists('setup.py')
        self.has_manage = self.exists('manage.py')
        self.has_flask = self.has_package('flask')

        self.can_build = self.has_setup
        self.can_test = self.has_setup or self.has_package('pytest')
        self.can_deploy = self.has_setup or self.can_deploy
        self.can_run = (self.has_manage or self.main_package or self.has_flask or
                        (self.npm and self.npm.can_run))

        if self.env:
            self.using.append(self.env.description)
        if self.has_setup:
            self.using.append('setup.py')
        if self.has_manage:
            self.using.append('manage.py')
        if not self.has_manage and self.has_flask:
            self.using.append('Flask')

    @classmethod
    def find(cls):
        return cls.find_containing('setup.py',
                                   'requirements.txt',
                                   'requirements.in',
                                   'Pipfile')

    def ensure_deps(self):
        if self.env:
            self.env.ensure_deps()

    def env_cmd(self, cmd):
        if self.env:
            self.env.cmd(cmd)
        else:
            self.cmd(cmd)

    def has_package(self, name):
        if self.env:
            return self.env.has_package(name)
        else:
            return False

    def build(self, env):
        self.ensure_deps()
        if self.has_setup:
            self.env_cmd('python setup.py build')
        else:
            super().build(env)

    def run(self, env):
        can_py_run = self.has_manage or self.main_package or self.has_flask
        can_npm_run = self.npm and self.npm.can_run

        if not can_py_run and not can_npm_run:
            super().run(env)
            return

        def run_py():
            self.ensure_deps()

            if self.has_manage:
                self.env_cmd('python manage.py runserver')
            elif self.main_package:
                self.env_cmd('python -m ' + self.main_package)
            elif self.has_flask:
                self.env_cmd('flask run')

        if can_py_run and can_npm_run:
            tmux = Tmux(self.cwd)
            with tmux.pane():
                run_py()
            with tmux.pane():
                self.npm.run(env)
            tmux.run()
        elif can_npm_run:
            self.npm.run()
        else:
            run_py()

    def test(self):
        self.ensure_deps()
        if self.has_setup:
            self.env_cmd('python setup.py test')
        elif self.has_package('pytest'):
            self.env_cmd('pytest')
        else:
            super().test()

    def deploy(self, env):
        if self.has_setup:
            self.ensure_deps()
            self.env_cmd('python setup.py sdist bdist_wheel upload')
        else:
            super().deploy(env)

    def lint(self, fix):
        self.ensure_deps()
        if fix:
            self.env_cmd('autopep8 --recursive --in-place ' +
                         ' '.join(self.packages))
        with delayed_exit():
            self.env_cmd('flake8 ' + ' '.join(self.packages))
            self.env_cmd('pylint ' + ' '.join(self.packages))
            if self.exists('setup.py'):
                self.env_cmd('python setup.py check')
