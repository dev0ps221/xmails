from os import listdir,getcwd
from base64 import b64encode as b_encode,b64decode as b_decode

class CredsInstance:
    creds = {}
    def __init__(self,credsfile,manager):
        self.manager = manager
        self.set_credsfile(credsfile)
        self.set_data()

    def set_data(self):
        self.usr,self.pwd = self.manager.decode_creds_file(self.get_credsfile())
        self.set_creds()
    
    def set_creds(self):
        self.set_cred('user',self.usr)
        self.set_cred('pass',self.pwd)

    def set_credsfile(self,credsfile):
        self.credsfile = credsfile

    def get_credsfile(self):
        return self.credsfile

    def get_cred(self,cred):
        return self.get_creds()[cred] if cred in self.get_creds()  else None

    def set_cred(self,cred,val):
        self.creds[cred] = val
        return self.creds[cred]
    def get_creds(self):
        return self.creds

class CredsManager:
    _s = None
    credspath = '/'.join(__file__.split('/')[:-2])+"/craids/list" 
    credsfiles = []
    credsprofiles = []
    credsinstances = {}

    def __init__(self):
        sfile_ = open(f"{self.get_credspath()}/../_sfile",'r')
        self.set_s(int(sfile_.read()))
        self.update_creds_stuff()

    def set_credspath(self):
        self.credspath = getcwd()+"/craids/list"
        if not path.isdir(self.credspath):
            from os import mkdir
            mkdir(self.credspath)

    def get_credspath(self):
        return self.credspath

    def get_s(self):
        return self._s

    def set_s(self,s):
        self._s = s

    def _Ccode(self,ncDPattern):
        CcdPattern = ""
        for char in ncDPattern: 
            char = ord(f"{char}")+self.get_s()
            CcdPattern = f"{CcdPattern}{b_encode('h4ck'.encode()).decode()}{char}"
        return CcdPattern

    def _Ncode(self,pattern):
        ncDPattern = b_encode(pattern.encode())
        return self._Ccode(ncDPattern.decode())

    def _NDcode(self,Ccdpattern):
        ncDPattern = self._CDcode(Ccdpattern)
        pattern = b_decode(ncDPattern.encode()).decode()
        return pattern

    def _CDcode(self,ncdPattern):
        pattern = ""
        for char in ncdPattern.split(b_encode('h4ck'.encode()).decode()):
            if(char):
                pattern = f"{pattern}{chr(int(char)-self.get_s())}"
        return pattern
        
    def kode(self,pattern):
        return self._Ncode(pattern)

    def dkode(self,pattern):
        return self._NDcode(pattern)

    def has_credsext(self,filename):
        return filename if len(filename) > 7 and filename[-7:] == '.xcreds' else None 

    def isnt_none(self,pattern):
        return pattern 

    def cred_file_at(self,idx):
        return self.credsfiles[idx] if len(self.credsfiles>idx) else None

    def set_cred_file(self,credfile):
        self.credsfiles.append(credfile)
        return self.credsfiles

    def set_creds_files(self):
        filelist = listdir(self.get_credspath())
        for credfile in filter(self.isnt_none,map(self.has_credsext,filelist)):
            self.set_cred_file(credfile)

    def get_creds_files(self):
        return self.credsfiles

    def get_creds_file(self,profile):
        credsfiles = self.get_creds_files()
        def matches(filename):
            return f"{profile}.xcreds" == filename
        match_ = [elem for elem in filter(matches,credsfiles)]
        return f"{self.get_credspath()}/{match_[0]}" if len(match_) else None

    def set_creds_profiles(self):
        for profile in self.get_creds_files():
            self.credsprofiles.append(profile.replace('.xcreds',''))
        return self.credsprofiles

    def get_creds_profiles(self):
        return self.credsprofiles

    def set_creds_instances(self):
        for profile in self.get_creds_profiles():
            self.set_creds_instance(profile)
        return self.get_creds_instances()

    def get_creds_instances(self):
        return self.credsinstances

    def set_creds_instance(self,profile):  
        self.credsinstances[profile] = CredsInstance(self.get_creds_file(profile),self)

    def get_creds_instance(self,profile):
        ret = self.set_creds_instances().get(profile)
        return CredsInstance(self.get_creds_file(profile),self) if ret else ret

    def ask_profile(self):
        return input("profile:")

    def ask_creds(self):
        user = ask_and_code('user')
        pwd =  ask_and_code()
        return user,pwd

    def ask_and_code(self,val='pwd'):
        if val == 'user':
            raw = input("Email:")
            ret = (raw,kode(raw))
        else:
            ret = kode(getpass.getpass())
        return ret 

    def decode_creds_file(self,credsfile):
        file_ = open(credsfile,'r')
        usr,pwd = file_.read().split('<=>')
        file_.close()
        return self.dkode(usr),self.dkode(pwd)

    def generate_creds_file(self,filename=None,gui=False,page=None,usr=None,pwd=None):
        if not usr and not pwd:
            if not gui:
                usr,pwd = self.ask_creds()
            else:
                print('error, no creds supplied')
        else:
            usr = usr,self.kode(usr)
            pwd = self.kode(pwd)
        if usr and pwd:
            filename = f"{self.get_credspath()}/{usr[0]}.xcreds" if not filename else filename
            file_ = open(filename,'w')
            file_.write(f"{usr[1]}<=>{pwd}")
            file_.close()
            self.update_creds_stuff()
            return filename
        else:
            print('no creds supplied...')
            return 

    def update_creds_stuff(self):
        self.set_creds_files()
        self.set_creds_profiles()
        self.set_creds_instances()

    def get_creds(self,profile=None):
        if profile and profile in self.get_creds_profiles():
            return CredsInstance(self.get_creds_file(profile),self) 
        else :
            print('sorry, but the requested profile {} doesnt exist'.format(profile))
            return None
