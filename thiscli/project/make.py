import subprocess

from . import Project
from ..util import fatal


class MakeProject(Project):
    description = 'Makefile'

    def __init__(self, cwd):
        super().__init__(cwd)
        self.targets = subprocess.check_output("make -pRrq : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($1 !~ \"^[#.]\") {print $1}}' | egrep -v '^[^[:alnum:]]'", shell=True, encoding='utf-8').strip().split('\n')
        self.can_test = self.find_target(['test', 'check']) is not None

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

    def test(self):
        self.target(['test', 'check'])
