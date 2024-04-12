from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='CRUDRepository',
    version='0.1.0',
    url='https://github.com/dellius-alexander/CRUDRepository',
    author='Dellius Alexander',
    author_email='dellius.alexander@example.com',
    description='Description of my package',
    packages=find_packages(
        include=['src', 'src.*'],
        exclude=['tests', 'tests.*', 'src.logs']
    ),
    install_requires=[

    ],
    license=Path('LICENSE').read_text(),
    long_description=Path('README.md').read_text(),
)