from . import Project


class CargoProject(Project):
    @classmethod
    def find(cls):
        return cls.find_containing('Cargo.toml')

    def build(self):
        self.cmd("cargo build")

    def test(self):
        self.cmd("cargo test")
