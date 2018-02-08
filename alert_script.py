#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from simplejson import dumps

corp_id = 'wx1d3eac4738e2a42a'
agent_id = '1000002'
secret = '9ykpnjkT0zp_zymQAzjpSwsoBkISo_759FY15f1wIRc'
toparty_id = '2'

def get_token():
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='\
                   + corp_id + '&corpsecret=' + secret
    res_data = urllib2.urlopen(gettoken_url)
    res = res_data.read()
    res_dict = eval(res)
    token = res_dict.get('access_token',0)
    return token

def send_message(in_str=None):
    access_token = get_token()
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message' \
               '/send?access_token=' + access_token

    send_str = in_str if in_str \
        else '落霞与代码齐飞,\n秋水共bug一色'

    send_dict = {
        # 见开发者文档
        # https://work.weixin.qq.com/api/doc#10167
        'toparty': toparty_id,
        'agentid': agent_id,
        'msgtype': 'text',
        'text':{
            'content': str(send_str)
        }
    }

    send_data = dumps(obj=send_dict,ensure_ascii=False).encode('utf-8')



    res_data = urllib2.urlopen(url=send_url, data=send_data)
    res = res_data.read()
    res_dict = eval(res)

    result = res_dict.get('errmsg')
    if result == 'ok':
        print('告警成功')
