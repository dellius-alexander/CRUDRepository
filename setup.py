"""
This module is used for packaging the CRUDRepository project.
"""

from setuptools import setup, find_packages
from pathlib import Path
import toml


with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as fh:
    REQUIREMENTS = fh.read()

with open("LICENSE", "r") as fh:
    LICENSE = fh.read()

with open("VERSION", "r") as fh:
    VERSION = fh.read()

# Load the pyproject.toml file
pyproject_toml = toml.load(Path(__file__).parent / "pyproject.toml")

# Extract the metadata from the pyproject.toml file
metadata = pyproject_toml["tool"]["poetry"]

setup(
    name=metadata["name"],
    version=metadata["version"],
    url=metadata["homepage"],
    author=metadata["authors"][0],
    author_email=metadata["authors"][0].split("<")[1].replace(">", ""),
    description=metadata["description"],
    packages=find_packages(
        include=["src", "src.*"], exclude=["tests", "tests.*", "src.logs"]
    ),
    install_requires=[],
    license=Path("LICENSE").read_text(encoding="utf-8"),
    long_description=Path("README.md").read_text(encoding="utf-8"),
)