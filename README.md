# stapy
[![Latest Release](https://img.shields.io/github/release/zMoooooritz/stapy.svg)](https://github.com/zMoooooritz/stapy/releases)
[![Build Status](https://github.com/zMoooooritz/stapy/workflows/build/badge.svg)](https://github.com/zMoooooritz/stapy/actions)
[![Python Version](https://img.shields.io/pypi/pyversions/stapy.svg)](https://pypi.org/project/stapy/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/zMoooooritz/stapy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/zMoooooritz/stapy/context:python)
[![Codecov](https://codecov.io/gh/zMoooooritz/stapy/branch/master/graph/badge.svg?token=04D52OK2H4)](https://codecov.io/github/zMoooooritz/stapy?branch=master)

This is an easy to use SensorThings API Client written in Python

The SensorThings API (STA) is an [OGC](https://www.osgeo.org/partners/ogc/) standard for IoT device sensing data.\
A server implementation of the STA can be found here [FROST](https://github.com/FraunhoferIOSB/FROST-Server).\
For more (advanced) information about the SensorThings API see the official OGC [documentation](http://developers.sensorup.com/docs).

## Installation

`stapy` is compatible with Python 3.7+ and the recommended way to install is via [pip](https://pip.pypa.io/en/stable/)
```bash
pip install stapy
```

## Usage

`stapy` can be used both form the command line (in two different ways) and as a Python library.

### STA_URL

At first it is necessary to set the URL of the STA.
Optionally it is also possible to set credentials for a basic authentication.
Within the CLI this can be achieved as follows:
```bash
stapy -u {URL}
stapy -c {USR} {PWD}
```
`stapy` can of course be also run as a Python module(`python -m stapy`)
\
\
The URL and credentials can also be set from within a Python script:
```python
>>> import stapy

>>> stapy.set_sta_url({URL})
>>> stapy.set_credentials({USR}, {PWD})
```


### CLI - Interactive

The interactive mode is the easiest one to use but can **not** be used programmatically.
Therefore it is probably a good starting point to get familiar with the STA.
The interactive mode can be invoked in the following way.
```bash
stapy -i
```
Currently it does support `POST`, `PATCH` and `DELETE` requests.

### CLI - Normal

The *normal* command line mode is a bit more difficult to use but can be automated.
```bash
stapy --help
```
Should give sufficient information on how two use it properly.
As the interactive mode it does support `POST`, `PATCH` and `DELETE` requests.

### Library

This is the Python interface to the SensorThings API (stapy is meant to be used as Python library).
Therefore it supports all requests (`POST`, `PATCH`, `DELETE` and `GET`).

The relevant classes can be found within the files `entity.py`, `delete.py`, `post.py`, `patch.py` and `query.py` in the [sta](https://github.com/zMoooooritz/stapy/tree/master/stapy/sta) sub-module.

The following syntax can be used to create new entities:
```python
>>> from stapy import Post

>>> Post.observed_property("TestProp", "TestProp-Desc", "TestProp-Def")
```
To understand which arguments are available and mandatory it is advisable to have a look at the [STA-Docs](https://developers.sensorup.com/docs/) and/or use the interactive mode of stapy.

Following is one example of a `GET` request:
```python
>>> from stapy import Query, Entity

>>> results, times = Query(Entity.Observation).select("result", "phenomenonTime").order("result").get_data_sets()
```
`results` afterwards contains **all** results of the present Observations in ascending order.\
`times` contains the respective times for the results.

stapy does support all `GET` query options that are available for the [STA](https://developers.sensorup.com/docs/#queryparameters).
Some examples are select, filter, orderby and skip. These can be chained together as seen in the example above.
\
\
Further use-cases and applications can be found in the [examples](https://github.com/zMoooooritz/stapy/tree/master/examples).

## Development
To build this project, run `python setup.py build`. To execute the unit tests, run `python setup.py test`.
