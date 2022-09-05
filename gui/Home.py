import quopri
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, ListView, dropdown, Divider, Container

class Home:
    view = Column()
    def __init__(self,master):
        self.view = Row()
        self.viewbox = Container(bgcolor='red')
        self.master = master
        self.page      = self.master.page
        self.profile   = self.master.logged_profile
        self.refresh_page = self.master.refresh_page
        self.refresh_view = self.master.refresh_view
        self.panelbox_container = self.master.panelbox_container
        self.logout = self.master.logout
        self.pagewidth = int(self.page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
        self.pageheight = int(self.page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])


    def reset_profile(self):
        self.profile = self.master.logged_profile

    def update_view(self):
        self.update_controls()
        self.view.update()
        self.viewbox.update()

    def update_controls(self):
        self.view.height   = self.pageheight
        self.viewbox.height= self.view.height
        self.viewbox.controls = [self.view]

    def show(self):
        # self.reset_profile()
        # if self.profile:
        self.build_view()
        print(self.view.controls)
        self.page.add(self.viewbox)        

    def build_view(self):    
        self.view.width = self.pagewidth
        self.update_controls()
        self.master.build_panelbox()
        self.view.controls = [self.panelbox_container,Divider(),self.view]
        return self.view

