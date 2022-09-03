from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown


class Home:
    view = Column()
    mailbox_container = Row()
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
        mailboxes = self.get_mailboxes()
        self.boxlist.width = int(int(self.pagewidth*20)/100)
        for mailbox in mailboxes:
            box = self.mailboxes[mailbox]
            self.boxlist.controls.append(Text(value=f"{box.get_info('name')} ({box.get_info('mail_count')})"))
        self.mailbox_container.controls.append(self.boxlist)
        if self.actual_view = 'box':
            viewlist = Column()
            viewlist.width = int(int(self.pagewidth*80)/100)
            if  self.actual_mailbox:
                for mail in self.actual_mailbox.mails:
                    viewlist.controls.append(self.generate_mail_hook(mail))

        self.view.controls.append(self.mailbox_container)
        return self.view


    def generate_mail_hook(self,mail):
        


