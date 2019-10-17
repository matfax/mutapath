from pathlib import Path

from setuptools import setup, find_packages

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
    install_requires=[
        "cached-property==1.5.1",
        "filelock==3.0.12",
        "importlib-metadata==0.23",
        "more-itertools==7.2.0",
        "path-py==12.0.0",
        "zipp==0.6.0",
    ],
    dependency_links=[],
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
