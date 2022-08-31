#!/usr/bin/env python3

from krypt import code as kode,d_code as dkode

def ask_creds():
    user = ask_and_code('user')
    pwd =  ask_and_code()
    return user,pwd

def ask_and_code(val):
    return kode(getpass.getuser()) if val = 'user' else kode(getpass.getpass())

def generate_creds_file(gui=False,page=None):
    if not gui:
        usr,pwd = ask_creds()
        print(usr,pwd)
        