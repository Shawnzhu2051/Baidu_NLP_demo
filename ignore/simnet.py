# -*- coding: utf-8 -*-

import numpy
import scipy
import urllib2
import json
import requests
import csv
import chardet
from requests.adapters import HTTPAdapter



def getAccessToken(AK,SK):
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

def getScore(point,AT):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet' + '?charset=UTF-8&access_token='
    question = "一辆汽车刹车后做匀减速运动，初速度为10m/s，加速度大小为2m/s，则汽车在6s末的速度和位移分别为"
    #print(chardet.detect(point))
    #print(chardet.detect(question))
    info = {
        "text_1": question,
        "text_2": point
    }
    dic_info = json.dumps(info)
    request_url = url + AT
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url=request_url, headers=headers, data=dic_info, timeout=10)
    except requests.exceptions.ReadTimeout as e:
        print('except:', e)
    except requests.exceptions.ConnectTimeout as e:
        print('except:', e)
    response = json.loads(response.content)
    return response['score']

if __name__ == '__main__':
    AK = 'ylCi3zhVArGU4gkS2NzAB0dr'
    SK = 'VEjH2k6stKYValgX5DjvbHVthpELMN3p'
    AT = getAccessToken(AK,SK)
    if AT:
        pointList = []
        index = 0
        with open("shortKnowledgePoint.csv", "rU") as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                point = line[0].decode('utf-8')
                if point.startswith(u'\ufeff'):
                    point = point.encode('utf-8')[3:].decode('utf-8')
                score = getScore(point, AT)
                print(index)
                index += 1
                pointList.append((point,score))
        pointList.sort(key=lambda k:k[1],reverse=True)

        with open("result.csv","w") as csvfile2:
            writer = csv.writer(csvfile2)
            fileHeader = ["Point", "relevancy"]
            writer.writerow(fileHeader)
            for items in pointList:
                print(items)
                writer.writerow([items[0].encode('gbk'), items[1]])

    else:
        print('error! No Access Token received!')


