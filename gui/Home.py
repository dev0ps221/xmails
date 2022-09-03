from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown


class Home:
    view = Column()
    mailbox_container = Row()
    boxlist = Column()   
    mailboxes = []
    def __init__(self,page,profile,refresh_page,refresh_view,logout):
        self.page       = page
        self.profile   = profile
        self.refresh_page = lambda *a : refresh_page(*a)
        self.refresh_view = lambda *a : refresh_view(*a)
        self.logout = lambda *a : logout(*a)
        self.pagewidth = int(self.page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
        self.pageheight = int(self.page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
        self.set_mailboxes()

    def set_mailboxes(self):
        self.mailboxes = self.profile.set_mailboxes()
        return self.get_mailboxes()
    
    def get_mailboxes(self):
        return self.mailboxes

    def show(self):
        self.build_view()
        return self.view
    

    def build_view(self):    
        mailboxes = self.get_mailboxes()
        self.boxlist.width = int(int(self.pagewidth*30)/100)
        for mailbox in mailboxes:
            box = self.mailboxes[mailbox]
            self.boxlist.controls.append(Text(value=f"{box.get_info('name')} ({box.get_info('mail_count')})"))
        self.mailbox_container.controls.append(self.boxlist)
        self.view.controls.append(self.mailbox_container)
        return self.view
