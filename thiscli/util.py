import os
import shutil
import sys
import click


def walk_up(bottom):
    """
    mimic os.walk, but walk 'up'
    instead of down the directory tree
    """

    while True:
        bottom = os.path.realpath(bottom)

        yield bottom, os.listdir(bottom)

        new_path = os.path.realpath(os.path.join(bottom, '..'))

        if new_path == bottom:
            return
        bottom = new_path


def has_command(cmd):
    return shutil.which(cmd) is not None


def needs_update(src, dest):
    if not os.path.exists(dest):
        return True
    return os.path.getmtime(src) > os.path.getmtime(dest)


def fail(message):
    click.echo(message)
    sys.exit(1)


def fatal(message, *args, **kwargs):
    if args or kwargs:
        message = message.format(*args, **kwargs)
    click.secho('ERROR: ' + message, fg='red', bold=True)
    sys.exit(1)


def warn(message):
    click.secho('WARNING: ' + message, fg='yellow', bold=True)


def oxford_join(phrases):
    if not phrases:
        return ""
    elif len(phrases) == 1:
        return str(phrases[0])
    elif len(phrases) == 2:
        return "{} and {}".format(", ".join(phrases[:-1]), phrases[-1])
    else:
        return "{}, and {}".format(", ".join(phrases[:-1]), phrases[-1])
