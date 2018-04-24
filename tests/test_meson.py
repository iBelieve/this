import pytest

from thiscli.project import Project
from thiscli.project.meson import MesonProject
from . import setup_dir, runs_commands


@pytest.fixture
def meson_project(mocker):
    setup_dir(mocker, 'meson.build')
    return Project.find()


def test_find_meson_project(meson_project):
    assert isinstance(meson_project, MesonProject)


def test_build_meson_project(meson_project):
    with runs_commands('meson setup build --prefix=$HOME/.local',
                       'ninja -C build'):
        meson_project.build(env=None)
