from distutils.core import setup

setup(
    name='mutapath',
    packages=['mutapath'],
    version='0.1',
    license='lgpl-3.0',
    description='Mutable Pathlib',
    author='matfax',
    author_email='matthias.fax@gmail.com',
    url='https://github.com/matfax/mutapath',
    keywords=['pathlib', 'mutable', 'path'],
    install_requires=[
        'path-py',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.7',
    ],
)
