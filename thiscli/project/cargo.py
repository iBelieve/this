from . import Project
from ..env import is_env_release


class CargoProject(Project):
    description = 'Rust/Cargo'

    @classmethod
    def find(cls):
        return cls.find_containing('Cargo.toml')

    def build(self, env):
        if is_env_release(env):
            self.cmd("cargo build --release")
        else:
            self.cmd("cargo build")

    def test(self):
        self.cmd("cargo test")

    def run(self, env):
        if is_env_release(env):
            self.cmd("cargo run --release")
        else:
            self.cmd("cargo run")
