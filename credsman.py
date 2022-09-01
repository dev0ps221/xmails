#!/usr/bin/env python3
import getpass

from krypt import code as kode,d_code as dkode
credspath = 'craids'
def ask_creds():
    user = ask_and_code('user')
    pwd =  ask_and_code()
    return user,pwd

def ask_and_code(val='pwd'):
    if val == 'user':
        ret = kode(input("Email:"))
    else:
        ret = kode(getpass.getpass())
    return ret 

def decode_creds_file(credsfile):
    file_ = open(credsfile,'r')
    usr,pwd = file_.read().split('<=>')
    print(dkode(usr),dkode(pwd))

def generate_creds_file(gui=False,page=None):
    if not gui:
        usr,pwd = ask_creds()
        filename = f"{credspath}/{usr}.xcreds"
        file_ = open(filename,'w')
        file_.write(f"{usr}<=>{pwd}")
        file_.close()
        return filename
if(__name__ == '__main__'):
    credsfile = generate_creds_file()
    decode_creds_file(credsfile)        