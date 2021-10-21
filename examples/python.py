#!/usr/bin/env python

# from stapy import set_api_url, Post, Patch, Delete, Query, Entity
from stapy import *

# set the url of the STA instance
set_api_url("http://localhost:8080/FROST-Server/v1.1/")

# post / add a new ObservedProperty with the given values
op_id = Post.observed_property("TestPropName", "TestPropDesc", "TestPropDef", properties={"TestPropKey": "TestPropValue"})

# change the name of the ObservedProperty with ID op_id
Patch.observed_property(op_id, name="TestPropNewName")

# retrieve the id of all ObservedProperties with the name 'TestPropNewName'
ids = Query(Entity.ObservedProperty).select("@iot.id").filter("substringof('TestPropNewName', name)").get_data_sets()
# print(ids)

# delete all ObservedProperties with the name 'TestPropNewName'
# Delete.query("/ObservedProperties?$filter=substringof('TestPropNewName', name)")
