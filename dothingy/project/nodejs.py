import json
import os

from . import Project
from ..util import needs_update, has_command, warn, fatal


def get_npm_cmd(path):
    has_yarn = has_command('yarn')
    has_yarn_lock = os.path.exists(os.path.join(path, 'yarn.lock'))
    has_npm_lock = os.path.exists(os.path.join(path, "package-lock.json"))

    if has_yarn_lock and has_npm_lock:
        warn("Both yarn.lock and package-lock.json found. " +
             "This may result in out-of-sync dependencies.")

    if has_yarn_lock:
        if has_yarn:
            return 'yarn'
        elif has_npm_lock:
            return 'npm'
        else:
            fatal("yarn.lock found but yarn isn't installed")
    elif has_npm_lock:
        return 'npm'
    elif has_yarn:
        return 'yarn'
    return 'npm'


class NodejsProject(Project):
    def __init__(self, cwd):
        super().__init__(cwd)
        with open('package.json') as f:
            self.package = json.load(f)
        self.npm_cmd = get_npm_cmd(self.cwd)

    @classmethod
    def find(cls):
        return cls.find_containing('package.json')

    def ensure_deps(self):
        if needs_update(self.path('package.json'), self.path('node_modules')):
            self.npm('install')

    def npm(self, cmd):
        if not isinstance(cmd, list):
            cmd = [cmd]

        self.cmd([self.npm_cmd] + cmd)

    def has_script(self, script):
        return script in self.package.get('scripts', {})

    def npm_script(self, scripts, *args):
        args = list(args)
        if args and self.npm_cmd == 'npm':
            args = ['--'] + args
        if not isinstance(scripts, list):
            scripts = [scripts]

        script = next((script for script in scripts
                       if self.has_script(script)), None)
        if script is None:
            fatal("NPM script not found. Looked for: " + ' '.join(scripts))
        self.ensure_deps()
        self.npm(['run', script] + args)

    def build(self):
        self.npm_script('build')

    def test(self):
        self.npm_script('test')

    def lint(self, fix):
        if fix:
            self.npm_script('lint', '--fix')
        else:
            self.npm_script('lint')
