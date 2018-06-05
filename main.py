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
    keyword = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword?charset=UTF-8&access_token='
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ AK +'&client_secret='+ SK
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    ATresponse = urllib2.urlopen(request)
    content = ATresponse.read()
    if (content):
        dic_json = json.loads(content)
        AT = dic_json['access_token']
        info = {"title":"iphone手机出现“白苹果”原因及解决办法，用苹果手机的可以看下",
	            "content": "如果下面的方法还是没有解决你的问题建议来我们门店看下成都市锦江区红星路三段99号银石广场24层01室。在通电的情况下掉进清水，这种情况一不需要拆机处理。尽快断电。用力甩干，但别把机器甩掉，主意要把屏幕内的水甩出来。如果屏幕残留有水滴，干后会有痕迹。^H3 放在台灯，射灯等轻微热源下让水分慢慢散去。"}
        dic_info = json.dumps(info)
        keyword_url = keyword + AT
        headers = {'Content-Type':'application/json'}
        response = requests.post(url=keyword_url, headers=headers, data=dic_info)
        print(keyword_url)
        #print(response.content)
        response = json.loads(response.content)
        #print(response)
        for tags in response['items']:
            print(tags['tag'])
            print(tags['score'])

    else:
        print('error! No Access Token received!')