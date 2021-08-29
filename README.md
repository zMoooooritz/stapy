# stapy
[![Latest Release](https://img.shields.io/github/release/zMoooooritz/stapy.svg)](https://github.com/zMoooooritz/stapy/releases)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/zMoooooritz/stapy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/zMoooooritz/stapy/context:python)

This is an easy to use SensorThings API Client written in Python

The SensorThings API (STA) is an [OGC](https://www.osgeo.org/partners/ogc/) standard for IoT device sensing data.\
A server implementation of the STA can be found here [FROST](https://github.com/FraunhoferIOSB/FROST-Server)

## Installation

TODO

## Usage

stapy can be used both form the command line (in two different ways) and as a Python library.

### CLI - Interactive

The interactive mode is the easiest one to use but can **not** be used programmatically.
Therefore it is porbably good starting point to get familiar with the STA.
The interactive mode can be invoked in the following way.
```bash
python -m stapy -i
```
Currently it does only support `POST` and `DELETE` requests. (`PATCH` will be added)
`GET` are not supported but can be used within a web-browser.

### CLI - Normal

The *normal* command line mode is a bit more difficult to use but can be automated.
```bash
python -m stapy --help
```
Should give sufficient information on how two use it properly.
As the interactive mode it does currently only support `POST` and `DELETE` requests.

### Library

This is the Python interface to the SensorThings API (stapy is meant to be used as Python library).

The relevant classes can be found within the files `entity.py`, `post.py` and `query.py` in the `sta` sub-module.

The following syntax can be used to create new entities:
```python
>>> from stapy import Post

>>> Post.new_observed_property("TestProp", "TestProp-Desc", "TestProp-Def")
```
To understand which arguments are available and mandatory it is advisable to have a look at the [STA-Docs](https://developers.sensorup.com/docs/) and/or use the interactive mode stapy.

Following is one example for a `GET` request:
```python
>>> from stapy import Query, Entity

>>> results, times = Query(Entity.Observation).select("result", "phenomenonTIme").order("result").get_data_sets()
```
`results` afterwards contains **all** results of the present Observations in ascending order.\
`times` contains the respective times for the results.

stapy does support all query options that are available for the [STA](https://developers.sensorup.com/docs/#queryparameters).
Some examples are select, filter, orderby and skip. These can be chained together as seen in the example above.

## Development
To build this project, run `python setup.py build`. To run the unit tests, run `python setup.py test`
