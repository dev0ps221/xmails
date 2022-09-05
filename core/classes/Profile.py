#!/usr/bin/env/python3
from core.classes.MailBox import MailBox
from managers.connectionmanager import ConnectionManager 
class Profile:
    rmailboxes = None
    mailboxes = {}
    
    def send_mail(self,target,subject,data):
        maildata = {
            'to':target,
            'subject':subject,
            'message':data
        }
        results = self.connection.send_mail(maildata)
        print(results)
        print(mail_data)
    def login(self,login_success=lambda x:print('login success'),login_failed=lambda x:print('login failed '+x)):
        self.loginerr = None
        if not self.connection.is_connected():
            self.connection.connect()
            if not self.connection.is_connected():
                self.loginerr = self.connection.get_connect_error() 
                login_failed(self.connection.connecterror)
                return
        ret = self.connection.login()
        if self.connection.is_logged():
            login_success(self)
        else:
            self.loginerr = self.connection.get_login_error() 
            login_failed(self.connection.get_login_error())
        return ret

    def init_server_connection(self,connect_success,connect_failed):
        self.connection.connect()
        if self.connection.is_connected():
            connect_success()
        else:
            connect_failed(self.connection.get_connect_error())

    def append_mailbox(self,name,box):
        self.mailboxes[name] = box

    def get_mailbox(self,name):
        return self.get_mailboxes()[name] if name in self.get_mailboxes() else None

    def get_mailboxes(self):
        return self.mailboxes if len(self.mailboxes) else self.set_mailboxes() 

    def set_mailboxes(self):
        if not self.connection.is_connected():
            self.connection.connect()
            if not self.connection.is_connected():
                print(self.connection.connecterror)
                return
        if not self.connection.is_logged():
            self.connection.login()
            if not self.connection.is_logged():
                print(self.connection.loginerror)
                return
        self.rmailboxes = self.connection.server.list()
        for elem in self.rmailboxes[1]:
            box = MailBox(elem,self.server())
            if "Gmail" not in box.get_info('name'):
                self.append_mailbox(box.get_info('name'),box)
        return self.get_mailboxes()
            
    def server(self):
        return self.connection.server

    def __init__(self,creds,host=None,send_host=None):
        self.creds      = creds
        self.connection = ConnectionManager(self.creds,host,send_host)   
