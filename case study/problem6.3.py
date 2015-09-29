#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    global tagDict
    tagDict = dict()
    in_dictionary_or_not(tagDict, root.tag)
    for child in root: 
        in_dictionary_or_not(tagDict, child.tag)
        for i in child:
            in_dictionary_or_not(tagDict, i.tag)
    return tagDict
 
def in_dictionary_or_not(dic, text):
    if text not in dic.keys():
        dic[text] = 1
    else:
        dic[text] += 1
        


def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()