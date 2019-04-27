# -*- coding: utf-8 -*-
from devl.ttypes import ApplicationType
import json, requests, urllib.parse
import re

class Utils:
    _session        = requests.session()
    timelineHeaders = {}
    Headers         = {}
    LINE_BASE                   = 'https://legy-jp.line.naver.jp'
    LINE_OBS_DOMAIN             = 'https://obs-jp.line-apps.com'
    LINE_TIMELINE_API           = 'https://legy-jp.line.naver.jp/mh/api'
    LINE_TIMELINE_MH            = 'https://legy-jp.line.naver.jp/mh'

    LINE_LOGIN_QUERY_PATH       = '/api/v4p/rs'
    LINE_AUTH_QUERY_PATH        = '/api/v4/TalkService.do'

    LINE_API                    = '/S4'
    LINE_POLL_FIR               = '/P4'
    LINE_POLL_QUERY_PATH_THI    = '/F4'
    LINE_CALL                   = '/V4'
    LINE_CERTIFICATE_PATH       = '/Q'
    LINE_CHAN_QUERY_PATH        = '/CH4'
    LINE_SQUARE_QUERY_PATH      = '/SQS1'
    LINE_SHOP_QUERY_PATH        = '/SHOP4'
    LINE_LIFF_SEND              = 'https://api.line.me/v2/bot/message/push'
    LINE_LIFF_QUERY_PATH        = '/LIFF1'

    CHANNEL_ID = {
        'LINE_TIMELINE': '1341209850',
        'LINE_WEBTOON': '1401600689',
        'LINE_TODAY': '1518712866',
        'LINE_STORE': '1376922440',
        'LINE_MUSIC': '1381425814',
        'LINE_SERVICES': '1459630796'
    }

    APP_VERSION = {
        'ANDROID': '8.17.0',
        'IOS': '8.17.0',
        'ANDROIDLITE': '2.1.0',
        'BIZANDROID': '1.7.2',
        'BIZIOS': '1.7.5',
        'BIZWEB': '1.0.22',
        'DESKTOPWIN': '5.9.0',
        'DESKTOPMAC': '5.9.0',
        'IOSIPAD': '8.17.0',
        'CHROMEOS': '2.1.5',
        'WIN10': '5.5.5',
        'DEFAULT': '8.11.0'
    }

    APP_TYPE    = 'IOSIPAD'
    APP_VER     = APP_VERSION[APP_TYPE] if APP_TYPE in APP_VERSION else APP_VERSION['DEFAULT']
    CARRIER     = '51089, 1-0'
    SYSTEM_NAME = 'FDLRCN'
    SYSTEM_VER  = '8.1.0'
    IP_ADDR     = '8.8.8.8'
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def __init__(self, appType=None):
        self.Headers = {}
        self.timelineHeaders = {}
        if appType:
            self.APP_TYPE = appType
            self.APP_VER = self.APP_VERSION[self.APP_TYPE] if self.APP_TYPE in self.APP_VERSION else self.APP_VERSION['DEFAULT']
        self.APP_NAME = '%s\t%s\t%s\t%s' % (self.APP_TYPE, self.APP_VER, self.SYSTEM_NAME, self.SYSTEM_VER)
        self.USER_AGENT = 'Line/%s' % self.APP_VER


    def parseUrl(self, path):
        return self.LINE_HOST_DOMAIN + path

    def urlEncode(self, url, path, params=None):
        return url + path + '?' + urllib.parse.urlencode(params)

    def getJson(self, url, allowHeader=False):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            return json.loads(self._session.get(url, headers=self.Headers).text)

    def setHeadersWithDict(self, headersDict):
        self.Headers.update(headersDict)

    def setHeaders(self, argument, value):
        self.Headers[argument] = value

    def setTimelineHeadersWithDict(self, headersDict):
        self.timelineHeaders.update(headersDict)

    def setTimelineHeaders(self, argument, value):
        self.timelineHeaders[argument] = value

    def additionalHeaders(self, source, newSource):
        headerList={}
        headerList.update(source)
        headerList.update(newSource)
        return headerList

    def optionsContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, data=None, files=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.post(url, headers=headers, data=data, files=files)

    def getContent(self, url, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.put(url, headers=headers, data=data)
