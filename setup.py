from setuptools import setup, find_packages

setup(
    name='dothingy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points='''
        [console_scripts]
        this=dothingy:cli
    ''',
)
