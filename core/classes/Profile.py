#!/usr/bin/env/python3
class Profile:
    mailboxes = {}
    def __init__(self,creds):
        self.creds      = creds
        self.connection = ConnectionManager(self.creds)       
