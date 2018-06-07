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
    keyword = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_sim?charset=UTF-8&access_token='
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ AK +'&client_secret='+ SK
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    ATresponse = urllib2.urlopen(request)
    content = ATresponse.read()
    if (content):
        dic_json = json.loads(content)
        AT = dic_json['access_token']
        info = {
            "word_1":"平抛运动",
            "word_2":"直线运动"
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