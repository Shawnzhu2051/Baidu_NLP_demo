# -*- coding: utf-8 -*-
from __future__ import division
import csv
import math
import numpy as np
import urllib2
import json
import requests
from sklearn.cluster import AgglomerativeClustering


if __name__ == '__main__':
    sentenceList = np.loadtxt(open("sentenceVector.csv","rb"),delimiter=",",skiprows=0)
    k = 3
    Cluster = AgglomerativeClustering(n_clusters=k,affinity='euclidean',linkage='ward',compute_full_tree='false')
    result = Cluster.fit_predict(sentenceList)
    print(result)
    print(Cluster.labels_)
    print(Cluster.n_leaves_)
    print(Cluster.n_components_)
    print(Cluster.children_)
