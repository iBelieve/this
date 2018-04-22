from . import Project


class AutotoolsProject(Project):
    description = 'Autotools project'

    @classmethod
    def find(cls):
        return cls.find_containing('configure.ac')

    def ensure_makefile(self):
        if self.exists('Makefile'):
            return

        if not self.exists('configure'):
            if self.exists('bootstrap'):
                self.cmd('./bootstrap')
            elif self.exists('autogen.sh'):
                self.cmd('./autogen.sh')
            else:
                self.cmd('autoreconf')

        self.cmd('./configure')

    def build(self):
        self.ensure_makefile()
        self.cmd('make')

    def test(self):
        self.ensure_makefile()
        self.cmd('make check')
