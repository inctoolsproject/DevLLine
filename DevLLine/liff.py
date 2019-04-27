# -*- coding: utf-8 -*-
from . import LiffChatContext,LiffContext,LiffViewRequest,cek_auth
from random import randint

import json, ntpath, requests

class Liff(object):
    isLogin = False

    def __init__(self):
        self.isLogin = True
        self.liffUrl = 'https://api.line.me/message/v3/share'
        self.__loginLiff()

    @cek_auth
    def __loginLiff(self):
        url = 'https://access.line.me/dialog/api/permissions'
        data = {
            'on': [
                'P',
                'CM'
            ],
            'off': []
        }
        headers = {
            'X-Line-Access': self.authToken,
            'X-Line-Application': self.APP_NAME,
            'X-Line-ChannelId': '1606644641',
            'Content-Type': 'application/json'
        }
        r = requests.post(url,headers=headers,data=json.dumps(data))
        return r

    @cek_auth
    def __LIFF(self,to,data=None):
        az = LiffChatContext(to)
        ax = LiffContext(chat=az)
        lf = LiffViewRequest('1606644641-DAwvRm5p', ax)
        _  = self.liff.issueLiffView(lf)
        a  = {'Content-Type': 'application/json','Authorization': 'Bearer %s' % _.accessToken}
        r = requests.post(self.liffUrl,headers=a,data=json.dumps(data))
        return r

    @cek_auth
    def liffReply(self, to=None,data=None):
        data    = {'messages': [json.loads(str(data))]}
        return self.__LIFF(to,data)