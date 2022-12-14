from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, FilePicker, Dropdown, dropdown, Container, Image, border_radius
import pyautogui
from os.path import expanduser
from managers.credsmanager import CredsManager,CredsInstance
from gui.Login import Login
from gui.Write import Write
from gui.Home import Home
from gui.MailBoxes import MailBoxes
from os import path,mkdir,chdir,rename as mv
from shutil import rmtree
import atexit
chdir('/'.join(__file__.split('/')[:-2]))
winwidth, winheight = pyautogui.size()
credsman = CredsManager()
credsprofiles = credsman.get_creds_profiles()


class XMAIL:
    panelbox_container = Container()
    panelbox = Column()
    filestuff = FilePicker()
    credsman = credsman
    credsprofiles = credsprofiles
    CredsInstance = CredsInstance
    is_logged  = 0
    actual_view = '/login'
    views = None
    login_view = None
    logged_profile = None
    view = None
    script_path = path.dirname(__file__)
    core_path = path.join(script_path,'../core/')
    cache_path = path.join(core_path,'cache')


    def __init__(self):
        self.start_handler()
        self.filestuff.on_result = self.on_select_download_folder
        atexit.register(self.exit_handler)


    def select_folder(self):
        return self.filestuff.get_directory_path(dialog_title='Choisir une destination',initial_directory=expanduser("~"))
    
    def download_attachment(self,filePath,fileName):
        self.actual_download_target = filePath
        self.actual_download_name = fileName
        self.select_folder()

    def on_select_download_folder(self,ev):
        if ev.path and self.actual_download_target and self.actual_download_name:
            mv(self.actual_download_target,path.join(ev.path,self.actual_download_name))
        actual_download_target = None

    def start_handler(self):
        rmtree(self.cache_path)
        mkdir(self.cache_path)


    def exit_handler(self):
        rmtree(self.cache_path)
        mkdir(self.cache_path)


    def login_success(self,profile):
        self.is_logged = 1
        self.logged_profile = profile
        self.logged_profile.set_mailboxes()
        self.update_actual_view('/mailboxes')
        self.refresh_view()

    def logout(self):
        if self.logged_profile:
            if self.logged_profile.connection.server.state == 'SELECTED':
                self.logged_profile.connection.server.close()
        self.logged_profile = None
        self.is_logged = 0
        self.update_actual_view('/login')
        self.refresh_view()


    def isin_login_view(self):
        return self.actual_view == '/login'

    def  refresh_view(self):
        self.view.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.view.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.page.clean()
        self.view.show()
        self.refresh_page()

    def refresh_page(self):
        self.page.add(self.filestuff)
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

        if '??crire' in view:
            self.update_actual_view('/write')

        self.refresh_view()
        

    def build_panelbox(self):
        self.panelbox_container.controls = []
        self.logobox = Container()
        self.logo = Image(
            src=f"/logo.png",fit='contain',width = int(self.view.pagewidth*15/100),height = int(self.view.pageheight*25/100),border_radius=border_radius.all(10)
        )
        self.logoboxtext = Text(color=colors.LIGHT_BLUE,value='TEK TECH \'s xmail')
        self.logobox.content = Column(controls=[self.logo,Row(controls=[self.logoboxtext],alignment='center')],alignment='center')
        self.panelbox_container.width = int(self.view.view.width*15/100)
        self.panelbox_container.height = int(self.view.view.height)
        gotohome = ElevatedButton(bgcolor=colors.LIGHT_BLUE,color=colors.WHITE,width=self.panelbox_container.width,text='Home',on_click=self.switch_to)
        gowrite = ElevatedButton(bgcolor=colors.LIGHT_BLUE,color=colors.WHITE,width=self.panelbox_container.width,text='??crire',on_click=self.switch_to)
        gotomailboxes = ElevatedButton(bgcolor=colors.LIGHT_BLUE,color=colors.WHITE,width=self.panelbox_container.width,text='Mailbox',on_click=self.switch_to)
        logout = ElevatedButton(bgcolor=colors.RED,color=colors.WHITE,width=self.panelbox_container.width,text='D??connexion',on_click=self.switch_to)
        paneloptions = Column()
        paneloptions.controls = [gotohome,gowrite,gotomailboxes,logout]
        self.panelbox.controls = [self.logobox,paneloptions]
        self.panelbox_container.content = self.panelbox
    
    def update_panelbox(self):
        self.panelbox_container.update()

    def resize_view(self,e):
        self.page.window_width = int(self.page.window_width)
        self.page.window_height = int(self.page.window_height)
        self.refresh_view() 
        self.page.update()

    def app_loop(self,page: Page):
        self.page = page
        self.page.color = colors.BLACK
        self.page.bgcolor = colors.BLUE_200
        self.page.on_resize = self.resize_view
        self.page.window_width = winwidth
        self.page.window_height = winheight
        self.page.vertical_alignment = "center"
        self.LoginView = Login(self)
        self.HomeView = Home(self)
        self.WriteView = Write(self)
        self.MailBoxesView = MailBoxes(self)
        self.views = {
            '/login':self.LoginView,
            '/home':self.HomeView,
            '/write':self.WriteView,
            '/mailboxes':self.MailBoxesView
        }
        if self.view_exists(self.actual_view) :
            self.view = self.views[self.actual_view]
        self.refresh_view()
    


    
