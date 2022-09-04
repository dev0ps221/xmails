import quopri
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, ListView, dropdown, Divider, Container


class Home:
    view = Column()
    mailbox_container = Row(alignment='start')
    boxlist = Column()   
    messagebox = Column()
    mailboxes = []
    gotmailboxes = False
    actual_mailbox = None
    actual_message = None
    messagebody = Container(bgcolor=colors.LIGHT_BLUE)
    actual_message_frombox = Text()
    actual_message_tobox = Text()
    actual_message_bodybox = Column(scroll='adaptive')
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
        
    def set_actual_message(self,idx):
        if self.actual_mailbox and idx < len(self.actual_mailbox.mails):
            match_ = None
            i = 0
            for mail in self.actual_mailbox.mails:
                mail = self.actual_mailbox.mails[mail]
                if i == idx:
                    match_ = mail
                i+=1
            if match_:
                self.actual_message = match_

    def update_message_box(self):
        messagebox = self.messagebox
        messagebody = self.messagebody
        
        if self.actual_message:
            frombox = self.actual_message_frombox
            tobox = self.actual_message_tobox
            bodybox = self.actual_message_bodybox 
            messagebox.height = self.pageheight
            messagebox.width = int(self.pagewidth*55/100)
            frombox.height = int(self.pageheight*5/100)
            tobox.height = int(self.pageheight*5/100)
            bodybox.height = int(self.pageheight*90/100)
            bodybox.width = int(self.pagewidth*55/100)
            messagebodytext = ""
            for part in self.actual_message.walk():
                if part.get_content_type() == "text/plain":
                    messagebodytext = part.as_string().split("\n")
                    messagebodytext = "\n".join(messagebodytext)
            ndate = self.actual_message.get('Date')
            messagebodytext=f"Date:{ndate} \n\n {messagebodytext}"
            frombox.value="From       : {}".format(self.actual_message.get("From"))
            tobox.value="To       : {}".format(self.actual_message.get("To"))
            messagebodytext=quopri.decodestring(messagebodytext).decode()
            messagebody.width=int(self.pagewidth*55/100)
            messagebody.content = Text(value=messagebodytext)
            print(messagebody)
            print(messagebodytext)
            self.messagebox.update() 
            self.actual_message_bodybox.update()

    def build_view(self):    
        self.view.width = self.pagewidth
        mailboxes = self.get_mailboxes()
        self.boxlist.controls = []
        for mailbox in mailboxes:
            box = self.mailboxes[mailbox]
            self.boxlist.controls.append(Text(value=f"{box.get_info('name')} ({box.get_info('mail_count')})"))
        self.boxlist.width = int(self.pagewidth*15/100)
        self.mailbox_container.controls.append(self.boxlist)
        viewlist = Column(scroll='adaptive')
        viewlist.width = int(self.pagewidth*30/100)
        viewlist.height = self.pageheight
        messagebox = self.messagebox
        if  self.actual_mailbox:
            titlesusr = self.profile.creds.get_cred('user')
            mailboxname = self.actual_mailbox.get_info('name')
            self.page.title = f'{titlesusr} - XMAIL - {mailboxname} - TEK TECH 2022 '
            self.actual_mailbox.get_mails()
            if not self.actual_message : self.set_actual_message(0)
            idx = 0
            for mail in self.actual_mailbox.mails:
                mail = self.actual_mailbox.mails[mail]
                viewlist.controls.append(self.generate_mail_hook(mail,idx))
                idx+=1

            self.actual_message_bodybox.controls.append(self.messagebody)
            messagebox.controls = [self.actual_message_frombox,self.actual_message_tobox,self.actual_message_bodybox]

        self.mailbox_container.controls.append(viewlist)
        self.mailbox_container.controls.append(messagebox)    
        self.view.controls.append(self.mailbox_container)
        return self.view


    def generate_mail_hook(self,mail,idx):
        mailcontainer = Column()
        mailcontainer.width = int(self.pagewidth*30/100)
        mailtitle = Text(color=colors.BLUE_600,value=mail.get("From"))
        mailtitle.width = int(self.pagewidth*30/100)
        maildate = Text(value=mail.get('Date'))
        maildate.width = int(self.pagewidth*30/100)
        mailhooktext = ""
        for part in mail.walk():
            if part.get_content_type() == "text/plain":
                body_lines = part.as_string().split("\n")
                mailhooktext += "\n".join(body_lines[4:6])
        mailhooktext=quopri.decodestring(mailhooktext).decode()
        mailhook = Text(value=mailhooktext)
        mailcontainer.controls.append(mailtitle)
        mailcontainer.controls.append(mailhook)
        mailcontainer.controls.append(maildate)
        
        def click(e):
            self.set_actual_message(idx)
            self.update_message_box()
        viewbutton = ElevatedButton(on_click=click,text='CONSULTER')
        mailcontainer.controls.append(viewbutton)
        mailcontainer.controls.append(Divider())
        return mailcontainer



