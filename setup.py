import os
from pathlib import Path

from requirementslib import Lockfile
from setuptools import setup, find_packages

lockfile = Lockfile.create(os.getcwd())

setup(
    name="mutapath",
    packages=find_packages(),
    version_format="{tag}",
    license="lgpl-3.0",
    description="Mutable Pathlib",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="matfax",
    author_email="matthias.fax@gmail.com",
    url="https://github.com/matfax/mutapath",
    keywords=["pathlib", "mutable", "path"],
    setup_requires=["setuptools-git-version"],
    install_requires=lockfile.as_requirements(dev=False),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
