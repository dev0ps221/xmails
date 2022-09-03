from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown


class HomeView:


        view = Column()
        mailbox_container = Row()
        boxlist = Column()   
    def __init__(self,page,profiles,refresh_page,refresh_view,login_success):
        self.page       = page
        self.login_profiles   = profiles
        self.refresh_page = lambda *a : refresh_page(*a)
        self.refresh_view = lambda *a : refresh_view(*a)
        self.login_success = lambda *a : login_success(*a)
        self.pagewidth = int(self.page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
        self.pageheight = int(self.page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
   
    def show(self):
        return self.view
    
    def mail_folders(server):
        boxes = [folder for folder in map(lambda folder:folder.decode().split(' "/" '),server.list()[1])]
        mailboxes = []
        for box in boxes :
            if box[1] == '"[Gmail]"':
                box.append(['',''])
                box.append('')
                continue
            resp_code, mail_count = server.select(box[1])
            box.append([resp_code,mail_count])
            box.append(box[1].replace('"','').split('/')[-1])
            mailboxes.append(box)
        return mailboxes

    def home_view(page,profile,refresh_page,refresh_view,logout):    
        mailboxes = profile.set_mailboxes()
        pagewidth = int(page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
        pageheight = int(page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
    
        boxlist.width = int(int(pagewidth*30)/100)
        for mailbox in mailboxes:
            box = mailboxes[mailbox]
            boxlist.controls.append(Text(value=f"{box.get_info('name')} ({box.get_info('mail_count')})"))

        mailbox_container.controls.append(boxlist)
        view.controls.append(mailbox_container)
        return view
