# -*- coding: utf-8 -*-
from __future__ import division
import csv
import codecs
import math
import numpy as np
import urllib2
import json
import requests


if __name__ == '__main__':
    pointList = []
    with open('knowledgeTree.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            for index in range(len(line)):
                if line[index] == '' and line[index-1] != '':
                    pointList.append(line[index-1])

    with open('knowledgeList.csv','w') as csvfile2:
        writer = csv.writer(csvfile2)
        csvfile2.write(codecs.BOM_UTF8)
        for items in pointList:
            print(items)
            writer.writerow(items)
