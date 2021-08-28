# stapy
[![Latest Release](https://img.shields.io/github/release/zMoooooritz/STAPy.svg)](https://github.com/zMoooooritz/STAPy/releases)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/zMoooooritz/STApy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/zMoooooritz/STApy/context:python)

This is an easy to use SensorThings API Client written in python

The SensorThings API is an OGC standard for IoT device sensing data.

## Installation

TODO

## Usage

STAPy does currently support 3 different ways of interaction.

### Interactive

The interactive mode is the easiest one to use but can **not** be used programmatically.
This mode can be invoked in the following way.
```bash
python main.py -i
```
Currently it does only support `POST` and `DELETE` requests.

### CLI

The *normal* command line mode can be easier automated.
```bash
python main.py --help
```
Should give sufficient information on how two use it properly.
As the interactive mode it does only support `POST` and `DELETE` requests so far.

### API

This is the Python interface to the SensorThings API.
It can be used from within python scripts, following are some examples:

The relevant classes can be found within the `sta` sub-module.

The following syntax can be used to create new entities.
```python
>>> from stapy import Post

>>> Post.new_observed_property("TestProp", "TestProp-Desc", "TestProp-Def")
```

To get the data from the STA the procedure is split in two parts.
First the request-URL needs to be constructed and afterwards the data can be received:
```python
>>> from stapy import Query, Entity

>>> query = Query(Entity.Sensor).select("result").order("phenomenonTime").limit(10).get_query()

>>> JSONExtract(query).select(JSONSelect.attribute("result").get_selector()).get_data_sets()
```

## Development
To build this project, run `python setup.py build`. To run the unit tests, run `python setup.py test`