import json
from pathlib import Path
from typing import List, Optional

from setuptools import setup, find_packages


def get_dependencies(pipfile_lock: Optional[str] = None, develop: bool = False):
    if pipfile_lock is None:
        pipfile_lock = Path("Pipfile.lock")
    lock_data = json.load(pipfile_lock.open())
    result: List[str] = [package_name for package_name in lock_data.get('default', {}).keys()]
    if develop:
        result += [package_name for package_name in lock_data.get('default', {}).keys()]
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
    setup_requires=["setuptools-git-version"],
    install_requires=get_dependencies("../Pipfile.lock", develop=True) + get_dependencies(develop=True),
    python_requires=">=3.7"
)
