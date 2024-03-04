import os
from setuptools import setup, find_packages, find_namespace_packages
from codes import relative_quest
import sys
# version-keeping codes based on pybedtools
curdir = os.path.abspath(os.path.dirname(__file__))
MAJ = 0
MIN = 0
REV = 1
VERSION = '%d.%d.%d' % (MAJ, MIN, REV)

#sys.path.append(curdir)

with open(os.path.join(curdir, 'version.py'), 'w') as fout:
        fout.write(
            "\n".join(["",
                       "# THIS FILE IS GENERATED FROM SETUP.PY",
                       "version = '{version}'",
                       "__version__ = version"]).format(version=VERSION)
        )


setup(
    name='relative_quest',
    version=VERSION,
    description='Gene Gents - CSE 284 Group 1 Final Project',
    author='Gene Gents (Group 1)',
    packages=find_namespace_packages(),
    entry_points={
        "console_scripts": [
            "relative_quest=codes.relative_quest:main"
        ],
    },
)