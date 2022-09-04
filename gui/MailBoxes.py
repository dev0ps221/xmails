import quopri
from html2text import html2text
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, ListView, dropdown, Divider, Container

class MailBoxes:
    view = Row()
    mailbox_container = Column(alignment='start')
    message_stuff = Row(alignment='start')
    boxlist = Row(wrap=True)   
    messagebox = Column()
    mailboxes = []
    gotmailboxes = False
    panelbox = Column()
    actual_mailbox = None
    actual_message = None
    messagebody = Container(bgcolor=colors.BLUE_GREY,padding=10)

    actual_message_frombox_container = Container(bgcolor=colors.LIGHT_BLUE,padding=2.5)
    actual_message_frombox = Text(size=12)
    actual_message_tobox_container = Container(bgcolor=colors.LIGHT_BLUE,padding=2.5)
    actual_message_tobox = Text(size=12)
    actual_message_datebox_container = Container(bgcolor=colors.LIGHT_BLUE,padding=2.5)
    actual_message_datebox = Text(size=12)
    actual_message_bodybox = Column(scroll='always')
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
            datebox = self.actual_message_datebox
            bodybox = self.actual_message_bodybox 
            messagebox.height = self.pageheight
            messagebox.width = int(self.mailbox_container.width*65/100)
            frombox.width = int(self.mailbox_container.width*65/100)
            frombox.height = int(self.mailbox_container.height*5/100)
            datebox.width = int(self.mailbox_container.width*65/100)
            datebox.height = int(self.mailbox_container.height*5/100)
            tobox.width = int(self.mailbox_container.width*65/100)
            tobox.height = int(self.mailbox_container.height*5/100)
            bodybox.height = int(self.mailbox_container.height*55/100)
            bodybox.width = int(self.mailbox_container.width*65/100)
            messagebodytext = ""
            messagebodyhtml = None
            partidx = 0
            print(self.actual_message.get('Content'))
            if msg.get_content_subtype() == "html":
                messagebodytext = html2text(self.actual_message.get_content()) 
            
            if msg.get_content_subtype() == "text":
                messagebodytext = html2text(self.actual_message.get_content()) 
            
            # for part in self.actual_message.walk():
            #     print(part.get_content_type())
            #     # print(part.as_string().split("\n"))
            #     if 
            #         messagebodyhtml= [elem for elem in filter(lambda line:'Content-' not in line,part.as_string().split("\n"))]
            #         messagebodyhtml = "\n".join(messagebodyhtml)
            #     if part.get_content_type() == "text/plain":
            #         messagebodytext = [elem for elem in filter(lambda line:'Content-' not in line,part.as_string().split("\n"))]
            #         messagebodytext = "\n".join(messagebodytext)
            #     partidx+=1
            # if messagebodyhtml:
            #     messagebodytext = messagebodyhtml
            partidx = None
            datebox.value="Date       : {}".format(self.actual_message.get("Date"))
            frombox.value="From       : {}".format(self.actual_message.get("From"))
            tobox.value="To       : {}".format(self.actual_message.get("To"))
            messagebodytext=quopri.decodestring(messagebodytext).decode()
            messagebody.width=int(self.pagewidth*65/100)
            messagebody.content = Text(value=messagebodytext,selectable=True,size=12,color=colors.BLACK)
            self.messagebox.update() 
            self.actual_message_bodybox.update()



    def set_actual_mailbox_idx(self,idx):
        self.mailbox_idx = idx
        self.set_actual_mailbox()

    def build_view(self):    
        self.panelbox_container = Container(bgcolor=colors.PURPLE)
        self.panelbox_container.width = int(self.pagewidth*15/100)
        self.panelbox_container.height = int(self.pageheight)
        self.panelbox.width = int(self.pagewidth*15/100)
        self.boxlist.height=int(self.pageheight*10/100)
        self.mailbox_container.width  = int(self.pagewidth*85/100)
        self.mailbox_container.height = int(self.pageheight*100/100)
        self.message_stuff.height = int(self.mailbox_container.height*90/100)
        self.panelbox_container.content = self.panelbox
        self.view.controls.append(self.panelbox_container)
        self.view.width = self.pagewidth
        mailboxes = self.get_mailboxes()
        self.boxlist.controls = []
        ix = 0
        for mailbox in mailboxes:
            box = self.mailboxes[mailbox]
            button = ElevatedButton(text=f'{box.get_info("name")}{box.get_info("mail_count")}')
            if self.actual_mailbox :
                if self.actual_mailbox.get_info('name') == box.get_info('name'):
                    button.color=colors.LIGHT_BLUE
            def switch_box(e):
                self.set_actual_mailbox_idx(ix)
                self.view.update()
            button.on_click = switch_box
            self.boxlist.controls.append(button)
            ix+=1
        self.boxlist.width = int(self.mailbox_container.width)
        self.mailbox_container.controls.append(self.boxlist)
        self.mailbox_container.controls.append(Divider())
        viewlist = Column(scroll='adaptive')
        viewlist.width = int(self.mailbox_container.width*30/100)
        viewlist.height = int(self.mailbox_container.height*90/100)
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
            self.actual_message_tobox_container.content = self.actual_message_tobox
            self.actual_message_datebox_container.content = self.actual_message_datebox
            self.actual_message_frombox_container.content = self.actual_message_frombox
            messagebox.controls = [self.actual_message_frombox_container,self.actual_message_tobox_container,self.actual_message_datebox_container,self.actual_message_bodybox]
        self.message_stuff.controls.append(viewlist)
        
        self.message_stuff.controls.append(messagebox)
        self.mailbox_container.controls.append(self.message_stuff)    
        self.view.controls.append(self.mailbox_container)
        return self.view


    def generate_mail_hook(self,mail,idx):
        mailcontainer = Column()
        mailhookcontainer = Container()
        mailhookcontainer.width=int(self.mailbox_container.width*30/100)
        mailcontainer.width = int(self.mailbox_container.width*30/100)

        mailtitlecontainer = Container(bgcolor=colors.LIGHT_BLUE)
        mailtitle = Text(value=mail.get("From"),size=12)
        mailtitle.width = int(self.mailbox_container.width*30/100)
        maildate = Text(value=mail.get('Date'),size=10)
        maildate.width = int(self.mailbox_container.width*30/100)
        mailhooktext = ""
        partidx = 0
        for part in mail.walk():

            if part.get_content_type() == "text/plain":
                body_lines = [elem for elem in filter(lambda line:'Content-' not in line,part.as_string().split("\n"))]
                mailhooktext += "\n".join(body_lines[4:5])
            partidx+=1
        partidx = None
        try :
            mailhooktext=quopri.decodestring(mailhooktext).decode()
        except Exception as e:
            pass
        mailhook = Text(value=mailhooktext,size=10)
        mailhook.padding = 5
        mailtitlecontainer.content=mailtitle
        mailcontainer.controls.append(mailtitlecontainer)
        mailhookcontainer.content=mailhook
        mailcontainer.controls.append(mailhookcontainer)
        mailcontainer.controls.append(maildate)
        
        def click(e):
            self.set_actual_message(idx)
            self.update_message_box()
        viewbutton = ElevatedButton(on_click=click,text='CONSULTER')
        mailcontainer.controls.append(viewbutton)
        mailcontainer.controls.append(Divider())
        return mailcontainer



