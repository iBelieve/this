from . import Project
from ..env import is_env_release


class DotnetCoreProject(Project):
    description = '.NET Core'

    @classmethod
    def find(cls):
        return cls.find_containing('*.csproj')

    def build(self, env):
        if is_env_release(env):
            self.cmd("dotnet build -c release")
        else:
            self.cmd("dotnet build")

    def test(self):
        self.cmd("dotnet test")

    def run(self, env):
        if is_env_release(env):
            self.cmd("dotnet run -c release")
        else:
            self.cmd("dotnet run")
