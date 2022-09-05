import quopri
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, ListView, dropdown, Divider, VerticalDivider, Container

class Write:
    view = Column()
    sendmail_container = Container()
    sendmail = Column()
    mail_label = TextField(label='ÉCRIRE UN MAIL',bgcolor=colors.LIGHT_BLUE)
    mail_target = TextField(label='Destinataire')
    mail_subject = TextField(label='Sujet')
    mail_message = TextField(label='Message',multiline=True,min_lines=15)
    def __init__(self,master):
        self.view = Row()
        self.viewbox = Container()
        self.master = master
        self.page      = self.master.page
        self.profile   = self.master.logged_profile
        self.refresh_page = self.master.refresh_page
        self.refresh_view = self.master.refresh_view
        self.panelbox_container = self.master.panelbox_container
        self.logout = self.master.logout
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.viewcontent = Column()
        self.do_send = ElevatedButton(text='Envoyer',on_click=self.send_mail)

    def send_mail(self,e):
        if self.profile:
            sendres = self.profile.send_mail(self.mail_target.value,self.mail_subject.value,self.mail_message.value)

    def build_write_field(self):
        self.sendmail.controls = [self.mail_label,self.mail_target,self.mail_subject,self.mail_message,self.do_send]
        self.sendmail_container.content = self.sendmail
        self.mail_message.height = int(self.viewcontent.height*40/100)
        self.mail_message.vertical_alignment = "top"
    def reset_profile(self):
        self.profile = self.master.logged_profile

    def update_view(self):
        self.update_controls()
        self.view.update()
        self.viewbox.update()

    def update_controls(self):
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.view.height   = self.pageheight
        self.viewbox.height= self.view.height
        self.viewbox.content = self.view
        self.viewcontent.width= int(self.view.width*80/100)
        self.viewcontent.height= self.view.height
        self.sendmail_container.width= int(self.viewcontent.width*45/100)
        self.build_write_field()
        self.viewcontent.controls = [self.sendmail_container]

    def show(self):
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.reset_profile()
        if self.profile:
            self.build_view()
        self.page.add(self.viewbox)        

    def build_view(self):    
        self.view.width = self.pagewidth
        self.update_controls()
        self.master.build_panelbox()
        self.view.controls = [self.panelbox_container,VerticalDivider(),self.viewcontent]
        return self.view

