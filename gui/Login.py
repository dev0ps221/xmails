
from flet import TextField, Text, Column, Row, ElevatedButton, colors, alignment, Dropdown, dropdown
from core.classes.Profile import Profile

class Login:

    email = Column()
    pwd = Column()
    login = Column()
    profiles = Column()
    select_view = Row()
    loginview = Column()
    profilesview = Column()
    loginerr = None
    emaillabel = Text(value='Email',color=colors.BLACK)
    emailInput = TextField(label='Email')
    pwdlabel = Text(value='pwd',color=colors.BLACK)
    pwdInput = TextField(label='pwd',password=True)
    login_profiles_select = Dropdown(
        label="PROFILES",
        options=[],
        hint_text="Choose the profile you want to log in",
        autofocus=True
    )
        

    def __init__(self,master):
        self.master = master
        self.page       = self.master.page
        self.credsman = self.master.credsman
        self.CredsInstance = self.master.CredsInstance
        self.login_profiles   = self.master.credsprofiles
        self.refresh_page = self.master.refresh_page
        self.refresh_view = self.master.refresh_view
        self.login_success = self.master.login_success
        self.pagewidth = int(self.page.__dict__['_Control__attrs']['windowwidth'][0])
        self.pageheight = int(self.page.__dict__['_Control__attrs']['windowheight'][0])
        self.actual_login_view = 'Login'
        self.build_components()
        self.build_view()

    def build_components(self):
        self.loginview = self.loginbox()
        self.profilesview = self.profilesbox()
        

    def loginbox(self):
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.email.horizontal_alignment ='center'
        self.emaillabel.width = int(self.pagewidth/2)
        self.emaillabel.alignment = alignment.center
        self.emailInput.width = int(self.pagewidth/2)
        self.emailInput.alignment = alignment.center
        self.email.controls=[self.emaillabel,self.emailInput]
        self.email.horizontal_alignment = "center"
        
        
        self.pwdlabel.width = int(self.pagewidth/2)
        self.pwdInput.width = int(self.pagewidth/2)
        self.pwd.controls=[self.pwdlabel,self.pwdInput]
        self.pwd.horizontal_alignment = "center"

        self.loginview.width = self.pagewidth
        self.loginview.horizontal_alignment ='center'
        self.loginview.controls = [self.email,self.pwd]
        return self.loginview

    def profilesbox(self):
        profiles = [dropdown.Option(profile) for profile in self.login_profiles]
        
        self.login_profiles_select.options=profiles
        self.login_profiles_select.width = int(self.pagewidth/2)
        
        
        self.profilesview.width = self.pagewidth
        self.profilesview.horizontal_alignment ='center'
        self.profilesview.controls = [self.login_profiles_select]

        return self.profilesview



    def switch_login_view(self,*kwargs):
        self.view.clean()
        self.actual_login_view = self.select_box.value
        self.build_components()
        self.build_view()
        self.refresh_view()
        
        



    def do_login(self,event):
        loginerror = None
        usrval  = None
        passval = None
        if self.actual_login_view == 'Profiles':
            credsinstance = self.credsman.get_creds_instance(self.login_profiles_select.value)
            if credsinstance :
                usrval = credsinstance.get_cred('user')
                passval = credsinstance.get_cred('pass')
        else:
            usrval  = self.emailInput.value
            passval = self.pwdInput.value
            credsinstance = self.CredsInstance(self.credsman.generate_creds_file(None,None,None,usrval,passval),self.credsman)
        if usrval and passval:
            profile = Profile(credsinstance)
            try:
                profile.login()
                self.loginerr = profile.connection.get_login_error()
            except Exception as e:
                earr = str(e).split('[AUTHENTICATIONFAILED]' if 'AUTHENTICATIONFAILED' in str(e) else ']')
                self.loginerr = earr[1 if len(earr) > 1 else 0].replace('\'','') 
            finally:
                if profile.connection.is_logged():
                    self.page.clean()
                    self.master.logged_profile = profile
                    self.login_success(profile)
                else:
                    self.refresh_view()
                    self.loginerr = profile.connection.get_login_error()

    def login_error(self,error):
        self.loginerr = error 


    def show(self,*kwargs):
        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.page.clean()
        self.page.title = 'XMAIL - TEK TECH 2022 - LOGIN'
        self.build_view()
        self.page.add(self.view)
        
    def build_view(self):

        self.pagewidth = int(float(self.page.__dict__['_Control__attrs']['windowwidth'][0]))
        self.pageheight = int(float(self.page.__dict__['_Control__attrs']['windowheight'][0]))
        self.view = Column()
        self.select_view.width = self.pagewidth/2
        self.select_box  = Dropdown(
            label="LOGIN MODE",
            on_change=self.switch_login_view,
            hint_text="Choose the way you want to log in",
            value=self.actual_login_view,
            options=[
                dropdown.Option("Login"),
                dropdown.Option("Profiles")
            ],
            autofocus=True
        )
        self.select_box.width = self.pagewidth/2
        self.select_box.alignment =alignment.center

        self.select_view.controls = [self.select_box]

        self.view.width = self.pagewidth
        self.view.horizontal_alignment ='center'
        self.loginInput = ElevatedButton(text='login',on_click=self.do_login)
        self.login.controls=[self.loginInput]
        self.login.horizontal_alignment = "center"

        if self.select_box.value == 'Login':
            self.actual_view = self.loginview
        else :
            self.actual_view = self.profilesview

        if self.loginerr: 
            self.actual_view.controls.append(Text(value=f"{self.loginerr}"))

        self.actual_view.width = self.pagewidth/2
        self.view.controls = [self.select_view,self.actual_view,self.login]

        return self.view