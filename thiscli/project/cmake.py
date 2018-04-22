import os

from . import Project
from ..util import has_command, fail


class CMakeProject(Project):
    description = 'CMake project'

    def __init__(self, cwd):
        super().__init__(cwd)

        if self.exists('build/Makefile'):
            self.description += ' using make'
        elif self.exists('build/build.ninja'):
            self.description += ' using ninja'

    @classmethod
    def find(cls):
        return cls.find_containing('CMakeLists.txt')

    def ensure_builddir(self):
        if (self.exists('build/Makefile') or
                self.exists('build/build.ninja')):
            return

        os.makedirs('build', exist_ok=True)

        if has_command('ninja'):
            self.cmd('cmake -G Ninja ..', cwd='build')
        else:
            self.cmd('cmake ..', cwd='build')

    def target(self, target=''):
        self.ensure_builddir()
        if self.exists('build/Makefile'):
            self.cmd('make ' + target, cwd='build')
        elif self.exists('build/build.ninja'):
            self.cmd('ninja -C build ' + target)
        else:
            fail("Sorry! I don't know what build tool CMake is using")

    def build(self):
        self.target()

    def test(self):
        self.target('test')
