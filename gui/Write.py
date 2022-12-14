from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, ListView, border_radius, dropdown, Divider, VerticalDivider, Container, FilePicker, FilePickerResultEvent
from sys import getsizeof
import filetype
import quopri
class Write:
    view = Column()
    sendmail_container = Container()
    sendmail = Column()
    mail_label = Container(bgcolor=colors.LIGHT_BLUE) 
    mail_label_text = Text(value='ÉCRIRE UN MAIL')
    mail_target = TextField(label='Destinataire')
    mail_subject = TextField(label='Sujet')
    mail_message = TextField(label='Message',multiline=True,min_lines=15)

    attachments = []
    objets_container = Container()
    add_objet_container = Container()
    add_objet = Row()
    objets = Column()
    objets_label = Container(bgcolor=colors.LIGHT_BLUE) 
    objets_label_text = Text(value='PIÈCES JOINTES')
    objets_list_container = Container()
    objets_list = Row(wrap=True)


    def filedata(self,fn):
        res = 0
        try:
            f = open(fn,'rb')
            res = f.read()
        except Exception as e:
            print(e)
        return res

    def add_attachment(self,e: FilePickerResultEvent):
        if e.files:
            [self.attachments.append((f,filetype.guess(f.path))) for f in e.files]
        self.show_attachments()
        return self.attachments

    def show_attachments(self):
        self.objets_list.controls = []
        for attachment,filetype in self.attachments:
            objet_container = Container(padding=10,border_radius=border_radius.all(15))
            objet_container.width = int(self.objets_container.width*32/100)
            objet = Column()
            objet_title = Text(value=attachment.name)
            objet_size = Text(value=f"{float(attachment.size/1000000)}Mb")
            objet_type = Text(value=filetype.mime if filetype else "format non reconnu")
            objet.controls = [objet_title,objet_type,objet_size]
            objet_container.content = objet
            self.objets_list.controls.append(objet_container)
        self.objets_list.update()

    def __init__(self,master):
        self.view = Row()
        self.viewbox = Container()
        self.viewcontent = Row()
        self.master = master
        self.page      = self.master.page   
        self.add_attachment_dialog = FilePicker(on_result=self.add_attachment)
        self.add_attachment_input = ElevatedButton(text='Lier des fichiers',on_click=lambda _:self.add_attachment_dialog.pick_files(allow_multiple=True))
        self.page.overlay.append(self.add_attachment_dialog)
        self.profile   = self.master.logged_profile
        self.refresh_page = self.master.refresh_page
        self.refresh_view = self.master.refresh_view
        self.panelbox_container = self.master.panelbox_container
        self.logout = self.master.logout
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.do_send = ElevatedButton(text='Envoyer',on_click=self.send_mail)

    def send_mail(self,e):
        if self.profile:
            sendres = self.profile.send_mail(self.mail_target.value,self.mail_subject.value,self.mail_message.value,self.attachments)

    def build_write_field(self):
        self.sendmail_container.width= int(self.viewcontent.width*45/100)
        self.mail_label.width = self.sendmail_container.width 
        self.mail_label.content = self.mail_label_text
        self.sendmail.controls = [self.mail_label,self.mail_target,self.mail_subject,self.mail_message,Row(controls=[self.do_send,self.add_attachment_input])]
        self.sendmail_container.content = self.sendmail
        self.mail_message.height = int(self.viewcontent.height*40/100)
        self.mail_message.vertical_alignment = "top"
    
    def build_objets_field(self):
        self.objets_list_container.width= int(self.viewcontent.width*55/100)
        self.objets_container.width = self.objets_list_container.width
        self.objets_label.width = self.objets_list_container.width
        self.objets_label.content = self.objets_label_text
        self.objets_list_container.content = self.objets_list
        self.objets.controls = [self.objets_label,self.objets_list_container]
        self.objets_container.content = self.objets
    
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
        self.build_write_field()
        self.build_objets_field()
        self.viewcontent.controls = [self.sendmail_container,self.objets_container]

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

