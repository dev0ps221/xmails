#!/usr/bin/env python3
import getpass

from krypt import code as kode,d_code as dkode
credspath = 'craids/list'

def get_creds_files():
    

def ask_creds():
    user = ask_and_code('user')
    pwd =  ask_and_code()
    return user,pwd

def ask_and_code(val='pwd'):
    if val == 'user':
        raw = input("Email:")
        ret = (raw,kode(raw))
    else:
        ret = kode(getpass.getpass())
    return ret 

def decode_creds_file(credsfile):
    file_ = open(credsfile,'r')
    usr,pwd = file_.read().split('<=>')
    print(dkode(usr),dkode(pwd))

def generate_creds_file(filename=None,gui=False,page=None):
    if not gui:
        usr,pwd = ask_creds()
    if usr and pwd:
        filename = f"{credspath}/{usr[0]}.xcreds" if not filename else filename
        file_ = open(filename,'w')
        file_.write(f"{usr[1]}<=>{pwd}")
        file_.close()
        return filename
    else:
        print('no creds supplied...')
        return 
        
if(__name__ == '__main__'):
    credsfile = generate_creds_file()