from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown

def mail_folders(server):
    boxes = [folder for folder in map(lambda folder:folder.decode().split(' "/" '),server.list()[1])]
    for box in boxes :
        if box[1] == "[Gmail]": continue
        resp_code, mail_count = server.select(box[1])
        box.append([resp_code.decode(),mail_count.decode()])
    return boxes
def home_view(page,imap_server,refresh_page,refresh_view,logout):    
    mailboxes = mail_folders(imap_server)
    pagewidth = int(page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
    pageheight = int(page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])

    view = Column()
    mailbox_container = Row()
    boxlist = Column()
    for box in mailboxes:
        boxlist.controls.append(Text(value=f"{box[1]} ({box[2][1]})"))
        
    mailbox_container.controls.append(boxlist)
    view.controls.append(mailbox_container)
    return view
