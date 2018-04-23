from . import Project


class CargoProject(Project):
    description = 'Rust project using Cargo'

    @classmethod
    def find(cls):
        return cls.find_containing('Cargo.toml')

    def build(self):
        self.cmd("cargo build")

    def test(self):
        self.cmd("cargo test")

    def run(self, env):
        self.cmd("cargo run", env=env)
