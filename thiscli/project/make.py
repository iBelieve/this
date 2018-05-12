import subprocess

from . import Project
from ..util import fatal


class MakeProject(Project):
    description = 'Makefile'

    def __init__(self, cwd):
        super().__init__(cwd)
        self.targets = subprocess.check_output(
            "make -pRrq : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($1 !~ \"^[#.]\") {print $1}}' | egrep -v '^[^[:alnum:]]'", shell=True, encoding='utf-8').strip().split('\n')
        self.can_run = self.find_target('run') is not None
        self.can_test = self.find_target(['test', 'check']) is not None
        self.can_deploy = self.find_target('deploy') is not None or self.can_deploy

    @classmethod
    def find(cls):
        return cls.find_containing('Makefile')

    def find_target(self, targets):
        if isinstance(targets, str):
            targets = [targets]
        return next((target for target in targets
                     if target in self.targets), None)

    def target(self, targets=None):
        if targets is None:
            self.cmd("make")
            return

        target = self.find_target(targets)

        if not target:
            fatal("Not sure which Makefile target to run. Looked for: " +
                  ' '.join(targets))
        self.cmd("make " + target)

    def build(self, env):
        # TODO: Configure release/debug build from env
        self.target()

    def run(self, env):
        if self.can_run:
            self.target('run')
        else:
            super().run(env)

    def test(self):
        if self.can_test:
            self.target(['test', 'check'])
        else:
            super().test()

    def deploy(self, env):
        if self.can_deploy:
            self.target('deploy')
        else:
            super().deploy(env)
