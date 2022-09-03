from flet import TextField, Text, Column, Row, ElevatedButton, colors, alignment, Dropdown, dropdown
from managers.credsmanager import CredsManager,CredsInstance
from core.classes.Profile import Profile

credsman = CredsManager()
credsprofiles = credsman.get_creds_profiles()

class Login:

    email = Column()
    pwd = Column()
    view = Column()
    login = Column()
    profiles = Column()
    select_view = Row()
    loginview = Column()
    loginerr = None
    emaillabel = Text(value='Email')
    emailInput = TextField(label='Email')
    pwdlabel = Text(value='pwd')
    pwdInput = TextField(label='pwd',password=True)
    login_profiles_select = Dropdown(
        label="PROFILES",
        options=[],
        hint_text="Choose the profile you want to log in",
        autofocus=True
    )
        

    def __init__(self,page,profiles,refresh_page,refresh_view,login_success):
        self.page       = page
        self.login_profiles   = profiles
        self.refresh_page = lambda *a : refresh_page(*a)
        self.refresh_view = lambda *a : refresh_view(*a)
        self.login_success = lambda *a : login_success(*a)
        self.pagewidth = int(self.page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
        self.pageheight = int(self.page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
        self.actual_login_view = 'Login'
        self.build_components()

    def build_components(self):
        self.loginview = loginbox(page)
        self.profilesview = profilesbox(page)
        

    def loginbox(self):
        self.email.horizontal_alignment ='center'
        self.emaillabel.width = int(pagewidth/2)
        self.emaillabel.alignment = alignment.center
        self.emailInput.width = int(pagewidth/2)
        self.emailInput.alignment = alignment.center
        self.email.controls=[self.emaillabel,self.emailInput]
        self.email.horizontal_alignment = "center"
        
        
        self.pwdlabel.width = int(pagewidth/2)
        self.pwdInput.width = int(pagewidth/2)
        self.pwd.controls=[self.pwdlabel,self.pwdInput]
        self.pwd.horizontal_alignment = "center"

        self.loginview.width = pagewidth
        self.loginview.horizontal_alignment ='center'
        self.loginview.controls = [email,pwd]
        return self.loginview

    def profilesbox(self):
        profiles = [profile for profile in self.login_profiles]
        
        self.login_profiles_select.options=profiles
        self.login_profiles_select.width = int(self.pagewidth/2)
        
        
        self.profilesview.width = pagewidth
        self.profilesview.horizontal_alignment ='center'
        self.profilesview.controls = [self.login_profiles_select]

        return self.profilesview



    def switch_login_view(self,event):
        self.actual_login_view = event.data
        self.refresh_view(self.page,self.server)


    def do_login(self,event):
        loginerror = None
        usrval  = None
        passval = None
        if login_view.actual_login_view == 'Profiles':
            credsinstance = credsman.get_creds_instance(self.login_profiles_select.value)
            if credsinstance :
                usrval = credsinstance.get_cred('user')
                passval = credsinstance.get_cred('pass')
        else:
            usrval  = emailInput.value
            passval = pwdInput.value
            credsinstance = CredsInstance(credsman.generate_creds_file(usrval,passval),credsman)
        if usrval and passval:
            profile = Profile(credsinstance)
            try:
                profile.login(self.login_success,self.login_error)
            except Exception as e:
                self.loginerror = str(e).split('[AUTHENTICATIONFAILED]' if 'AUTHENTICATIONFAILED' in str(e) else ']')[1].replace('\'','') 
            finally:
                if loginerror:
                    login_view.login_failed = loginerror
                    refresh_view(page,imap_server)
                else:
                    login_success(page,usrval)
    def login_error(self,error):
        self.loginerr = error 


    def build_view(self):
        self.page.clean()
        login_profiles = [elem for elem in map(dropdown.Option,get_creds_profiles())]
        login_profiles_select = None


        
        select_view.width = pagewidth/2
        select_box  = Dropdown(
            label="LOGIN MODE",
            on_change=switch_login_view,
            hint_text="Choose the way you want to log in",
            value=self.actual_login_view,
            options=[
                dropdown.Option("Login"),
                dropdown.Option("Profiles")
            ],
            autofocus=True
        )
        select_box.width = pagewidth/2
        select_box.alignment =alignment.center

        select_view.controls = [select_box]

        view.width = pagewidth
        view.horizontal_alignment ='center'
        
        
        loginInput = ElevatedButton(text='login',on_click=do_login)
        login.controls=[loginInput]
        login.horizontal_alignment = "center"



        if select_box.value == 'Login':
            self.actual_login_view = loginview
        else :
            self.actual_login_view = profilesview

        if self.loginerr: 
            self.actual_login_view.controls.append(Text(value=self.loginerr))

        view.controls = [select_view,self.actual_login_view,login]
        
        return view