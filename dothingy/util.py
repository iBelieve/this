import os
import os.path


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
