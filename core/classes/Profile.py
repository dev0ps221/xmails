#!/usr/bin/env/python3
from managers.connectionmanager import ConnectionManager 
class Profile:
    mailboxes = {}
    def __init__(self,creds):
        self.creds      = creds
        self.connection = ConnectionManager(self.creds)       
