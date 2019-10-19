from setup_helper import get_dependencies
from setuptools import setup, find_packages

setup(
    name="mutapath",
    packages=find_packages(),
    version_format="{tag}",
    license="lgpl-3.0",
    setup_requires=["setuptools-git-version"],
    install_requires=get_dependencies(develop=True),
    python_requires=">=3.7"
)
