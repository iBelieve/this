from . import Project


class PythonProject(Project):
    @classmethod
    def find(cls):
        return Project.find_one_of(PythonSetupProject,
                                   PythonPipenvProject)


class PythonSetupProject(Project):
    def build(self):
        self.run("python setup.py build")

    @classmethod
    def find(cls):
        return cls.find_containing("setup.py")


class PythonPipenvProject(Project):
    @classmethod
    def find(cls):
        return cls.find_containing("Pipenv")
