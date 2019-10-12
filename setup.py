from pathlib import Path

from setuptools import setup, find_packages

setup(
    name='mutapath',
    packages=find_packages(),
    version_format='{tag}',
    license='lgpl-3.0',
    description='Mutable Pathlib',
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author='matfax',
    author_email='matthias.fax@gmail.com',
    url='https://github.com/matfax/mutapath',
    keywords=['pathlib', 'mutable', 'path'],
    setup_requires=[
        'setuptools-git-version',
        'green',
        'wheel',
    ],
    install_requires=[
        'path.py',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.7',
    ],
)
