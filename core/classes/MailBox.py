#!/usr/bin/env python3


class MailBox:
    b_raw = None
    raw   = None 
    name  = None
    selector= None
    parent= None
    mail_count= None
    resp_code= None

    def get_info(self,info):
        return self[info] if hasattr(self,info) else None

    def initdata(self):
        self.selector   = self.raw.split(' "/" ')[1]
        self.name = selef.selector.replace('"','').split('/')[-1] 
        self.resp_code,self.mail_count = server.select(self.selector)

    def __init__(self,raw,server):
        self.b_raw = raw
        self.raw   = self.b_raw.decode()
        self.server = server
        self.initdata()