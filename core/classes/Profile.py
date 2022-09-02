#!/usr/bin/env/python3
from core.classes.MailBox import MailBox
from managers.connectionmanager import ConnectionManager 
class Profile:
    rmailboxes = None
    mailboxes = {}


    def login(self,login_success,login_failed):
        self.connection.login()
        if self.is_logged():
            login_success()
        else:
            login_failed(self.connection.get_login_error())

    def init_server_connection(self,connect_success,connect_failed):
        self.connection.connect()
        if self.is_connected():
            connect_success()
        else:
            connect_failed(self.connection.get_connect_error())

    def append_mailbox(self,name,box):
        self.mailboxes[name] = box

    def set_mailboxes(self):
        self.rmailboxes = server.list()
        for elem in self.rmailboxes[1]:
            box = MailBox(elem)
            self.append_mailbox(box.getinfo('name'),box)
        

    def __init__(self,creds):
        self.creds      = creds
        self.connection = ConnectionManager(self.creds)       
