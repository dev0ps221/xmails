import quopri
from html2text import html2text
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, ListView, dropdown, Divider, VerticalDivider, Container, border_radius
from os import mkdir,path
from filetype import guess
class MailBoxes:
    view = Row()
    mailbox_container = Column(alignment='start')
    message_stuff = Row(alignment='start')
    boxlist = Row(wrap=True)   
    messagebox = Column()
    viewlist = Column(scroll='adaptive')
    objets_list = Row(wrap=True)   
    mailboxes = []
    gotmailboxes = False
    panelbox = Column()
    actual_mailbox = None
    actual_message = None
    messagebody = Container(bgcolor=colors.BLUE_100,padding=10)

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
        self.panelbox_container = self.master.panelbox_container
        self.refresh_view = self.master.refresh_view
        self.logout = self.master.logout
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        if self.profile:
            self.set_mailboxes()

    def reset_profile(self):
        self.profile = self.master.logged_profile
        self.get_mailboxes()

    def set_mailboxes(self):
        if self.profile:
            self.mailboxes = self.profile.get_mailboxes()
            self.gotmailboxes = True
            self.set_actual_mailbox()
            return self.mailboxes
        else : return []

    def set_actual_mailbox(self):
        if len(self.mailboxes) == 0:
            self.actual_mailbox = None
            self.mailbox_idx = -1
        else:
            if self.mailbox_idx < 0 or self.mailbox_idx >= len(self.mailboxes): 
                self.mailbox_idx = 0
            self.actual_mailbox = self.mailboxes[list(self.mailboxes.keys())[self.mailbox_idx]]
        print(self.actual_mailbox.get_info('name'))
        

    def get_mailboxes(self):
        return self.set_mailboxes()

    def show(self):
        self.view.controls = []
        self.viewlist.controls = []
        self.messagebox = Column()
        self.page.update()
        self.page.clean()
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
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
            messagebodytext = ""
            messagebodyhtml = None
            if self.actual_message.is_multipart():
                for part in self.actual_message.walk():
                    if part.get_content_subtype() == "html":
                        messagebodyhtml= [elem for elem in str(html2text(part.get_payload(decode=True).decode())).split("\n")]
                        messagebodyhtml = "\n".join(messagebodyhtml) 
                    
                    if part.get_content_subtype() == "text":
                        messagebodytext = [elem for elem in filter(lambda line:'Content-' not in line,part.as_string().split("\n"))]
                        messagebodytext = "\n".join(messagebodytext)
                    fileName = part.get_filename()        
                    if bool(fileName):
                        fileName = fileName.split('/')[-1]
                        profile_path = path.join(self.master.cache_path,self.profile.creds.get_cred('user'))
                        try :
                            mkdir(profile_path)
                        except Exception:
                            pass
                        filePath = path.join(profile_path, fileName)
                        print(profile_path)
                        print(filePath)
                        print(not path.isfile(filePath))
                        filesize = 'UNKNOWN'
                        if not path.isfile(filePath) :
                            fp = open(filePath, 'wb')
                            filesize = len(part.get_payload(decode=True))
                            fp.write(part.get_payload(decode=True))
                            fp.close()            
                        self.objets_list.width = int(self.pagewidth*65/100)
                        filetype = guess(filePath)
                        objet_container = Container(padding=10,border_radius=border_radius.all(15))
                        objet_container.width = int(self.objets_list.width*32/100)
                        objet = Column()
                        objet_title = Text(value=fileName)
                        objet_size = Text(value=f"{float(filesize/1000000)}Mb")
                        objet_type = Text(value=filetype.mime if filetype else "format non reconnu")
                        objet.controls = [objet_title,objet_type,objet_size]
                        objet_container.content = objet
                        self.objets_list.controls.append(objet_container)

            else:
                if self.actual_message.get_content_subtype() == "html":
                    messagebodytext = self.actual_message.get_payload(decode=True)
                    messagebodyhtml = str(html2text(messagebodytext.decode('utf-8')))
                else:
                    messagebodytext = self.actual_message.as_string().split("\n")
                    messagebodytext = "\n".join(messagebodytext)
            if messagebodyhtml:
                messagebodytext = messagebodyhtml
            else:
                messagebodytext=quopri.decodestring(messagebodytext).decode()
            partidx = None
            datebox.value="Date       : {}".format(self.actual_message.get("Date"))
            frombox.value="From       : {}".format(self.actual_message.get("From"))
            tobox.value="To       : {}".format(self.actual_message.get("To"))
            messagebody.width=int(self.pagewidth*65/100)
            messagebody.content = Text(value=messagebodytext,selectable=True,size=12,color=colors.BLACK)
            self.messagebox.update() 
            self.actual_message_bodybox.update()



    def set_actual_mailbox_idx(self,idx=None):
        self.mailbox_idx = idx if idx is not None else self.mailbox_idx
        self.set_actual_mailbox()

    def update_boxlist(self):
        mailboxes = self.get_mailboxes()
        self.boxlist.controls = []
        self.boxlist.height = int(self.mailbox_container.height*10/100)
        ix = 0
        for mailbox in mailboxes:
            box = self.mailboxes[mailbox]
            def boxbutton(idx):
                def switch_box(e):
                    self.set_actual_mailbox_idx(int(idx)-1)
                    self.build_view()
                    self.view.update()
                    self.page.update()
                button = ElevatedButton(text=f'{box.get_info("name")}({box.get_info("mail_count")})',on_click=switch_box)
                return button
            button = boxbutton(ix+1)
            if self.actual_mailbox :
                if self.actual_mailbox.get_info('name') == box.get_info('name'):
                    button.color=colors.LIGHT_BLUE
            self.boxlist.controls.append(button)
            ix+=1

    def update_viewlist(self):
        viewlist = self.viewlist
        viewlist.width = int(self.mailbox_container.width*30/100)
        viewlist.height =  int(self.mailbox_container.height*85/100)
        if  self.actual_mailbox:
            self.actual_mailbox.get_mails()
            if not self.actual_message : self.set_actual_message(0)
            idx = 0
            viewcontrols = []
            for mail in self.actual_mailbox.mails:
                mail = self.actual_mailbox.mails[mail]
                viewcontrols.append(self.generate_mail_hook(mail,idx))
                idx+=1
            viewlist.controls = viewcontrols
        

    def update_actualmsgbox(self):
        messagebox = self.messagebox
        if  self.actual_mailbox:
            self.actual_message_bodybox.controls = []
            self.actual_message_bodybox.controls.append(self.messagebody)
            self.actual_message_tobox_container.content = self.actual_message_tobox
            self.actual_message_datebox_container.content = self.actual_message_datebox
            self.actual_message_frombox_container.content = self.actual_message_frombox
            messagebox.controls = [self.actual_message_frombox_container,self.actual_message_tobox_container,self.actual_message_datebox_container,self.actual_message_bodybox,self.objets_list]

    def build_view(self):
        self.reset_profile()
        if self.profile:
            titlesusr = self.profile.creds.get_cred('user')
            mailboxname = self.actual_mailbox.get_info('name')
            self.page.title = f'{titlesusr} - XMAIL - {mailboxname} - TEK TECH 2022 '
        self.view.controls = []    
        self.mailbox_container.width  = int(self.pagewidth*90/100)
        self.mailbox_container.height = int(self.pageheight*100/100)
        self.message_stuff.height = int(self.mailbox_container.height*85/100)
        self.message_stuff.width = int(self.mailbox_container.width)
        self.boxlist.width = int(self.mailbox_container.width)
        self.view.width = self.pagewidth
        self.view.height = self.pageheight

        messagebox = self.messagebox
        messagebody = self.messagebody
        frombox = self.actual_message_frombox
        tobox = self.actual_message_tobox
        datebox = self.actual_message_datebox
        bodybox = self.actual_message_bodybox 
        messagebox.height =  int(self.mailbox_container.height*85/100)
        messagebox.width = int(self.message_stuff.width*65/100)
        frombox.width = int(self.mailbox_container.width*65/100)
        frombox.height = int(self.mailbox_container.height*5/100)
        datebox.width = int(self.mailbox_container.width*65/100)
        datebox.height = int(self.mailbox_container.height*5/100)
        tobox.width = int(self.mailbox_container.width*65/100)
        tobox.height = int(self.mailbox_container.height*5/100)
        bodybox.height = int(self.mailbox_container.height*55/100)
        bodybox.width = int(self.mailbox_container.width*65/100)
        self.master.build_panelbox()
        self.append_controls()
        return self.view

    def append_controls(self):
        self.update_boxlist()
        self.update_viewlist()
        self.update_actualmsgbox()
        viewlist = self.viewlist
        messagebox = self.messagebox
        self.message_stuff.controls=[viewlist,messagebox]
        self.mailbox_container.controls=[self.boxlist,Divider(),self.message_stuff]    
        self.view.controls = [self.panelbox_container,VerticalDivider(),self.mailbox_container]

    def generate_mail_hook(self,mail,idx):
        mailcontainerbox = Container(bgcolor=colors.BLUE_300,padding=5,border_radius=border_radius.all(10))
        mailcontainer = Column()
        mailhookcontainer = Container()
        mailhookcontainer.width=int(self.message_stuff.width*30/100)
        mailcontainer.width = int(self.message_stuff.width*30/100)

        mailtitlecontainer = Container(bgcolor=colors.LIGHT_BLUE)
        mailtitle = Text(value=mail.get("From"),size=12)
        mailtitle.width = int(self.mailbox_container.width*30/100)
        maildate = Text(value=mail.get('Date'),size=8)
        maildate.width = int(self.mailbox_container.width*30/100)
        
        try:
            mailhooktext  = ''.join([chr(ord(c))  for c in mail.get('Subject').__str__()]).encode().decode('utf-8') 
        except Exception as e:
            mailhooktext =  ''.join([chr(ord(c))  for c in mail.get('Subject').__str__()])
            print(e)
        mailhook = Text(value=mailhooktext,color=colors.BLACK,size=10)
        mailhook.padding = 5
        mailtitlecontainer.content=mailtitle
        mailcontainer.controls.append(mailtitlecontainer)
        mailhookcontainer.content=mailhook
        mailcontainer.controls.append(mailhookcontainer)
        
        def click(e):
            self.set_actual_message(idx)
            self.update_message_box()
        viewbutton = ElevatedButton(on_click=click,text='CONSULTER')
        mailcontainer.controls.append(maildate)
        mailcontainer.controls.append(Divider())
        mailcontainer.controls.append(viewbutton)
        mailcontainerbox.content = mailcontainer
        return mailcontainerbox



