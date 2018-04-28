import os
import subprocess
from contextlib import contextmanager
from unittest.mock import patch

from .project import Project


def echo(command):
    return 'echo -e "\\e[1;97m$ {}\\e[0m"'.format(command)


def tmux_line(commands):
    commands = [real_cmd for cmd in commands for real_cmd in [echo(cmd), cmd]]
    commands.append('tmux kill-session')
    return '; '.join(commands)


class Tmux:
    def __init__(self, cwd):
        self.cwd = cwd
        self.panes = []

    @contextmanager
    def pane(self):
        commands = []

        def run_command(self, cmd, cwd=None, env=None, echo=True, shell=None):
            from .project import format_command
            commands.append(format_command(cmd, cwd, env))

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

        subprocess.run(cmd, env=dict(os.environ, SHELL='bash'))
