from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown

def mail_folders(server):
    return [folder for folder in map(lambda folder:folder.decode().split(' "/" '),server.list()[1])]

def home_view(page,imap_server,refresh_page,refresh_view,logout):    
    mailboxes = mail_folders(imap_server)
    print(mailboxes)
    pagewidth = int(page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
    pageheight = int(page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])

    view = Column()
    mailbox_container = Row()
    view.controls.append(mailbox_container)
    return view
