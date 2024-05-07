"""
This module is used for packaging the CRUDRepository project.
"""
from setuptools import setup, find_packages
from pathlib import Path

# --------------------------------------------------------------
setup(
    name="crud_repository",
    url="https://github.com/dellius-alexander/CRUDRepository.git",
    author="Dellius Alexander",
    author_email="dalexander@hyfisolutions.com",
    description="The CRUDRepository is a Python project designed to provide a generic implementation of Create, Read, Update, and Delete (CRUD) operations for various databases.",
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*", "dist", "build", "logs"]
    ),
    long_description=Path("README.md").read_text(encoding="utf-8"),
    package_dir={
        "crud_repository": "crud_repository"
    },
)

