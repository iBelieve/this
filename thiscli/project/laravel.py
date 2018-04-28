from . import Project
from .nodejs import NodejsProject
from ..util import fatal, needs_update
from ..tmux import Tmux


class LaravelProject(Project):
    description = 'Laravel'

    def __init__(self, cwd):
        super().__init__(cwd)
        if self.exists('package.json'):
            self.npm = NodejsProject(cwd)
        else:
            self.npm = None

        self.can_build = self.npm and self.npm.can_build
        self.can_test = self.exists('tests') or (self.npm and self.npm.can_test)
        self.can_lint = self.npm and self.npm.can_lint

    @classmethod
    def find(cls):
        return cls.find_containing('artisan')

    def ensure_deps(self):
        if needs_update(self.path('composer.json'), self.path('vender')):
            self.cmd('composer install')

    def run(self, env):
        if self.npm and self.npm.can_run:
            tmux = Tmux(self.cwd)
            with tmux.pane():
                self.ensure_deps()
                self.cmd('php artisan serve')
            with tmux.pane():
                self.npm.run(env)
            tmux.run()
        else:
            self.ensure_deps()
            self.cmd('php artisan serve')

    def build(self, env):
        if self.npm and self.npm.can_build:
            self.npm.build(env)
        else:
            super().build(env)

    def test(self):
        if self.exists('tests'):
            self.ensure_deps()
            self.cmd('./vendor/bin/phpunit')
        if self.npm and self.npm.can_test:
            self.npm.test()
        if not self.can_test:
            super().test()

    def lint(self, fix):
        if self.npm and self.npm.can_lint:
            self.npm.lint(fix)
        else:
            super().lint(fix)
