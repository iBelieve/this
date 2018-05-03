import os
import subprocess
from contextlib import contextmanager
from unittest.mock import patch

from .project import Project, format_command


def echo(cmd, cwd, env, env_echo):
    cmd = format_command(cmd, cwd, env, env_echo)
    return 'echo -e "\\e[1;97m$ {}\\e[0m"'.format(cmd)


def tmux_line(commands):
    commands = [real_cmd for cmd in commands
                for real_cmd in [echo(**cmd), format_command(cmd=cmd['cmd'],
                                                             cwd=cmd['cwd'],
                                                             env=cmd['env'],
                                                             env_echo=None)]]
    commands.append('read')
    commands.append('tmux kill-session')
    return '; '.join(commands)


class Tmux:
    def __init__(self, cwd):
        self.cwd = cwd
        self.panes = []

    @contextmanager
    def pane(self):
        commands = []
        root_cwd = self.cwd

        def run_command(self, cmd, cwd=None, env=None, env_echo=None,
                        echo=True, shell=None):
            if cwd:
                cwd = self.path(cwd)
            else:
                cwd = self.cwd
            cwd = os.path.relpath(cwd, root_cwd)
            if cwd == '.':
                cwd = None
            commands.append(dict(cmd=cmd, cwd=cwd, env=env, env_echo=env_echo))

        with patch.object(Project, 'cmd', new=run_command):
            yield
        self.panes.append(commands)

    def run(self):
        cmd = ['tmux',
               'bind-key', '-n', 'C-c', 'kill-session', ';',
               'set', '-g', 'mouse', 'on', ';']
        cmd += ['new-session', tmux_line(self.panes[0]), ';']
        for pane in self.panes[1:]:
            cmd += ['split-window', tmux_line(pane), ';']
        cmd += ['select-layout', 'even-horizontal']

        subprocess.run(cmd, cwd=self.cwd, env=dict(os.environ,
                                                   PWD=self.cwd,
                                                   SHELL='bash'))
