import json
from pathlib import Path
from typing import List

from setuptools import setup, find_packages


def get_dependencies(pipfile_lock=None):
    if pipfile_lock is None:
        pipfile_lock = Path("Pipfile.lock")
    lock_data = json.load(pipfile_lock.open())
    result: List[str] = [package_name for package_name in lock_data.get('default', {}).keys()]
    for k in result:
        if "path-py" in k:
            new_key = k.replace("path-py", "path.py")
            result.remove(k)
            result.append(new_key)
    return result


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
