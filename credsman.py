#!/usr/bin/env python3
import getpass

from krypt import code as kode,d_code as dkode
from os import path

credspath = 'craids/list'

if not path.isdir(credspath):
    from os import mkdir
    mkdir(credspath)

def has_credsext(filename):
    return filename if len(filename) > 7 and filename[-7:] == '.xcreds' else None 

def isnt_none(pattern):
    return pattern 

def get_creds_files():
    from os import listdir
    filelist = listdir(credspath)
    credsfiles = [elem for elem in filter(isnt_none,map(has_credsext,filelist))]
    return credsfiles

def get_creds_file(profile):
    credsfiles = get_creds_files()
    def matches(filename):
        return f"{profile}.xcreds" == filename
    match_ = [elem for elem in filter(matches,credsfiles)]
    return f"{credspath}/{match_[0]}" if len(match_) else None

def get_creds_profiles():
    return [profile.replace('.xcreds','') for profile in get_creds_files()]

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
    return dkode(usr),dkode(pwd)

def generate_creds_file(filename=None,gui=False,page=None,usr=None,pwd=None):
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
        return filename
    else:
        print('no creds supplied...')
        return 

def get_creds(profile=None):
    if not profile:
        print('to which is the username do want to get related creds')
        profile = input('answer>')
    if profile in get_creds_profiles():
        return decode_creds_file(get_creds_file(profile)) 
    else :
        print('sorry, but the requested profile {} doesnt exist'.format(profile))
        return None
    

if(__name__ == '__main__'):
    actions = {
        '0': exit,
        '1': generate_creds_file,
        '2': get_creds
    }
    def action_menu():
        def ask_action():
            print("what do you want to do ?")
            print(" 1 - generate creds file")    
            print(" 2 - read creds file")
            print(" 0 - exit")
            choice = input("answer>")
            err = None
            try:
                choice = int(choice)
            except Exception as e:
                print(e)
                err = True
            finally:
                if not err :        
                    choice = str(choice)
                    if choice in actions:
                        return actions[choice]() 
                    else:
                        print('wrong choice')
                        ask_action()
        ask_action()
    action_menu()