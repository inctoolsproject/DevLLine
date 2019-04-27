# -*- coding: utf-8 -*-
from akad import ttypes
import json
from datetime import datetime
import os,sys,operator,threading,random

def threaded(f, daemon=False):
    import queue
    def wrapped_f(q, *args, **kwargs):
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        q = queue.Queue()
        t = threading.Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q
        return t
    return wrap

class SendObj(object):

    def sendMessage(self,to='',text=None, ct={},contentType=0):
        if to != 'reply':
            _ = ttypes.Message(to=to,text=text,contentMetadata=ct,contentType=contentType)
        else:
            _ = ttypes.Message(
                to=self.to,
                text=text,
                contentMetadata=ct,
                relatedMessageId=self.id,
                messageRelationType=3,
                relatedMessageServiceCode=1,
                contentType=contentType
            )
        return self.devl.talk.sendMessage(0,_)

    def sendContact(self,to='',mid=None):
        data = {'mid':mid if mid else self.devl.profile.mid}
        _ = ttypes.Message(
            to = to,
            contentMetadata= data,
            contentType= 13
            )
        return self.devl.talk.sendMessage(0,_)

    def sendSticker(self,to,packageId,stickerId):
        data = {'STKVER': '100','STKPKGID': packageId,'STKID': stickerId}
        _ = ttypes.Message(
            to = to,
            contentMetadata= data,
            contentType= 7
            )
        return self.devl.talk.sendMessage(0,_)
    
    def reply(self,t,ok='reply',ct={}):
        t = f'{t}'
        for i in range(0,len(t),10000):
            text = t[i:i+10000]
            if ok == 'reply':
                try:
                    ok = self.sendMessage(ok,text,ct)
                except:
                    ok = self.sendMessage(self.to,text,ct)
            else:
                ok = self.sendMessage(self.to,text,ct)
        return ok

    def m(self,*arg,**kwg):
        if len(arg) < 2 or len(arg) > 2:
            return self.reply("Invalid Method")
        data = list(arg[1]) if type(arg[1]) is dict else arg[1] if type(arg[1]) is list else [arg[1]]
        arrData = ""
        arr = []
        mention = "@DevL "
        if not data:
            return self.reply("Invalid Data")
        if "@!" in arg[0]:
            if arg[0].count("@!") != len(data):
                return self.reply(f"Invalid count @!")
            _t = arg[0].split("@!")
            _d = ''
            for m in range(len(data)):
                _d += f'{_t[m]}'
                slen = len(_d)
                elen = len(_d) + 6
                arrData = {'S':str(slen), 'E':str(elen), 'M':data[m]}
                arr.append(arrData)
                _d += mention
            _d += str(_t[len(data)])+' '
        self.reply(_d,ct={'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')})

    # Contact #
    def updateContactSetting(self, mid, flag, value):
        return self.devl.talk.updateContactSetting(0, mid, flag, value)

    def addContact(self,id=None):
        if not id:
            id = self.id
        contact = self.getContactID(id)
        if not contact:
            self.devl.findAndAddContactsByMid(id)
            return 1
        return 0

    def getContactID(self,id):
        for i in self.devl.contacts:
            if i.id == id:
                return i
        return 0

    def getGroupID(self,id):
        for i in self.devl.groups:
            if i.id == id:
                return i
        return 0

    def delContact(self,_=None):
        if _:
            self.id = _
        contact = self.getContactID(self.id)
        if contact:
            self.updateContactSetting(self.id,16,'True')
            return 1
        return 0

    def cancelgroup(self,gid='',mid=[]):
        if not gid:
            gid = self.to
        return self.devl.talk.cancelGroupInvitation(0,gid,mid if type(mid) is list else [mid])

    def rejectgroup(self,gid=''):
        if not gid:
            gid = self.to
        return self.devl.talk.rejectGroupInvitation(0,gid)

    def acceptgroup(self,gid=''):
        if not gid:
            gid = self.to
        return self.devl.talk.acceptGroupInvitation(0,gid)

    def cgroup(self,gid=''):
        if not gid:
            gid = self.to
        return self.devl.talk.getCompactGroup(gid)

    def GetID(self):
        if self.tag:
            a = [DevlContact(self.devl, contact) for contact in self.devl.getContacts(self.tag)]
            for i in a:
                i.i(self)
        else:
            if not self.toType:
                DevlContact(self.devl,self.devl.getContact(self.to)).i(self)
            elif self.toType == 2:
                import humanize
                id = self.getGroupID(self.to)
                u =  'Disable' if id.preventedJoinByTicket else f"line://ti/g/{self.devl.reissueGroupTicket(id.id)}" 
                a= f"Group Name:\n{id.name}\nGroup ID:\n{id.id}\n\nAnggota: {len(id.members)}\nInvitation: {len(id.invitee)}\nTicket:{u}\n\nCreated at:\n{humanize.naturaltime(datetime.fromtimestamp(id.waktu/1000))}\nby @!"
                self.m(a,[id.creator.id])
                self.sendContact(self.to,id.creator.id)

    def read(self):
        return self.devl.talk.sendChatChecked(0,self.to,self.id)

    @threaded
    def unsend(self,a):
        self.devl.unsendMessage(self.id)
        ok = self.set['unsend']["message"][self.to]
        nah = []
        for i in ok[::-1][:int(a)]:
            try:
                self.devl.unsendMessage(i)
            except:
                pass
            nah.append(i)
        for i in nah:
            ok.remove(i)

    @threaded
    def cpdp(self,vid='',ok='',cover='',nahh=''):
        ac = 1
        nah = self.reply(" 「 Profile 」\nPlease Wait....")
        while ac:
            try:
                if nahh:
                    a = self.devl.downloadFileURL(f'http://dl.profile.line-cdn.net/{self.devl.getProfile().pictureStatus}')
                else:
                    a = self.devl.downloadFileURL(self.image.path)
                ac = 0
            except:
                pass
        if nahh:
            import requests
            os.system(f"rm '{self.profile['backup']['icon']}'")
            os.system(f"rm '{self.profile['backup']['vid']}'")
            r = requests.get("{}".format(self.url))
            data = r.text
            data = json.loads(data)
            aa = self.devl.downloadFileURL(data['file'])
            self.devl.unsendMessage(nah.id)
            nah = self.reply(" 「 Profile 」\nType: Change Profile Video Picture\nStatus: Uploading....♪")
            self.devl.updateVideoAndPictureProfile(a,aa)
            g = " 「 Profile 」\nType: Change Profile Video Picture\nStatus: Profile Video Picture Hasbeen change♪"
            self.profile['backup']['icon'] = a
            self.profile['backup']['vid'] = aa
        elif cover:
            self.devl.updateProfileCover(a)
            g = " 「 Profile 」\nType: Change Profile Cover\nStatus: Profile Cover Hasbeen change♪"
            self.profile['cover'] = 0
        elif not vid:
            os.system(f"rm '{self.profile['backup']['icon']}'")
            self.profile['backup']['icon'] = a
            if not ok:
                self.devl.updateProfilePicture(a)
                g = " 「 Profile 」\nType: Change Profile Picture\nStatus: Profile Picture Hasbeen change♪"
                self.profile['icon'] = 0
            else:
                self.profile['cvp']['icon']['s'] = 0
                self.profile['cvp']['vid']['s'] = 1
                self.profile['cvp']['icon']['p'] = a
                g = " 「 Profile 」\nType: Change Profile Video Picture\nStatus: Sent the video♪"
        else:
            os.system(f"rm '{self.profile['backup']['vid']}'")
            self.profile['backup']['vid'] = a
            self.profile['cvp']['vid']['s'] = 0
            self.devl.updateVideoAndPictureProfile(self.profile['cvp']['icon']['p'],a)
            g = " 「 Profile 」\nType: Change Profile Video Picture\nStatus: Profile Video Picture Hasbeen change♪"
        self.devl.unsendMessage(nah.id)
        self.reply(g)

    @threaded
    def cgdp(self,mid=''):
        if mid:
            self.to = mid
        ac = 1
        while ac:
            try:
                a = self.devl.downloadFileURL(self.image.path)
                ac = 0
            except:
                pass
        self.devl.updateGroupPicture(self.to,a)
        self.reply(" 「 Group 」\nType: Change Cover Group\nStatus: Cover Group Hasbeen change♪")

    @threaded
    def clone(self,mid=''):
        if not mid:
            ok = self.getGroupID(self.to)
            if not ok:
                return self.reply('Error~')
            ok = self.devl.addMember(self.to,self.tag[0])
        else:
            ok = DevlContact(self.devl,self.devl.getContact(mid))
        if ok.picture:
            path = self.devl.downloadFileURL(ok.picture)
        else:
            return self.reply(f'Failed {ok.name} Not make a picture')
        a = self.devl.profile
        a.displayName = ok.name
        a.statusMessage = ok.bio
        try:
            b = self.devl.getProfileCoverId(ok.id)
            if b:
                self.devl.updateProfileCoverById(b)
        except:
            pass
        self.devl.updateProfile(a)
        if ok.video:
            nah = self.reply('Downloading Video Profile~')
            a = self.devl.downloadFileURL(ok.video)
            self.devl.unsendMessage(nah.id)
            nah = self.reply('Uploading Video Profile~')
            self.devl.updateVideoAndPictureProfile(path,a)
            self.devl.unsendMessage(nah.id)
            os.remove(a)
        else:
            self.devl.updateProfilePicture(path)
        os.remove(path)
        self.m('- Target: @!\n- Status: Success Copy profile♪',[ok.id])

    @threaded
    def backupclone(self,data):
        ok = DevlContact(self.devl,self.devl.getContact(self.devl.profile.mid))
        os.system(f'rm "{data["icon"]}" "{data["vid"]}"')
        data['name'] = ok.name
        data['icon'] = self.devl.downloadFileURL(ok.picture)
        data['status'] = ok.bio
        data['cover'] = self.devl.getProfileCoverId(ok.id)
        data['vid'] = ok.video
        self.reply(f"Sukses Backup\nName:{ok.name}\nStatus: {ok.bio}")
        if ok.video:
            self.devl.sendVideoWithURL_(self.to,ok.video,ok.picture)
            data['vid'] = self.devl.downloadFileURL(ok.video)
        else:
            self.devl.sendImageWithURL_(self.to,ok.picture)
        return 'Sukses'

    @threaded
    def fancyname(self,data):
        import time
        a = random.randint(0,len(data['name'])-1)
        self.devl.updateProfileAttribute(2,data['name'][a])
        data['timer'] = time.time()

    @threaded
    def clones(self,data):
        ok = DevlContact(self.devl,self.devl.getContact(self.devl.profile.mid))
        if ok.picture == data['icon']:
            return self.reply('No People Your Clone')
        a = self.devl.profile
        a.displayName = data['name']
        a.statusMessage = data['status']
        self.devl.updateProfile(a)
        self.devl.updateProfileCoverById(data['cover'])
        self.reply(f" 「 Backup Profil 」\nSukses Backup\nName:{data['name']}\nStatus: {data['status']}")
        if not data['vid']:
            self.devl.updateProfilePicture(data['icon'])
            self.devl.sendImageWithURL_(self.to,data['icon'])
        else:
            nah = self.reply('Uploading Video Profile~')
            self.devl.updateVideoAndPictureProfile(data['icon'],data['vid'])
            self.devl.unsendMessage(nah.id)
            ok = DevlContact(self.devl,self.devl.getContact(self.devl.profile.mid))
            self.devl.sendVideoWithURL_(self.to,ok.video,ok.picture)

class DevlADD(SendObj):
    def __init__(self,_,devl):
        self.to = _.param1
        self.devl = devl

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            if value != self.devl:
                L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))

class DevlGroup:
    def __init__(self, devl,_):
        self.devl = devl
        self.id = _.id
        self.name = _.name
        self.waktu = _.createdTime
        self.creator = DevlContact(devl, _.creator) if _.creator else DevlContact(devl, _.members[0])
        self.preventedJoinByTicket = _.preventedJoinByTicket
        self.ticket = None
        self.members = [DevlContact(devl, i) for i in _.members]
        self.members.sort(key=operator.attrgetter("name"))
        if _.invitee is not None:
            self.invitee = [DevlContact(devl, i) for i in _.invitee]
            self.invitee.sort(key=operator.attrgetter("name"))
        else:
            self.invitee = []

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            if value != self.devl:
                L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))

class DevlInvite(SendObj):

    def __init__(self,_, devl):
        self.devl = devl
        self.to = _.param1
        self.inviter = _.param2
        self.revision = _.revision
        self.type = _.type
        self.invites = _.param3.split('\x1e')

    def k(self):
        self.devl.kickoutFromGroup(self.to,[self.inviter])

    def a(self):
        self.devl.acceptGroupInvitation(self.to)

    def __repr__(self):
        L = ['{"%s":%r}' % (key, value) for key, value in self.__dict__.items() if value != self.devl]
        return '%s({%s})' % (self.__class__.__name__, ', '.join(L))

class DevlImage(SendObj):
    def __init__(self,_,devl):
        self.devl = devl
        self.path = 'https://obs-jp.line-apps.com/talk/m/download.nhn'
        self.ex = 'jpeg'
        if 'MEDIA_CONTENT_INFO' in _:
            a =  json.loads(_['MEDIA_CONTENT_INFO'])
            if a['extension'] == 'gif':
                self.path= self.path+f'?oid={_["id"]}&tid=original' if 'DOWNLOAD_URL' not in _ else  _['DOWNLOAD_URL']
                self.ex = 'gif'
            else:
                self.path= self.path+f'?oid={_["id"]}'  if 'DOWNLOAD_URL' not in _ else  _['DOWNLOAD_URL']
        else:
            self.path = _['DOWNLOAD_URL'] if 'DOWNLOAD_URL' in _ else f'{self.path}?oid={_["id"]}'
        self.to = _['to']

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            if value != self.devl:
                L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))

class DevlVideo(SendObj):
    def __init__(self,_,devl):
        self.devl = devl
        self.path = 'https://obs-jp.line-apps.com/talk/m/download.nhn'
        self.ex = 'mp4'
        self.path = _['DOWNLOAD_URL'] if 'DOWNLOAD_URL' in _ else f'{self.path}?oid={_["id"]}'
        self.to = _['to']

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            if value != self.devl:
                L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))

class DevlSticker:
    def __init__(self,_,devl):
        self.devl = devl
        self.id = _["STKID"]
        self.package_id = _["STKPKGID"]
        self.text = _["STKTXT"]
        self.type = "NORMAL STICKER"
        if "STKOPT" in _:
            s_type = _["STKOPT"]
            if s_type == "A":
                self.type = "ANIMATION STICKER"
            elif s_type == "PS":
                self.type = "POP UP STICKER"
            elif s_type == "S":
                self.type = "SOUND STICKER"
            elif s_type == "AS":
                self.type = "ANIMATION SOUND STICKER"
            else:
                self.type = "UNKNOWN STICKER:%s" % s_type
        self.version = _["STKVER"]

    def geturl(self):
        if self.type in ["ANIMATION STICKER","ANIMATION SOUND STICKER"]:
            return f'https://stickershop.line-scdn.net/stickershop/v1/sticker/{self.id}/IOS/sticker_animation@2x.png'
        else:
            return f'https://stickershop.line-scdn.net/stickershop/v1/sticker/{self.id}/ANDROID/sticker.png;compress=true'

    def info(self):
        return "ID:%s\nPACK_ID:%s\nVERSION:%s\nType:%s" % (self.id, self.package_id, self.version,self.type)

    def getname(self):
        return self.devl.getProduct(packageID=int(self.package_id), language='ID', country='ID').title

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            if value != self.devl:
                L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))

class DevlPesan(SendObj):

    def __init__(self,_, devl):
        self.data = _
        self.devl = devl
        self.text = _.text if _.text else None
        self.id = _.id
        self._from = _._from
        self.to = _._from if not _.toType and _._from != self.devl.profile.mid else _.to
        self.toType = _.toType
        self.cType = _.contentType
        self.Type = {'toType':ttypes.MIDType._VALUES_TO_NAMES[_.toType],'cType':ttypes.ContentType._VALUES_TO_NAMES[_.contentType]}
        self.waktu = _.createdTime
        self.cmdata = _.contentMetadata
        self.url = "http://os.line.naver.jp/os/m/%s" % _.id
        self.tag = []
        if not self.cType:
            if bool(self.cmdata):
                if "MENTION" in self.cmdata:
                    self.cmdata["MENTION"] = json.loads(self.cmdata["MENTION"])
                    self.tag = [m["M"] for m in self.cmdata["MENTION"]["MENTIONEES"]]
        elif self.cType == 7:
            nah = DevlSticker(self.cmdata,devl)
            self.cmdata['name'] = nah.getname()
            self.cmdata['url'] = nah.geturl()
            self.cmdata['type'] = 0 if nah.type == "NORMAL STICKER" else 1
        elif self.cType == 1:
            self.cmdata['to'] = self.to
            self.cmdata['id'] = self.id
            self.image = DevlImage(self.cmdata,devl)
            del self.cmdata
        elif self.cType == 2:
            self.cmdata['to'] = self.to
            self.cmdata['id'] = self.id
            self.image = DevlVideo(self.cmdata,devl)
            del self.cmdata

    def file(self,_):
        return open('txt/{}.txt'.format(_), 'r').read().title()
   
    def refresh(self,t):
        self.reply(t)
        os.system('clear')
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def steal(self,type='pict',dah=''):
        if type == 'pict':
            if not dah:
                if self.toType:
                    if self.tag:
                        a = [DevlContact(self.devl, contact) for contact in self.devl.getContacts(self.tag)]
                        h = []
                        for i in a:
                            if i.picture:
                                self.devl.sendImageWithURL_(self.to,i.picture)
                            else:
                                h.append(i.id)
                        if h:
                            self.m('{} Tidak Memiliki Profile Picture'.format(', '.join(['@!' for i in h])),h)
                    else:
                        self.devl.sendImageWithURL_(self.to,"https://obs.line-scdn.net/"+self.devl.getGroup(self.to).pictureStatus)
                else:
                    a = DevlContact(self.devl,self.devl.getContact(self.to))
                    if a.picture:
                        self.devl.sendImageWithURL_(self.to,a.picture)
                    else:
                        self.m('@! Tidak Memiliki Profile Picture',[self.to])
            else:
                i = DevlContact(self.devl,self.devl.getContact(self._from))
                if i.picture:
                    self.devl.sendImageWithURL_(self.to,i.picture)
                else:
                    self.m('@! Tidak Memiliki Profile Picture',[self._from])
        elif type == 'video':
            if not dah:
                if self.toType:
                    if self.tag:
                        a = [DevlContact(self.devl, contact) for contact in self.devl.getContacts(self.tag)]
                        h = []
                        for i in a:
                            if i.video:
                                self.devl.sendVideoWithURL_(self.to,i.video,i.picture)
                            else:
                                h.append(i.id)
                        if h:
                            self.m('{} Tidak Memiliki Video Profile Picture'.format(', '.join(['@!' for i in h])),h)
                else:
                    i = DevlContact(self.devl,self.devl.getContact(self.to))
                    if i.video:
                        self.devl.sendVideoWithURL_(self.to,i.video,i.picture)
                    else:
                        self.m('@! Tidak Memiliki Video Profile Picture',[self.to])
            else:
                i = DevlContact(self.devl,self.devl.getContact(self._from))
                if i.video:
                    self.devl.sendVideoWithURL_(self.to,i.video,i.picture)
                else:
                    self.m('@! Tidak Memiliki Video Profile Picture',[self._from])
        elif type == 'cover':
            if not dah:
                if self.toType:
                    if self.tag:
                        for i in self.tag:
                            self.devl.sendImageWithURL_(self.to,self.devl.getProfileCoverURL(i))
                else:
                    self.devl.sendImageWithURL_(self.to,self.devl.getProfileCoverURL(self.to))
            else:
                self.devl.sendImageWithURL_(self.to,self.devl.getProfileCoverURL(self._from))

    def cmd(self,key,c=1,k=0):
        key = key if type(key) is list else [key]
        text = self.text.lower()
        i = self.rname if not k else ''
        for cmd in key:
            if text[:len(i)] == i:
                if c:
                    if text == f'{i}{cmd}' or text == f'{i} {cmd}':
                        self.command = cmd if type(cmd) is list else cmd.lower()
                        self.setkey = f'{i}'  if text == f'{i}{cmd}' else f'{i} '
                        self.setkey = self.setkey.title()
                        return 1
                else:
                    if text.startswith(f'{i}{cmd}') or text.startswith(f'{i} {cmd}'):
                        t = self.text[len(i):] if text.startswith(f'{i}{cmd}') else self.text[len(i+' '):]
                        self.text = cmd if type(cmd) is list else t
                        self.command = cmd if type(cmd) is list else t.lower()
                        self.setkey = f'{i}'  if text.startswith(f'{i}{cmd}') else f'{i} '
                        self.setkey = self.setkey.title()
                        return 1

    def add(self):
        n = '   | ADD FRIEND |'
        for no,a in enumerate(self.tag,1):
            try:
                if self.addContact(a):
                    n+= f"\n{no}. @! Add to Friend"
                else:
                    n+= f'\n{no}. @! Already In FRIEND'
            except Exception as e:
                n+= f"\n{no}. @! Failed add because {e.reason}"
        self.m(n,self.tag)

    def mens(self,text,ok):
        for i in range(0,len(ok),20):
            c = '{}• {} •'.format(' '*4,text) if not i else ''
            for no,a in enumerate(ok[i:i+20],i+1):
                c+= f'\n{no}. @!'
                if text == 'Mention Me':
                    c+= f' {len(self.set["mention"]["gc"][self.to][a]["waktu"])}x'
                elif text == 'Add Mimic':
                    if a in self.set['mimic']["target"]:
                        c+= ' Already In Mimic'
                    else:
                        c+= ' Add To Mimic'
                        self.set['mimic']["target"].append(a)
                elif text == 'Del Mimic':
                    if a in self.set['mimic']["target"]:
                        self.set['mimic']["target"].remove(a)
                        c+= ' Delete From Mimic'
                    else:
                        c+= ' Not Found in Mimic'
            self.m(c.strip(),ok[i:i+20])

    @threaded
    def gcall(self,a):
        if not a:
            [self.devl.inviteIntoGroupCall(self.a.id,[self.a.members[int(i)-1].id for i in self.b],mediaType=2) for i in range(int(self.spl[2]))]
        else:
            [self.devl.inviteIntoGroupCall(a.id,[i.id for i in a.members],mediaType=2) for i in range(int(self.spl[2]))]
    
    def dom(self,*arg,**kwg):
        if not self.toType:
            return self.reply('Restriction This Feature Only in Group or Room only')
        data = [{'mid':i.id,'name':i.name} for i in self.getGroupID(self.to).members if i.id != self.devl.profile.mid] \
                    if self.toType == 2 else [{'mid':i.mid,'name':i.displayName} \
                    for i in self.devl.getRoom(self.to).contacts if i.mid != self.devl.profile.mid]
        return sorted(data, key = lambda i: i['name']) if len(arg) >= 1 else [i['mid'] for i in data]

    def lurk(self):
        data = self.set['lurk']['gc'][self.to]['member']
        lurk = []
        for i in data:
            lurk.append(DevlLurk(i,data[i]))
        lurk.sort(key=operator.attrgetter("waktu"))
        return lurk

    def mentionme(self):
        data = self.set['mention']['gc'][self.to]
        lurk = []
        for i in data:
            lurk.append(DevlMentionme(i,data[i]))
        lurk.sort(key=operator.attrgetter("waktu"))
        return lurk

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            if value != self.devl or value != self.data:
                L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))

class DevlLurk:
    def __init__(self,_,__):
        self.member = _
        self.waktu = __

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))

class DevlMentionme:
    def __init__(self,_,a):
        self.member = _
        self.waktu = list(a['waktu'])
        self.metadata = list(a['metadata'])
        self.id = list(a['mid'])
        self.pesan = list(a['pesan'])

    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))
        

class DevlContact(SendObj):
    def __init__(self,devl,_):
        self.devl = devl
        self.id = _.mid
        self.name = _.displayName if not _.displayNameOverridden else _.displayNameOverridden
        self.bio = _.statusMessage
        self.status = ttypes.ContactStatus._VALUES_TO_NAMES[_.status]
        self.relation = ttypes.ContactRelation._VALUES_TO_NAMES[_.relation]
        self.picture = "https://obs.line-scdn.net/%s" % _.pictureStatus if _.pictureStatus else None
        self.video = "https://obs.line-scdn.net/%s/vp" % _.pictureStatus if _.videoProfile else None


    def i(self,_):
        ok = f'Status:\n{self.bio}\n' if self.bio else ''
        a = f"「 ID 」\nName: @!\n{ok}User ID:\n{self.id}"
        _.m(a.strip(),self.id)
        self.sendContact(_.to,self.id)

    def c(self,_=None):
        if _:
            n = '   | DELETE FRIEND |'
            for no,a in enumerate(_.tag,1):
                try:
                    if self.delContact(a):
                        n+= f'\n{no}. @! Delete From Friend'
                    else:
                        n+= f'\n{no}. @! Failed because not your friend'
                except Exception as e:
                    n+= f'\n{no}. @! {e.reason} '
            _.m(n,_.tag)
            self.devl.rcontacts()
        else:
            try:
                if self.delContact():
                    n= f'@! Delete From Friend'
                else:
                    n= f'@! Failed because not your friend'
            except Exception as e:
                n= f'@! {e.reason} '
            return self.id,n


    def __repr__(self):
        L = {}
        for key, value in self.__dict__.items():
            if value != self.devl:
                L[key] = value
        return '%s(%s)' % (self.__class__.__name__, json.dumps(L, indent=4, sort_keys=True))