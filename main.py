# -*- coding: utf-8 -*-
from __future__ import division
import csv
import math
import numpy as np
import urllib2
import json
import requests
from sklearn.cluster import AgglomerativeClustering

def getAccessToken():
    print('Get Access Token')
    AK = 'ylCi3zhVArGU4gkS2NzAB0dr'
    SK = 'VEjH2k6stKYValgX5DjvbHVthpELMN3p'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + AK + '&client_secret=' + SK
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    ATresponse = urllib2.urlopen(request)
    content = ATresponse.read()
    if(content):
        dic_json = json.loads(content)
        AT = dic_json['access_token']
        return AT
    else:
        return False

def lexer(AT,pointList):
    print('Start lexer')
    lexer_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer' + '?charset=UTF-8&access_token=' + AT
    sentenceList = []
    count = 0
    for items in pointList:
        lexer_word = []
        info = {
            'text': items[0]
        }
        dic_info = json.dumps(info)
        headers = {'Content-Type': 'application/json'}
        while(1):
            try:
                response = requests.post(url=lexer_url, headers=headers, data=dic_info, timeout=10)
                break
            except requests.exceptions.ReadTimeout as e:
                print('except:', e)
            except requests.exceptions.ConnectTimeout as e:
                print('except:', e)
        response = json.loads(response.content)
        for items in response['items']:
            if(items['pos'] != 'w'):
                lexer_word.append(items['item'])
        sentenceList.append(lexer_word)
        count += 1
        print(count)
    print('lexer end')
    return sentenceList

def word_vec(AT,lexeredPointList):
    print('Compute word vector')
    vec_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_vec' + '?charset=UTF-8&access_token=' + AT
    vectorList = []
    count = 0
    for sentence in lexeredPointList:
        sentence_vec = []
        for word in sentence:
            info = {
                'word' : word
            }
            dic_info = json.dumps(info)
            headers = {'Content-Type': 'application/json'}
            while(1):
                try:
                    response = requests.post(url=vec_url, headers=headers, data=dic_info, timeout=10)
                    break
                except requests.exceptions.ReadTimeout as e:
                    print('except:', e)
                except requests.exceptions.ConnectTimeout as e:
                    print('except:', e)
            response = json.loads(response.content)
            if(response.has_key('vec')):
                sentence_vec = vector_sum(sentence_vec,response['vec'])
        vectorList.append(normalization(sentence_vec))
        print(count)
        count += 1
    print('Compute word vec end')
    return vectorList

def vector_sum(vector1, vector2):
    result = []
    if len(vector1) == 0:
        return vector2
    else:
        for index in range(len(vector1)):
            result.append(vector1[index] + vector2[index])
        return result

def normalization(vector):
    max_num = max(vector)
    min_num = min(vector)
    result = []
    for nums in vector:
        ans = (nums - min_num)/(max_num - min_num)
        result.append(ans)
    return result

def hierarchical(pointList,sentenceVector):
    print('Start cluster')
    k = 3
    label0List = []
    label1List = []
    label2List = []
    Cluster = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward', compute_full_tree='false')
    result = Cluster.fit_predict(sentenceVector)
    for index in range(len(result)):
        if (result[index] == 0):
            label0List.append(pointList[index])
        elif (result[index] == 1):
            label1List.append(pointList[index])
        elif (result[index] == 2):
            label2List.append(pointList[index])
    print('End cluster')
    return computeAveFindMax(label0List,label1List,label2List)

def getScore(point,AT):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet' + '?charset=UTF-8&access_token='
    question = "一辆汽车刹车后做匀减速运动，初速度为10m/s，加速度大小为2m/s，则汽车在6s末的速度和位移分别为"
    info = {
        "text_1": question,
        "text_2": point
    }
    dic_info = json.dumps(info)
    request_url = url + AT
    headers = {'Content-Type': 'application/json'}
    while(1):
        try:
            response = requests.post(url=request_url, headers=headers, data=dic_info, timeout=10)
            break
        except requests.exceptions.ReadTimeout as e:
            print('except:', e)
        except requests.exceptions.ConnectTimeout as e:
            print('except:', e)
    response = json.loads(response.content)
    if response.has_key('score'):
        return response['score']
    else:
        return 0

def computeAveFindMax(label0List,label1List,label2List):
    result0 = 0
    result1 = 0
    result2 = 0
    for dict in label0List:
        result0 += dict[1]
    result0 = result0/len(label0List)
    for dict in label1List:
        result1 += dict[1]
    result1 = result1/len(label1List)
    for dict in label2List:
        result2 += dict[1]
    result2 = result2/len(label2List)
    if(result0 > result1 and result0 > result2):
        return label0List
    if(result1 > result0 and result1 > result2):
        return label1List
    if(result2 > result0 and result2 > result1):
        return label2List


if __name__ == '__main__':
    AT = getAccessToken()
    if AT:
        count = 0
        pointList = []
        with open('shortKnowledgelist.csv', 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                pointStr = "".join(line)
                points = pointStr.decode('gbk')
                if points.startswith(u'\ufeff'):
                    points = points.encode('utf-8')[3:].decode('utf-8')
                score = getScore(points, AT)
                count += 1
                print(count)
                if score > 0.5:
                    pointList.append((points, score))
        pointList.sort(key=lambda k: k[1], reverse=True)
        lexeredPointList = lexer(AT,pointList)
        sentenceVector = word_vec(AT,lexeredPointList)
        targetPointList = hierarchical(pointList,sentenceVector)
        print('---------------------------')
        print('输入的试题为：')
        print('一辆汽车刹车后做匀减速运动，初速度为10m/s，加速度大小为2m/s，则汽车在6s末的速度和位移分别为')
        print('该题涉及的知识点为：')
        for targetPoint in targetPointList:
            print(targetPoint[0].encode('utf-8'))

