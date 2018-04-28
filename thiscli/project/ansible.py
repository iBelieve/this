from . import Project
from ..env import SHORT_ENV_NAMES, all_env_names
from ..util import fatal

GENERIC_INVENTORY_FILENAMES = ['ansible/hosts',
                               'ansible/inventory']


class AnsibleProject(Project):
    description = 'Ansible'

    @classmethod
    def find(cls):
        return cls.find_containing("ansible")

    def deploy(self, env):
        deploy(self, env)


def install_roles(project):
    if not project.exists('ansible/requirements.yml'):
        return

    project.cmd("ansible-galaxy install -r ansible/requirements.yml")


def inventory_filenames_for_env(name):
    return ([filename for env in all_env_names(name)
             for filename in [f'ansible/{env}',
                              f'ansible/{env}/hosts',
                              f'ansible/{env}/inventory']] +
            GENERIC_INVENTORY_FILENAMES)


def find_valid_inventory_envs(project):
    return [env for env in SHORT_ENV_NAMES
            if any(project.exists(filename) for filename in
                   inventory_filenames_for_env(env))]


def find_inventory(project, env):
    if env:
        filenames = inventory_filenames_for_env(env)
    else:
        filenames = GENERIC_INVENTORY_FILENAMES

    filename = project.find_file(*filenames)

    if not filename:
        if env is None:
            valid_envs = find_valid_inventory_envs(project)

            if valid_envs:
                fatal("Ansible hosts file not found. " +
                      "Did you forget to specifiy --env {}?",
                      ' | '.join(valid_envs))

        fatal("Ansible hosts file not found. Looked for one of: {}",
              ' '.join(filenames))

    return filename


def find_playbook(project):
    filenames = ["ansible/deploy.yml", "ansible/playbook.yml"]
    filename = project.find_file(*filenames)

    if not filename:
        fatal("Playbook not found. Looked for one of: {}",
              ' '.join(filenames))

    return filename


def run_playbook(project, env):
    inventory = find_inventory(project, env)
    playbook = find_playbook(project)

    project.cmd(f"ansible-playbook -i {inventory} {playbook}")


def deploy(project, env):
    install_roles(project)
    run_playbook(project, env)


def is_present(project):
    return project.exists("ansible")
