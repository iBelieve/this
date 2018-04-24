import pytest

from thiscli.project import Project
from thiscli.project.python import PythonProject
from . import setup_dir, runs_commands


@pytest.fixture
def python_project(mocker):
    setup_dir(mocker, 'setup.py', 'my_package', 'my_package/__init__.py')
    return Project.find()


def test_find_python_project(python_project):
    assert isinstance(python_project, PythonProject)


def test_build_python_project(python_project):
    with runs_commands('python setup.py build'):
        python_project.build(env=None)


def test_test_python_project(python_project):
    with runs_commands('python setup.py test'):
        python_project.test()


def test_lint_python_project(python_project):
    with runs_commands('flake8 my_package',
                       'pylint my_package',
                       'python setup.py check'):
        python_project.lint(fix=False)
