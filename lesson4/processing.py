#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a list of dictionaries of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc. If there is a singular synonym, the value should still be formatted
  in a list.
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
  * Note that the value associated with the classification key is a dictionary with
    taxonomic labels.
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def process_file(filename, fields):

    process_fields = fields.keys()
    
    # get a new dictionary for classification 
    global classificationList
    classificationList = ['family_label', 'class_label', 'phylum_label', 'order_label', 'kingdom_label', 'genus_label'] 
 
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()  
        
        for line in reader: 
            c = dict()
            o = dict()
            
            for key in FIELDS.keys():  
                # is it a comment?
                #print key
                content = line[key] 
                if key == 'rdf-schema#comment' or key == 'family_label':
                    isClassification(key, c, o)[FIELDS[key]] = content         
                                 
                # check if name is NULL or contain non-alphabetic characters
                elif key == 'name':
                    if content == "NULL" or len(re.sub('[^0-9a-zA-Z]+','',content)) != len(content):
                        o[FIELDS[key]] = line['rdf-schema#label']
                    else:
                        if content.find(' ') == -1:
                            o[FIELDS[key]] = content
                        else: 
                            # check if the second word starts with (
                            sep = content.split(' ')
                            if sep[1][0] == '(':
                                o[FIELDS[key]] = sep[0]
                            else: 
                                o[FIELDS[key]] = content
                # check if othe field is NULL
                elif content == "NULL":
                    isClassification(key, c, o)[FIELDS[key]] =  None
        
                # check if it's actually a list
                elif key == 'synonym':
                    if content.find("|") != -1:
                        separated = content.split("|")
                        separated[0] = separated[0][1:]
                        separated[len(separated)-1] = separated[len(separated)-1][:-1]
                        o[FIELDS[key]] =  separated
                    else:
                        # get single synonum into a list 
                        t = list()
                        t.append(content)
                        o[FIELDS[key]] = t
                        
                # is it a list?  
                elif content.find(' ') != -1:
                    isClassification(key, c, o)[FIELDS[key]] = content[0:content.find(' ')]
                    
                else:
                    isClassification(key, c, o)[FIELDS[key]] = content
            o['classification']=c
            data.append(o)
   # print data[0]
    return data
        
def isClassification(key, classDict, otherDict):
    if key in classificationList:
        return classDict
    else:
        return otherDict
        
def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None, 
        "name": "Argiope", 
        "classification": {
            "kingdom": "Animal", 
            "family": "Orb-weaver spider", 
            "order": "Spider", 
            "phylum": "Arthropod", 
            "genus": None, 
            "class": "Arachnid"
        }, 
        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
        "label": "Argiope", 
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
    test()