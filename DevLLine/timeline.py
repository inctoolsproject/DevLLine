# -*- coding: utf-8 -*-
from . import cek_auth
import json, time, base64

class Timeline:

    def __init__(self):
        if not self.channelId:
            self.channelId = self.CHANNEL_ID['LINE_TIMELINE']
        self.__loginChannel()
        self.__loginTimeline()

    def __loginTimeline(self):
        self.setTimelineHeadersWithDict({
            'Content-Type': 'application/json',
            'User-Agent': self.USER_AGENT,
            'X-Line-Mid': self.profile.mid,
            'X-Line-Carrier': self.CARRIER,
            'X-Line-Application': self.APP_NAME,
            'X-Line-ChannelToken': self.channelResult.channelAccessToken
        })
        self.profileDetail = self.getProfileDetail()

    @cek_auth
    def getFeed(self, postLimit=10, commentLimit=1, likeLimit=1, order='TIME'):
        params = {'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'order': order}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/feed/list.json', params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def getHomeProfile(self, mid=None, postLimit=10, commentLimit=1, likeLimit=1):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'LINE_PROFILE_COVER'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/post/list.json', params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def getProfileDetail(self, mid=None):
        if mid is None:
            mid = self.profile.mid
        params = {'userMid': mid}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v1/userpopup/getDetail.json', params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def updateProfileCoverById(self, objId):
        params = {'coverImageId': objId}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/home/updateCover.json', params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def getProfileCoverId(self, mid=None):
        if mid is None:
            mid = self.profile.mid
        home = self.getProfileDetail(mid)
        return home['result']['objectId']

    @cek_auth
    def getProfileCoverURL(self, mid=None):
        if mid is None:
            mid = self.profile.mid
        home = self.getProfileDetail(mid)
        params = {'userid': mid, 'oid': home['result']['objectId']}
        return self.urlEncode(self.LINE_OBS_DOMAIN, '/myhome/c/download.nhn', params)

    @cek_auth
    def createPost(self, text, holdingTime=None):
        params = {'homeId': self.profile.mid, 'sourceType': 'TIMELINE'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/post/create.json', params)
        payload = {'postInfo': {'readPermission': {'type': 'ALL'}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
        if holdingTime != None:
            payload["postInfo"]["holdingTime"] = holdingTime
        data = json.dumps(payload)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def sendPostToTalk(self, mid, postId):
        if mid is None:
            mid = self.profile.mid
        params = {'receiveMid': mid, 'postId': postId}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/post/sendPostToTalk.json', params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def createComment(self, mid, postId, text):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/comment/create.json', params)
        data = {'commentText': text, 'activityExternalId': postId, 'actorId': mid}
        data = json.dumps(data)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def deleteComment(self, mid, postId, commentId):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/comment/delete.json', params)
        data = {'commentId': commentId, 'activityExternalId': postId, 'actorId': mid}
        data = json.dumps(data)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def likePost(self, mid, postId, likeType=1001):
        if mid is None:
            mid = self.profile.mid
        if likeType not in [1001,1002,1003,1004,1005,1006]:
            raise Exception('Invalid parameter likeType')
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/like/create.json', params)
        data = {'likeType': likeType, 'activityExternalId': postId, 'actorId': mid}
        data = json.dumps(data)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def unlikePost(self, mid, postId):
        if mid is None:
            mid = self.profile.mid
        params = {'homeId': mid, 'sourceType': 'TIMELINE'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/like/cancel.json', params)
        data = {'activityExternalId': postId, 'actorId': mid}
        data = json.dumps(data)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def createGroupPost(self, mid, text):
        payload = {'postInfo': {'readPermission': {'homeId': mid}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
        data = json.dumps(payload)
        r = self.postContent(self.LINE_TIMELINE_API + '/v45/post/create.json', data=data, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def createGroupAlbum(self, mid, name):
        data = json.dumps({'title': name, 'type': 'image'})
        params = {'homeId': mid,'count': '1','auto': '0'}
        url = self.urlEncode(self.LINE_TIMELINE_MH, '/album/v3/album.json', params)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Create a new album failure.')
        return True

    @cek_auth
    def deleteGroupAlbum(self, mid, albumId):
        params = {'homeId': mid}
        url = self.urlEncode(self.LINE_TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.deleteContent(url, headers=self.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Delete album failure.')
        return True

    @cek_auth
    def getGroupPost(self, mid, postLimit=10, commentLimit=1, likeLimit=1):
        params = {'homeId': mid, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'TALKROOM'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/post/list.json', params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def getGroupAlbum(self, mid):
        params = {'homeId': mid, 'type': 'g', 'sourceType': 'TALKROOM'}
        url = self.urlEncode(self.LINE_TIMELINE_MH, '/album/v3/albums.json', params)
        r = self.getContent(url, headers=self.timelineHeaders)
        return r.json()

    @cek_auth
    def changeGroupAlbumName(self, mid, albumId, name):
        data = json.dumps({'title': name})
        params = {'homeId': mid}
        url = self.urlEncode(self.LINE_TIMELINE_MH, '/album/v3/album/%s' % albumId, params)
        r = self.putContent(url, data=data, headers=self.timelineHeaders)
        if r.status_code != 201:
            raise Exception('Change album name failure.')
        return True

    @cek_auth
    def addImageToAlbum(self, mid, albumId, path):
        file = open(path, 'rb').read()
        params = {
            'oid': int(time.time()),
            'quality': '90',
            'range': len(file),
            'type': 'image'
        }
        hr = self.additionalHeaders(self.timelineHeaders, {
            'Content-Type': 'image/jpeg',
            'X-Line-Mid': mid,
            'X-Line-Album': albumId,
            'x-obs-params': self.genOBSParams(params,'b64')
        })
        r = self.getContent(self.LINE_OBS_DOMAIN + '/album/a/upload.nhn', data=file, headers=hr)
        if r.status_code != 201:
            raise Exception('Add image to album failure.')
        return r.json()

    @cek_auth
    def getImageGroupAlbum(self, mid, albumId, objId, returnAs='path', saveAs=''):
        if saveAs == '':
            saveAs = self.genTempFile('path')
        if returnAs not in ['path','bool','bin']:
            raise Exception('Invalid returnAs value')
        hr = self.additionalHeaders(self.timelineHeaders, {
            'Content-Type': 'image/jpeg',
            'X-Line-Mid': mid,
            'X-Line-Album': albumId
        })
        params = {'ver': '1.0', 'oid': objId}
        url = self.urlEncode(self.LINE_OBS_DOMAIN, '/album/a/download.nhn', params)
        r = self.getContent(url, headers=hr)
        if r.status_code == 200:
            self.saveFile(saveAs, r.raw)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download image album failure.')
    def createPostGroup(self, text,to, holdingTime=None,textMeta=[]):
        params = {'homeId': to, 'sourceType': 'GROUPHOME'}
        url = self.urlEncode(self.LINE_TIMELINE_API, '/v45/post/create.json', params)
        payload = {'postInfo': {'readPermission': {'type': 'ALL'}}, 'sourceType': 'GROUPHOME', 'contents': {'text': text,'textMeta':textMeta}}
        if holdingTime != None:
            payload["postInfo"]["holdingTime"] = holdingTime
        data = json.dumps(payload)
        r = self.postContent(url, data=data, headers=self.timelineHeaders)
        return r.json()

    def __loginChannel(self):
        self.isLogin = True
        self.channelResult  = self.approveChannelAndIssueChannelToken(self.channelId)

    @cek_auth
    def getChannelResult(self):
        return self.channelResult

    @cek_auth
    def approveChannelAndIssueChannelToken(self, channelId):
        return self.channel.approveChannelAndIssueChannelToken(channelId)

    @cek_auth
    def issueChannelToken(self, channelId):
        return self.channel.issueChannelToken(channelId)

    @cek_auth
    def getChannelInfo(self, channelId, locale='ID'):
        return self.channel.getChannelInfo(channelId, locale)

    @cek_auth
    def revokeChannel(self, channelId):
        return self.channel.revokeChannel(channelId)