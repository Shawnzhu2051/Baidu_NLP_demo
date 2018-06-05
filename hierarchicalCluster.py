# -*- coding: utf-8 -*-
import csv
import math
import numpy as np
import urllib2
import json
import requests

def getAccessToken():
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

def lexer(AT,keywordList):
    lexer_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer' + '?charset=UTF-8&access_token=' + AT
    sentensList = []
    for items in keywordList:
        lexer_word = []
        info = {
            'text': items.decode('gbk')
        }
        dic_info = json.dumps(info)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url=lexer_url, headers=headers, data=dic_info, timeout=10)
        except requests.exceptions.ReadTimeout as e:
            print('except:', e)
        except requests.exceptions.ConnectTimeout as e:
            print('except:', e)
        response = json.loads(response.content)
        for items in response['items']:
            if(items['pos'] != 'w'):
                lexer_word.append(items['item'])
        sentensList.append(lexer_word)
    return sentensList

def word_vec(AT,sentenceList):
    vec_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_vec' + '?charset=UTF-8&access_token=' + AT
    vectorList = []
    for sentence in sentenceList:
        sentence_vec = []
        for word in sentence:
            sum = []
            info = {
                'word' : word
            }
            dic_info = json.dumps(info)
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.post(url=vec_url, headers=headers, data=dic_info, timeout=10)
            except requests.exceptions.ReadTimeout as e:
                print('except:', e)
            except requests.exceptions.ConnectTimeout as e:
                print('except:', e)
            response = json.loads(response.content)
            if(response.has_key('vec')):
                sum = sum + response['vec']


if __name__ == '__main__':
    keywordList = []
    with open('hierarchicalCluster.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if float(line[1]) > 0.5:
                point = line[0]
                keywordList.append(point)
    AT = getAccessToken()
    if AT:
        sentenceList = lexer(AT,keywordList)
        sentenceVector = word_vec(AT,sentenceList)

