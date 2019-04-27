# -*- coding: utf-8 -*-
from . import DevL_Exception,cek_auth,Message,threaded,Pesan

class Talk(Message):
    isLogin = False
    _messageReq = {}
    _unreplyReq = 0

    def __init__(self):
        Message.__init__(self)
        self.isLogin = True

    """User"""

    @cek_auth
    def acquireEncryptedAccessToken(self, featureType=2):
        return self.talk.acquireEncryptedAccessToken(featureType)

    @cek_auth
    def getProfile(self):
        return self.talk.getProfile()

    @cek_auth
    def getSettings(self):
        return self.talk.getSettings()

    @cek_auth
    def getUserTicket(self):
        return self.talk.getUserTicket()

    @cek_auth
    def generateUserTicket(self):
        try:
            ticket = self.getUserTicket().id
        except:
            self.reissueUserTicket()
            ticket = self.getUserTicket().id
        return ticket

    @cek_auth
    def updateProfile(self, profileObject):
        return self.talk.updateProfile(0, profileObject)

    @cek_auth
    def updateSettings(self, settingObject):
        return self.talk.updateSettings(0, settingObject)

    @cek_auth
    def updateProfileAttribute(self, attrId, value):
        return self.talk.updateProfileAttribute(0, attrId, value)

    @cek_auth
    def updateContactSetting(self, mid, flag, value):
        return self.talk.updateContactSetting(0, mid, flag, value)

    @cek_auth
    def deleteContact(self, mid):
        return self.updateContactSetting(mid, 16, 'True')

    @cek_auth
    def renameContact(self, mid, name):
        return self.updateContactSetting(mid, 2, name)

    @cek_auth
    def addToFavoriteContactMids(self, mid):
        return self.updateContactSetting(mid, 8, 'True')

    @cek_auth
    def addToHiddenContactMids(self, mid):
        return self.updateContactSetting(mid, 4, 'True')

    """Operation"""

    @cek_auth
    def getLastOpRevision(self):
        return self.poll.getLastOpRevision()

    """Message"""

    @cek_auth
    def getRecentMessageV2(self, chatId, count=1001):
        return self.talk.getRecentMessagesV2(chatId,count)

    @cek_auth
    def reply(
        self,
        to='',
        text=None,
        ct={},
        contentType=0,
        reply=0
    ):
        if reply:
            self.relatedMessageId = f'{reply}'
            self.messageRelationType = 3
            self.relatedMessageServiceCode = 1
        self.to = to
        self.text = text
        self.contentMetadata = ct
        self.contentType = contentType
        o = self.talk.sendMessage(0,self)
        return Pesan(o.__dict__)

    @cek_auth
    def unsendMessage(self, messageId):
        self._unsendMessageReq += 1
        return self.talk.unsendMessage(self._unsendMessageReq, messageId)

    @cek_auth
    def urlEncode(self, url):
        import base64
        return base64.b64encode(url.encode()).decode('utf-8')

    @cek_auth
    def urlDecode(self, Encodeurl):
        import base64
        return base64.b64decode(Encodeurl.encode()).decode('utf-8')

    @cek_auth
    def requestResendMessage(self, senderMid, messageId):
        return self.talk.requestResendMessage(0, senderMid, messageId)

    @cek_auth
    def respondResendMessage(self, receiverMid, originalMessageId, resendMessage, errorCode):
        return self.talk.respondResendMessage(0, receiverMid, originalMessageId, resendMessage, errorCode)

    @cek_auth
    def removeMessage(self, messageId):
        return self.talk.removeMessage(messageId)
    
    @cek_auth
    def removeAllMessages(self, lastMessageId):
        return self.talk.removeAllMessages(0, lastMessageId)

    @cek_auth
    def removeMessageFromMyHome(self, messageId):
        return self.talk.removeMessageFromMyHome(messageId)

    @cek_auth
    def destroyMessage(self, chatId, messageId):
        return self.talk.destroyMessage(0, chatId, messageId, sessionId)

    @cek_auth
    def sendEvent(self, messageObject):
        return self.talk.sendEvent(0, messageObject)

    @cek_auth
    def getLastReadMessageIds(self, chatId):
        return self.talk.getLastReadMessageIds(0, chatId)

    @cek_auth
    def getPreviousMessagesV2WithReadCount(self, messageBoxId, endMessageId, messagesCount=50):
        return self.talk.getPreviousMessagesV2WithReadCount(messageBoxId, endMessageId, messagesCount)

    """Contact"""
        
    @cek_auth
    def blockContact(self, mid):
        return self.talk.blockContact(0, mid)

    @cek_auth
    def unblockContact(self, mid):
        return self.talk.unblockContact(0, mid)

    @cek_auth
    def findAndAddContactByMetaTag(self, userid, reference):
        return self.talk.findAndAddContactByMetaTag(0, userid, reference)

    @cek_auth
    def findAndAddContactsByMid(self, mid):
        return self.talk.findAndAddContactsByMid(0, mid, 0, '')

    @cek_auth
    def findAndAddContactsByEmail(self, emails=[]):
        return self.talk.findAndAddContactsByEmail(0, emails)

    @cek_auth
    def findAndAddContactsByUserid(self, userid):
        return self.talk.findAndAddContactsByUserid(0, userid)

    @cek_auth
    def findContactsByUserid(self, userid):
        return self.talk.findContactByUserid(userid)

    @cek_auth
    def findContactByTicket(self, ticketId):
        return self.talk.findContactByUserTicket(ticketId)

    @cek_auth
    def getAllContactIds(self):
        return self.talk.getAllContactIds()

    @cek_auth
    def getBlockedContactIds(self):
        return self.talk.getBlockedContactIds()

    @cek_auth
    def getContact(self, mid):
        return self.talk.getContact(mid)

    @cek_auth
    def getContacts(self, midlist):
        return self.talk.getContacts(midlist)

    @cek_auth
    def getFavoriteMids(self):
        return self.talk.getFavoriteMids()

    @cek_auth
    def getHiddenContactMids(self):
        return self.talk.getHiddenContactMids()

    @cek_auth
    def tryFriendRequest(self, midOrEMid, friendRequestParams, method=1):
        return self.talk.tryFriendRequest(midOrEMid, method, friendRequestParams)

    @cek_auth
    def makeUserAddMyselfAsContact(self, contactOwnerMid):
        return self.talk.makeUserAddMyselfAsContact(contactOwnerMid)

    @cek_auth
    def getContactWithFriendRequestStatus(self, id):
        return self.talk.getContactWithFriendRequestStatus(id)

    @cek_auth
    def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        return self.talk.reissueUserTicket(expirationTime, maxUseCount)

    """Group"""

    @cek_auth
    def getChatRoomAnnouncementsBulk(self, chatRoomMids):
        return self.talk.getChatRoomAnnouncementsBulk(chatRoomMids)

    @cek_auth
    def getChatRoomAnnouncements(self, chatRoomMid):
        return self.talk.getChatRoomAnnouncements(chatRoomMid)

    @cek_auth
    def createChatRoomAnnouncement(self, chatRoomMid, type, contents):
        return self.talk.createChatRoomAnnouncement(0, chatRoomMid, type, contents)

    @cek_auth
    def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
        return self.talk.removeChatRoomAnnouncement(0, chatRoomMid, announcementSeq)

    @cek_auth
    def getGroupWithoutMembers(self, groupId):
        return self.talk.getGroupWithoutMembers(groupId)
    
    @cek_auth
    def findGroupByTicket(self, ticketId):
        return self.talk.findGroupByTicket(ticketId)

    @cek_auth
    def acceptGroupInvitation(self, groupId):
        return self.talk.acceptGroupInvitation(0, groupId)

    @cek_auth
    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self.talk.acceptGroupInvitationByTicket(0, groupId, ticketId)

    @cek_auth
    def cancelGroupInvitation(self, groupId, contactIds):
        return self.talk.cancelGroupInvitation(0, groupId, contactIds)

    @cek_auth
    def createGroup(self, name, midlist):
        return self.talk.createGroup(0, name, midlist)

    @cek_auth
    def getGroup(self, groupId):
        return self.talk.getGroup(groupId)

    @cek_auth
    def getGroups(self, groupIds):
        return self.talk.getGroups(groupIds)

    @cek_auth
    def getGroupsV2(self, groupIds):
        return self.talk.getGroupsV2(groupIds)

    @cek_auth
    def getCompactGroup(self, groupId):
        return self.talk.getCompactGroup(groupId)

    @cek_auth
    def getCompactRoom(self, roomId):
        return self.talk.getCompactRoom(roomId)

    @cek_auth
    def getGroupIdsByName(self, groupName):
        gIds = []
        for gId in self.getGroupIdsJoined():
            g = self.getCompactGroup(gId)
            if groupName in g.name:
                gIds.append(gId)
        return gIds

    @cek_auth
    def getGroupIdsInvited(self):
        return self.talk.getGroupIdsInvited()

    @cek_auth
    def getGroupIdsJoined(self):
        return self.talk.getGroupIdsJoined()

    @cek_auth
    def updateGroupPreferenceAttribute(self, groupMid, updatedAttrs):
        return self.talk.updateGroupPreferenceAttribute(0, groupMid, updatedAttrs)

    @cek_auth
    def inviteIntoGroup(self, groupId, midlist):
        return self.talk.inviteIntoGroup(0, groupId, midlist)

    @cek_auth
    def kickoutFromGroup(self, groupId, midlist):
        return self.talk.kickoutFromGroup(0, groupId, midlist)

    @cek_auth
    def leaveGroup(self, groupId):
        return self.talk.leaveGroup(0, groupId)

    @cek_auth
    def rejectGroupInvitation(self, groupId):
        return self.talk.rejectGroupInvitation(0, groupId)

    @cek_auth
    def reissueGroupTicket(self, groupId):
        return self.talk.reissueGroupTicket(groupId)

    @cek_auth
    def updateGroup(self, groupObject):
        return self.talk.updateGroup(0, groupObject)

    """Room"""

    @cek_auth
    def createRoom(self, midlist):
        return self.talk.createRoom(0, midlist)

    @cek_auth
    def getRoom(self, roomId):
        return self.talk.getRoom(roomId)

    @cek_auth
    def inviteIntoRoom(self, roomId, midlist):
        return self.talk.inviteIntoRoom(0, roomId, midlist)

    @cek_auth
    def leaveRoom(self, roomId):
        return self.talk.leaveRoom(0, roomId)

    """Call"""
        
    @cek_auth
    def acquireCallTalkRoute(self, to):
        return self.talk.acquireCallRoute(to)
    
    """Report"""

    @cek_auth
    def reportSpam(self, chatMid, memberMids=[], spammerReasons=[], senderMids=[], spamMessageIds=[], spamMessages=[]):
        return self.talk.reportSpam(chatMid, memberMids, spammerReasons, senderMids, spamMessageIds, spamMessages)
        
    @cek_auth
    def reportSpammer(self, spammerMid, spammerReasons=[], spamMessageIds=[]):
        return self.talk.reportSpammer(spammerMid, spammerReasons, spamMessageIds)