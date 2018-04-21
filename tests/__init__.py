from contextlib import contextmanager
from unittest.mock import patch
import os

from thiscli.project import Project


def setup_dir(mocker, *files):
    cwd = '/path/to/project'
    files = [os.path.join(cwd, filename) for filename in files]

    def listdir(path):
        files_in_dir = []
        for filename in files:
            if filename.startswith(path):
                name = filename[len(path):]
                if name.startswith('/'):
                    name = name[1:]
                if '/' not in name:
                    files_in_dir.append(name)
        return files_in_dir

    mocker.patch('os.getcwd', new=lambda: cwd)
    mocker.patch('os.path.exists', new=lambda path: path in files)
    mocker.patch('os.listdir', new=listdir)


@contextmanager
def runs_commands(*commands):
    commands = list(commands)
    ran_commands = []

    def run_command(self, cmd, cwd=None, env=None, echo=True, shell=None):
        from thiscli.project import format_command, echo_command
        echo_command(cmd, cwd, env)
        ran_commands.append(format_command(cmd, cwd, env))

    with patch.object(Project, 'cmd', new=run_command):
        yield
    assert ran_commands == commands
