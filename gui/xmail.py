
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown, Container, Image,border_radius
from managers.credsmanager import CredsManager,CredsInstance

from gui.Login import Login
from gui.Home import Home
from gui.MailBoxes import MailBoxes

credsman = CredsManager()
credsprofiles = credsman.get_creds_profiles()

class XMAIL:
    panelbox_container = Container()
    panelbox = Column()
    credsman = credsman
    credsprofiles = credsprofiles
    CredsInstance = CredsInstance
    is_logged  = 0
    actual_view = '/home'
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
        if self.logged_profile:
            self.logged_profile.connection.server.close()
        self.is_logged = 0
        self.update_actual_view('/login')
        self.refresh_view()


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

    def switch_to(self,e):
        
        view = e.control.text.lower()

        if 'connexion' in view:
            self.logout()
        
        if 'home' in view:
            self.update_actual_view('/home')

        if 'mailbox' in view:
            self.update_actual_view('/mailboxes')

        self.refresh_view()
        

    def build_panelbox(self):
        self.panelbox_container.controls = []
        self.logobox = Container()
        self.logo = Image(
            src=f"/logo.png",fit='contain',width = int(self.view.pagewidth*15/100),height = int(self.view.pageheight*25/100),bgcolor=colors.LIGHT_BLUE,border_radius=border_radius.all(10)
        )
        self.logoboxtext = Text(color=colors.LIGHT_BLUE,value='TEK TECH \'s xmail')
        self.logobox.content = Column(controls=[self.logo,self.logoboxtext])
        self.panelbox_container.width = int(self.view.view.width*15/100)
        self.panelbox_container.height = int(self.view.view.height)
        gotohome = ElevatedButton(bgcolor=colors.LIGHT_BLUE,color=colors.WHITE,width=self.panelbox_container.width,text='Home',on_click=self.switch_to)
        gotomailboxes = ElevatedButton(bgcolor=colors.LIGHT_BLUE,color=colors.WHITE,width=self.panelbox_container.width,text='Mailbox',on_click=self.switch_to)
        logout = ElevatedButton(bgcolor=colors.LIGHT_BLUE,color=colors.WHITE,width=self.panelbox_container.width,text='Déconnexion',on_click=self.switch_to)
        paneloptions = Column()
        paneloptions.controls = [gotohome,gotomailboxes,logout]
        self.panelbox.controls = [self.logobox,paneloptions]
        self.panelbox_container.content = self.panelbox
    
    def update_panelbox(self):
        self.panelbox_container.update()

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
    


    
