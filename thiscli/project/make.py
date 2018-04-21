import subprocess

from . import Project
from ..util import fatal


class MakeProject(Project):
    def __init__(self, cwd):
        super().__init__(cwd)
        self.targets = subprocess.check_output("make -pRrq : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($1 !~ \"^[#.]\") {print $1}}' | egrep -v '^[^[:alnum:]]'", shell=True, encoding='utf-8').strip().split('\n')

    @classmethod
    def find(cls):
        return cls.find_containing('Makefile')

    def target(self, targets=None):
        if targets is None:
            self.cmd("make")
            return
        if isinstance(targets, str):
            targets = [targets]
        target = next((target for target in targets
                       if target in self.targets), None)
        if not target:
            fatal("Not sure which Makefile target to run. Looked for: " +
                  ' '.join(targets))
        self.cmd("make " + target)

    def build(self):
        self.target()

    def test(self):
        self.target(['test', 'check'])
