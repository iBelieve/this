import fastentrypoints
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='this-cli',
    version='0.3',
    description='Standardized project tool for running common tasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michael Spencer',
    author_email='sonrisesoftware@gmail.com',
    url='https://github.com/ibelieve/this',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    setup_requires=[
        'setuptools>=38.6.0',
        'pytest-runner'
    ],
    tests_require=['pytest', 'pytest-mock'],
    entry_points='''
        [console_scripts]
        this=thiscli:cli
    ''',
)
