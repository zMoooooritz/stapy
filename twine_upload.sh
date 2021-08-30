#!/bin/sh

python3 setup.py sdist bdist_wheel
twine upload dist/* --username $1 --password $2
