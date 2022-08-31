#!/usr/bin/env python3
import getpass

from krypt import code as kode,d_code as dkode

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

def generate_creds_file(filename,gui=False,page=None):
    if not gui:
        usr,pwd = ask_creds()
        file_ = open(filename,'w')
        file_.write(f"{usr}<=>{pwd}")
        file_.close()
if(__name__ == '__main__'):
    print('generate a new credsfile')
    credsfile = input("output filename:")
    generate_creds_file(credsfile)
    decode_creds_file(credsfile)        