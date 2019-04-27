# -*- coding: utf-8 -*-
from .auth import Auth
from .talk import Talk
from .timeline import Timeline
from .liff import Liff

class DEVL_LINE(Auth,Talk,Timeline,Liff):

    def __init__(self, idOrAuthToken=None, passwd=None, **kwargs):
        """
        :param idOrAuthToken: Login email, token. Default: None
        :param passwd: Login password. Default: None
        :param kwargs: See below
        :Keyword Arguments:
            - **certificate**: Line certificate after email login. Default: None
            - **systemName**: System name when first login. Default: None
            - **appType**: Application type to login. Default: None
            - **appName**: Application name to login. Default: None
            - **showQr**: Print out qr code. Default: False
            - **channelId**: Channel ID to login Timeline. Default: None
            - **keepLoggedIn**: Keep logged in if succesfull login. Default: True
            - **customThrift**: Increase speed thrift with custom thrift. Default: False
        :return:
        """
        self.certificate = kwargs.pop('certificate', None)
        self.systemName = kwargs.pop('systemName', None)
        self.to = kwargs.pop('to', None)
        self.client = kwargs.pop('client', None)
        self.appType = kwargs.pop('appType', None)
        self.appName = kwargs.pop('appName', None)
        self.showQr = kwargs.pop('showQr', False)
        self.channelId = kwargs.pop('channelId', None)
        self.keepLoggedIn = kwargs.pop('keepLoggedIn', True)
        self.customThrift = kwargs.pop('customThrift', True)
        Auth.__init__(self)
        if not (idOrAuthToken or idOrAuthToken and passwd):
            if self.to:
                self.nah = self.loginWithQrCode(to=self.to,client=self.client)
            else:
                self.loginWithQrCode()
        if idOrAuthToken and passwd:
            self.loginWithCredential(idOrAuthToken, passwd)
        elif idOrAuthToken and not passwd:
            self.loginWithAuthToken(idOrAuthToken)
        self.__initAll()

    def __initAll(self):
        if not self.to:
            self.profile    = self.talk.getProfile()
            self.userTicket = self.generateUserTicket()
            Talk.__init__(self)
            Timeline.__init__(self)
            Liff.__init__(self)