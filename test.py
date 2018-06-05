# -*- coding: utf-8 -*-

import numpy
import scipy
import urllib2
import json
import requests

if __name__ == '__main__':
    dic_json = {}
    AK = 'ylCi3zhVArGU4gkS2NzAB0dr'
    SK = 'VEjH2k6stKYValgX5DjvbHVthpELMN3p'
    keyword = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=UTF-8&access_token='
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ AK +'&client_secret='+ SK
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    ATresponse = urllib2.urlopen(request)
    content = ATresponse.read()
    if (content):
        dic_json = json.loads(content)
        AT = dic_json['access_token']
        info = {
            "text_1": '一辆汽车刹车后做匀减速运动，初速度为10m/s，加速度大小为2m/s，则汽车在6s末的速度和位移分别为',
            "text_2": '判断系统吸放热、做功情况和内能变化情况'
        }
        dic_info = json.dumps(info)
        keyword_url = keyword + AT
        print(keyword_url)
        headers = {'Content-Type':'application/json'}
        response = requests.post(url=keyword_url, headers=headers, data=dic_info)
        print(keyword_url)
        #print(response.content)
        response = json.loads(response.content)
        print(response)

    else:
        print('error! No Access Token received!')