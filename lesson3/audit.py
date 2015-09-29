#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint
from collections import defaultdict

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}

    index = list()
    fieldlist = list()
    result = defaultdict(list)
    count = 0
    getIndex = 0
    
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
       
        allTypes = list()
        for fields in reader:
    
            # get index of fields
            if getIndex == 0:
                for i in range(0,99):
                    if fields[i] in FIELDS:
                    #    print fields[i]
                        index.append(count)
                        fieldlist.append(fields[i])
                    count += 1
                getIndex = 1
             
            # get the types based on index
            elif getIndex > 4:
                for i in range(len(index)):
                    # check if it's NULL or empty
                    if fields[index[i]] == 'NULL' or fields[index[i]] == '':
                        result[fieldlist[i]].append(type(None))
                        
                    # check if it's a list
                    elif fields[index[i]][0] == "{":
                        result[fieldlist[i]].append(list)
                                  
                    else:
                        try:
                            # check if it's an int
                            intV = int(fields[index[i]])
                            result[fieldlist[i]].append(int)
                        except:
                            # check if it's a float
                            try:
                                floatV = float(fields[index[i]])
                                result[fieldlist[i]].append(float)
                            except:
                                result[fieldlist[i]].append(str)
                                
                                    
            getIndex += 1
        resultUnique = dict()

        for key,value in result.items():
            resultUnique[key] = set(result[key])
    return resultUnique


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
