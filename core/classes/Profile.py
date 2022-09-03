#!/usr/bin/env/python3
from core.classes.MailBox import MailBox
from managers.connectionmanager import ConnectionManager 
class Profile:
    rmailboxes = None
    mailboxes = {}
    
    def login(self,login_success=lambda x:print('login success'),login_failed=lambda x:print('login failed '+x)):
        if not self.connection.is_connected():
            self.connection.connect()
            if not self.connection.is_connected():
                login_failed(self.connection.connecterror)
                return
        self.connection.login()
        if self.connection.is_logged():
            login_success(self)
        else:
            login_failed(self.connection.get_login_error())

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
        return self.mailboxes

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
            self.append_mailbox(box.getinfo('name'),box)
        return self.get_mailboxes()
            
    def server(self):
        return self.connection.server

    def __init__(self,creds,host=None):
        self.creds      = creds
        self.connection = ConnectionManager(self.creds,host)   
