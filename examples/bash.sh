#!/bin/sh

# set the url of the STA instance
stapy -u "http://localhost:8080/FROST-Server/v1.1/"

# post / add a new ObservedProperty with the given values
stapy -a ObservedProperty TestPropName TestPropDesc TestPropDef properties="{\"TestPropKey\": \"TestPropValue\"}"

# change the name of the ObservedProperty with ID 1
stapy -p ObservedProperty 1 name=TestPropNewName

# delete all ObservedProperties with the name 'TestPropNewName'
stapy -d "/ObservedProperties?\$filter=substringof('TestPropNewName', name)"
