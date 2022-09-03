from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, ListView, dropdown


class Home:
    view = Column()
    mailbox_container = Row(alignment='start')
    boxlist = Column()   
    mailboxes = []
    gotmailboxes = False
    actual_mailbox = None
    actual_view = 'box'
    mailbox_idx = -1
    def __init__(self,master):
        self.master = master
        self.page      = self.master.page
        self.profile   = self.master.logged_profile
        self.refresh_page = self.master.refresh_page
        self.refresh_view = self.master.refresh_view
        self.logout = self.master.logout
        self.pagewidth = int(self.page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
        self.pageheight = int(self.page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
        if self.profile:
            self.set_mailboxes()

    def reset_profile(self):
        self.profile = self.master.logged_profile

    def set_mailboxes(self):
        self.mailboxes = self.profile.set_mailboxes()
        self.gotmailboxes = True
        self.set_actual_mailbox()
        return self.get_mailboxes()

    def set_actual_mailbox(self):
        if len(self.mailboxes) == 0:
            self.actual_mailbox = None
            self.mailbox_idx = -1
        else:
            if self.mailbox_idx < 0 or self.mailbox_idx >= len(self.mailboxes): 
                self.mailbox_idx = 0
            self.actual_mailbox = self.mailboxes[list(self.mailboxes.keys())[self.mailbox_idx]]

    def get_mailboxes(self):
        if self.gotmailboxes:
            return self.mailboxes
        else:
            return self.set_mailboxes()

    def show(self):
        self.reset_profile()
        if self.profile:
            self.build_view()
        self.page.add(self.view)
        

    def build_view(self):    
        self.view.width = self.pagewidth
        mailboxes = self.get_mailboxes()
        for mailbox in mailboxes:
            box = self.mailboxes[mailbox]
            self.boxlist.controls.append(Text(value=f"{box.get_info('name')} ({box.get_info('mail_count')})"))
        self.boxlist.width = int(self.pagewidth*30/100)
        self.mailbox_container.controls.append(self.boxlist)
        if self.actual_view == 'box':
            viewlist = Column(scroll='adaptive')
            viewlist.width = int(self.pagewidth*60/100)
            viewlist.height = self.pageheight
            if  self.actual_mailbox:
                self.actual_mailbox.get_mails()
                idx = 0
                for mail in self.actual_mailbox.mails:
                    mail = self.actual_mailbox.mails[mail]
                    viewlist.controls.append(self.generate_mail_hook(mail,idx))
                    idx+=1
            self.mailbox_container.controls.append(viewlist)
        self.view.controls.append(self.mailbox_container)
        return self.view


    def generate_mail_hook(self,mail,idx):
        mailcontainer = Column()
        mailtitle = Text(bgcolor=colors.BLUE_600,value=mail.get("From"))
        mailhooktext = ""
        for part in mail.walk():
            if part.get_content_type() == "text/plain":
                body_lines = part.as_string().split("\n")
                mailhooktext += "\n".join(body_lines[4:8])
        mailhook = Text(value=mailhooktext)
        mailcontainer.controls.append(mailtitle)
        mailcontainer.controls.append(mailhook)
        return mailcontainer



