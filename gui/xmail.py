
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown
from managers.credsmanager import CredsManager,CredsInstance

from gui.Login import Login
from gui.Home import Home
from gui.MailBoxes import MailBoxes

credsman = CredsManager()
credsprofiles = credsman.get_creds_profiles()

class XMAIL:
    credsman = credsman
    credsprofiles = credsprofiles
    CredsInstance = CredsInstance
    is_logged  = 0
    actual_view = '/login'
    views = None
    login_view = None
    logged_profile = None
    view = None
    def login_success(self,profile):
        self.is_logged = 1
        self.logged_profile = profile
        self.update_actual_view('/mailboxes')
        self.refresh_view()

    def logout(self):
        print('disconnecting ',self.logged_profile)


    def isin_login_view(self):
        return self.actual_view == '/login'

    def  refresh_view(self):
        self.page.clean()
        self.view.show()
        self.refresh_page()

    def refresh_page(self):
        self.page.update()

    def view_exists(self,view):
        return view in self.views

    def update_actual_view(self,view):
        if self.view_exists(view) : 
            self.actual_view = view
            self.view = self.views[self.actual_view]


    def app_loop(self,page: Page):
        self.page = page
        self.page.vertical_alignment = "center"
        self.LoginView = Login(self)
        self.HomeView = Home(self)
        self.MailBoxesView = MailBoxes(self)
        self.views = {
            '/login':self.LoginView,
            '/home':self.HomeView,
            '/mailboxes':self.MailBoxesView
        }
        if self.view_exists(self.actual_view) :
            self.view = self.views[self.actual_view]
        self.refresh_view()
    


    
