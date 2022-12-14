#!/usr/bin/env python3
import email
import quopri

class MailBox:
    b_raw = None
    raw   = None 
    name  = None
    selector= None
    parent= None
    mail_count= None
    mailcount_resp_code= None
    mail_ids= None
    mailids_resp_code= None
    gotmails = False
    mails = {}

    def update_mails(self,idx=0,count=50):

        if "Gmail" not in self.name: 
            self.mailcount_resp_code,self.mail_count = self.server.select(mailbox=self.selector)
            self.mail_count = self.mail_count[0].decode()
        if self.server.state == 'SELECTED':
            self.mailids_resp_code,self.mail_ids = self.server.search("utf-8","ALL")
        made = 0
        self.mails = {}
        idarr = self.mail_ids[0].split()
        idarr.reverse()
        while idx< count :
            if idx >=0 and idx < len(idarr):
                mail_id = idarr[idx].decode()
                if mail_id:
                    if self.server.state == 'SELECTED':
                        try:
                            resp_code, mail_data = self.server.fetch(mail_id,"(RFC822)")
                            if mail_data is not None and len(mail_data) and mail_data[0] is not None:
                                message = email.message_from_bytes(mail_data[0][1])
                                self.mails[idx] = message
                                idx+=1
                        except Exception as e:
                            mail_data = None
                            pass
            made+=1 
            if made >= len(idarr) : break
        self.gotmails = True
        return self.mails
    
    def get_mails(self,idx=0,count=50):
        return self.mails if self.gotmails else self.update_mails()

    def get_info(self,info):
        return getattr(self,info) if hasattr(self,info) else None

    def initdata(self):
        self.selector   = self.raw.split(' "/" ')[1]
        self.name = self.selector.replace('"','').split('/')[-1] 
        self.name = quopri.decodestring(self.name).decode()
        try:
            if "Gmail" not in self.name: 
                self.mailcount_resp_code,self.mail_count = self.server.select(mailbox=self.selector)
                self.mail_count = self.mail_count[0].decode()
            else :
                self.mailcount_resp_code,self.mail_count = "",0
        except Exception as e:
            print(e)

    def __init__(self,raw,server):
        self.b_raw = raw
        self.raw   = self.b_raw.decode()
        self.server = server
        self.initdata()