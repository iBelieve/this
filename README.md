# This - Standardized project tool

[![Travis branch](https://img.shields.io/travis/iBelieve/this/master.svg?style=for-the-badge)](https://travis-ci.org/iBelieve/this)
[![PyPI](https://img.shields.io/pypi/v/this-cli.svg?style=for-the-badge)](https://pypi.org/project/this-cli/)
[![PyPI - License](https://img.shields.io/pypi/l/this-cli.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/maintenance/yes/2018.svg?style=for-the-badge)]()

`this` provides a standardized and simplified interface for running
many common project tasks, such as building, running, testing, and
deploying. It supports many project types, including Node.js, Python,
Autotools, Meson, and CMake.

By providing a standard set of commands, the goal is to ease the
burden of having to remember or look up the exact commands to run for
specific projects. In addition, `this` will run multiple commands as
necessary to accomplish a given task. For example, building an
autotools-based project will run `./autogen.sh`, `./configure`, then
`make`, while a meson-based project will run `meson` and then `ninja`
in the build directory. `this` even supports projects with multiple
run commands using `tmux` split panes, such as a Laravel project with
a PHP backend and an React or Vue frontend.

The goal of `this` is not to provide every possible feature or
command, but only to wrap a subset of commands common to most
projects. For more advanced commands, use the actual commands that
`this` wraps.

### Installation and Usage

`this` is currently available via pip3 (Python 3-only):

    pip3 install this-cli

For Arch Linux users, `this` is also available from the
[AUR](https://aur.archlinux.org/packages/this/) and can be installed
with any AUR helper, such as [yay](https://github.com/Jguer/yay):

    yay -S this

To use on a project, you can directly invoke `this` with one of the commands
listed below, or run `this` with no arguments to see what project type
is detected and what subset of the commands are available:

    > this
	Node.js project using Yarn (deployed using Ansible)

	Available commands:
	  build
	  lint
	  test
	  check
	  run
	  deploy

To see what steps `this` will run for a given command, use the `--dry-run` flag:

    > this --dry-run deploy
	$ ansible-galaxy install -r ansible/requirements.yml
	$ ansible-playbook -i ansible/inventory ansible/playbook.yml

### Supported Project Formats

 - .NET Core
 - Ansible
 - Autotools
 - CMake
 - Gradle
 - Laravel
 - Makefile
 - Meson
 - Node.js
 - Python
 - Rust/Cargo

You can also run `this --help` to see the latest list of supported
project types.

### Supported Commands

 - build
 - lint
 - test
 - check (usually lint + test combined)
 - run
 - deploy

### License

Licensed under the [MIT license](https://opensource.org/licenses/MIT).
