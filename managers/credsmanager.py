from os import listdir

class CredsManager:
    credspath 
    credsfiles = []
    credsprofiles = []

    def __init__(self,credspath):
        self.credspath = credspath
            
    def has_credsext(self,filename):
        return filename if len(filename) > 7 and filename[-7:] == '.xcreds' else None 

    def isnt_none(pattern):
        return pattern 

    def cred_file_at(self,idx):
        return self.credsfiles[idx] if len(self.credsfiles>idx) else None


    def set_cred_file(self,credfile):
        self.credsfiles.append(credfile)
        return self.credsfiles

    def set_creds_files(self):
        filelist = listdir(credspath)
        for credfile in filter(self.isnt_none,map(self.has_credsext,filelist)):
            self.set_cred_file(credfile)

    def get_creds_files(self):
        return self.credsfiles

    def get_creds_file(self,profile):
        credsfiles = get_creds_files()
        def matches(filename):
            return f"{profile}.xcreds" == filename
        match_ = [elem for elem in filter(matches,credsfiles)]
        return f"{credspath}/{match_[0]}" if len(match_) else None

    def set_creds_profiles(self):
        for profile in get_creds_files():
            self.credsprofiles.append(profile.replace('.xcreds',''))
        return self.credsprofiles

    def get_creds_profiles(self):
        return self.credsprofiles

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
        return dkode(usr),dkode(pwd)

    def generate_creds_file(self,filename=None,gui=False,page=None,usr=None,pwd=None):
        if not usr and not pwd:
            if not gui:
                usr,pwd = ask_creds()
            else:
                print('error, no creds supplied')
        else:
            usr = usr,kode(usr)
            pwd = kode(pwd)
        if usr and pwd:
            filename = f"{credspath}/{usr[0]}.xcreds" if not filename else filename
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

    def get_creds(self,profile=None):
        if not profile:
            print('to which is the username do want to get related creds')
            profile = input('answer>')
        if profile in get_creds_profiles():
            return decode_creds_file(get_creds_file(profile)) 
        else :
            print('sorry, but the requested profile {} doesnt exist'.format(profile))
            return None
        
    