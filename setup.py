from setuptools import setup, find_packages
from io import open
from os import path
import re

VERSIONFILE = "stapy/version.py"
verstrline = open(VERSIONFILE).read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {VERSIONFILE}.")

# get the dependencies
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]

def test_suite():
    import unittest

    suite = unittest.TestLoader().discover("tests")
    return suite

setup(
    name="stapy",
    version=verstr,
    description="A Python module to interact with the SensorThings API",
    license="MIT",
    keywords="gis geography ogc data sensor",
    author="Moritz Biering",
    author_email="moritzbiering.mb@gmail.com",
    url="https://github.com/zMoooooritz/stapy/",
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=install_requires,
    test_suite="setup.test_suite",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Database :: Front-Ends"
    ]
)
