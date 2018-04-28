from collections import namedtuple
from .util import fatal

Env = namedtuple('Env', ['name', 'short', 'other'])

ENVIRONMENTS = [
    Env('development', 'dev', ['debug']),
    Env('staging', 'staging', ['stage']),
    Env('production', 'prod', ['release']),
    Env('testing', 'test', ['qa'])
]

STANDARD_ENV_NAMES = [env.name for env in ENVIRONMENTS]
SHORT_ENV_NAMES = [env.short for env in ENVIRONMENTS]

DEV_PROD_NAMES = ['dev', 'devleopment', 'prod', 'production']

def get_env(name):
    for env in ENVIRONMENTS:
        if env.name == name or env.short == name or name in env.other:
            return env
    return None


def short_env_name(name):
    env = get_env(name)
    return env.short if env else name


def env_to_release_or_debug(name, other=False):
    if name in ['release', 'production', 'prod']:
        return 'release'
    elif name in ['debug', 'development', 'dev']:
        return 'debug'
    elif other:
        return name

    fatal('Unsupport --env value. Please use --release/--debug or ' +
          'one of the equivalent aliases.')


def is_env_release(name):
    return env_to_release_or_debug(name) == 'release'


def all_env_names(name):
    env = get_env(name)
    if env:
        return set([env.name, env.short, *env.other])
    else:
        return set(name)
