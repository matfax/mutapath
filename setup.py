from pathlib import Path

from setuptools import setup, find_packages

from docs.setup_helper import get_dependencies

setup(
    name="mutapath",
    packages=find_packages(),
    version_config={
        "version_format": "{tag}",
        "starting_version": "0.1.0"
    },
    license="lgpl-3.0",
    description="Mutable Pathlib",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="matfax",
    author_email="matthias.fax@gmail.com",
    url="https://github.com/matfax/mutapath",
    keywords=["pathlib", "mutable", "path"],
    setup_requires=["better-setuptools-git-version"],
    install_requires=get_dependencies(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.7"
)
