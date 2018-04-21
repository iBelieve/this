# This - Universal do-thingy

`this` provides a standardized and simplified interface for running
many common project tasks, such as building, running, testing, and
deploying. It supports many project types, including Node.js, Python,
Autotools, Meson, and CMake.

By providing a standard set up commands, the goal is to ease the
burden of having to remember or look up the exact commands to run for
specific projects. In addition, `this` will run multiple commands as
necessary to accomplish a given task. For example, building an
autotools-based project will run `./autogen.sh`, `./configure`, then
`make`, while a meson-based project will run `meson` and then `ninja`
in the build directory.

### Installation

    pip install this-cli

### Supported Project Formats

 - Autotools
 - CMake
 - Meson
 - Node.js
 - Python

### Supported Commands

 - build
 - lint
 - test
 - check (usually lint + test combined)
 - run
 - deploy

### License

Licensed under the [MIT license](https://opensource.org/licenses/MIT).
