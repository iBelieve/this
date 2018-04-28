import os

from . import Project, delayed_exit
from ..env import env_to_release_or_debug


class GradleProject(Project):
    description = 'Gradle'

    def __init__(self, cwd):
        super().__init__(cwd)

        self.gradle_cmd = 'gradle'
        if os.name == 'nt':
            if self.exists('gradlew.bat'):
                self.gradle_cmd = './gradlew.bat'
        else:
            if self.exists('gradlew'):
                self.gradle_cmd = './gradlew'

    @classmethod
    def find(cls):
        return cls.find_containing('build.gradle')

    def gradle(self, task, env=None):
        if env:
            env = env_to_release_or_debug(env, other=True)
            task += env.capitalize()

        self.cmd(self.gradle_cmd + " " + task)

    def build(self, env):
        self.gradle('assemble', env=env)

    def test(self):
        self.gradle('test')

    def check(self):
        with delayed_exit():
            if self.has_action('lint'):
                self.lint(fix=False)
            self.gradle('check')
