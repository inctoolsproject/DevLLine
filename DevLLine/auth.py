# -*- coding: utf-8 -*-
from . import cek_auth,DevL_Exception
from devl.ttypes import IdentityProvider, LoginResultType, LoginRequest, LoginType,Message
from .util import Utils
from .session import Session

import rsa, os, asyncio

class Auth(Utils):
    authToken   = ""
    certificate = ""

    def __init__(self):
        Utils.__init__(self)
        self.setHeadersWithDict({
            'User-Agent': self.USER_AGENT,
            'X-Line-Application': self.APP_NAME,
            'X-Line-Carrier': self.CARRIER,
            'x-lal': "in_ID"
        })

    def __loadSession(self):
        self.talk       = Session(self.LINE_BASE, self.Headers, self.LINE_API, self.customThrift).Talk(isopen=False)
        self.poll       = Session(self.LINE_BASE, self.Headers, self.LINE_POLL_FIR, self.customThrift).Talk()
        self.call       = Session(self.LINE_BASE, self.Headers, self.LINE_CALL, self.customThrift).Call()
        self.channel    = Session(self.LINE_BASE, self.Headers, self.LINE_CHAN_QUERY_PATH, self.customThrift).Channel()
        self.shop       = Session(self.LINE_BASE, self.Headers, self.LINE_SHOP_QUERY_PATH, self.customThrift).Shop()
        self.liff       = Session(self.LINE_BASE, self.Headers, self.LINE_LIFF_QUERY_PATH, self.customThrift).Liff()
        self.revision = self.poll.getLastOpRevision()
        self.isLogin = True                

    def __loginRequest(self, type, data):
        lReq = LoginRequest()
        if type == '0':
            lReq.type = LoginType.ID_CREDENTIAL
            lReq.identityProvider = data['identityProvider']
            lReq.identifier = data['identifier']
            lReq.password = data['password']
            lReq.keepLoggedIn = data['keepLoggedIn']
            lReq.accessLocation = data['accessLocation']
            lReq.systemName = data['systemName']
            lReq.certificate = data['certificate']
            lReq.e2eeVersion = data['e2eeVersion']
        elif type == '1':
            lReq.type = LoginType.QRCODE
            lReq.keepLoggedIn = data['keepLoggedIn']
            if 'identityProvider' in data:
                lReq.identityProvider = data['identityProvider']
            if 'accessLocation' in data:
                lReq.accessLocation = data['accessLocation']
            if 'systemName' in data:
                lReq.systemName = data['systemName']
            lReq.verifier = data['verifier']
            lReq.e2eeVersion = data['e2eeVersion']
        else:
            lReq=False
        return lReq

    def loginWithCredential(self, _id, passwd):
        if self.systemName is None:
            self.systemName=self.SYSTEM_NAME
        if self.EMAIL_REGEX.match(_id):
            self.provider = IdentityProvider.LINE       # LINE
        else:
            self.provider = IdentityProvider.NAVER_KR   # NAVER
        
        if self.appName is None:
            self.appName=self.APP_NAME
        self.setHeaders('X-Line-Application', self.appName)
        self.tauth = Session(self.LINE_BASE, self.Headers, self.LINE_AUTH_QUERY_PATH).Talk(isopen=False)

        rsaKey = self.tauth.getRSAKeyInfo(self.provider)
        
        message = (chr(len(rsaKey.sessionKey)) + rsaKey.sessionKey +
                   chr(len(_id)) + _id +
                   chr(len(passwd)) + passwd).encode('utf-8')
        pub_key = rsa.PublicKey(int(rsaKey.nvalue, 16), int(rsaKey.evalue, 16))
        crypto = rsa.encrypt(message, pub_key).hex()

        try:
            with open(_id + '.crt', 'r') as f:
                self.certificate = f.read()
        except:
            if self.certificate is not None:
                if os.path.exists(self.certificate):
                    with open(self.certificate, 'r') as f:
                        self.certificate = f.read()

        self.auth = Session(self.LINE_BASE, self.Headers, self.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)

        lReq = self.__loginRequest('0', {
            'identityProvider': self.provider,
            'identifier': rsaKey.keynm,
            'password': crypto,
            'keepLoggedIn': self.keepLoggedIn,
            'accessLocation': self.IP_ADDR,
            'systemName': self.systemName,
            'certificate': self.certificate,
            'e2eeVersion': 0
        })

        result = self.auth.loginZ(lReq)
        
        if result.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            print(result.pinCode)

            self.setHeaders('X-Line-Access', result.verifier)
            getAccessKey = self.getJson(self.parseUrl(self.LINE_CERTIFICATE_PATH), allowHeader=True)

            self.auth = Session(self.LINE_BASE, self.Headers, self.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)

            try:
                lReq = self.__loginRequest('1', {
                    'keepLoggedIn': self.keepLoggedIn,
                    'verifier': getAccessKey['result']['verifier'],
                    'e2eeVersion': 0
                })
                result = self.auth.loginZ(lReq)
            except:
                raise DevL_Exception('Login failed')
            
            if result.type == LoginResultType.SUCCESS:
                if result.certificate is not None:
                    with open(_id + '.crt', 'w') as f:
                        f.write(result.certificate)
                    self.certificate = result.certificate
                if result.authToken is not None:
                    self.loginWithAuthToken(result.authToken)
                else:
                    return False
            else:
                raise DevL_Exception('Login failed')

        elif result.type == LoginResultType.REQUIRE_QRCODE:
            self.loginWithQrCode()
            pass

        elif result.type == LoginResultType.SUCCESS:
            self.certificate = result.certificate
            self.loginWithAuthToken(result.authToken)

    def loginWithQrCode(self,to=None,client=None):
        if self.systemName is None:
            self.systemName=self.SYSTEM_NAME
        if self.appName is None:
            self.appName=self.APP_NAME
        self.setHeaders('X-Line-Application', self.appName)

        self.tauth = Session(self.LINE_BASE, self.Headers, self.LINE_AUTH_QUERY_PATH).Talk(isopen=False)
        qrCode = self.tauth.getAuthQrcode(self.keepLoggedIn, self.systemName)
        if to:
            client.talk.sendMessage(0,Message(to=to,text='line://au/q/' + qrCode.verifier))
        else:
            print('line://au/q/' + qrCode.verifier)
        self.setHeaders('X-Line-Access', qrCode.verifier)

        getAccessKey = self.getJson(self.parseUrl(self.LINE_CERTIFICATE_PATH), allowHeader=True)
        
        self.auth = Session(self.LINE_BASE, self.Headers, self.LINE_LOGIN_QUERY_PATH).Auth(isopen=False)
        
        try:
            lReq = self.__loginRequest('1', {
                'keepLoggedIn': self.keepLoggedIn,
                'systemName': self.systemName,
                'identityProvider': IdentityProvider.LINE,
                'verifier': getAccessKey['result']['verifier'],
                'accessLocation': self.IP_ADDR,
                'e2eeVersion': 0
            })
            result = self.auth.loginZ(lReq)
        except:
            raise DevL_Exception('Login failed')

        if result.type == LoginResultType.SUCCESS:
            if result.authToken is not None:
                if not to:
                    self.loginWithAuthToken(result.authToken)
                else:
                    return result.authToken
            else:
                return False
        else:
            raise DevL_Exception('Login failed')
          
    def loginWithAuthToken(self, authToken=None):
        if authToken is None:
            raise DevL_Exception('Please provide Auth Token')
        if self.appName is None:
            self.appName=self.APP_NAME
        self.setHeadersWithDict({
            'X-Line-Application': self.appName,
            'X-Line-Access': authToken
        })
        self.authToken = authToken
        self.__loadSession()

    def __defaultCallback(self, str):
        print(str)

    def logout(self):
        self.auth.logoutZ()

    @cek_auth
    def run(self):
        try:
            ops = []
            operations = self.poll.fetchOperations(self.revision,100)
            for op in operations:
                ops.append(op)
                self.revision = max(op.revision, self.revision)
            return ops
        except EOFError:
            return []