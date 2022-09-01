from flet import TextField, Text, Column, Row, ElevatedButton, colors, alignment, Dropdown, dropdown
def login_view(page):
    page.clean()
    if not hasattr(login_view,'actual_login_view'):
        login_view.actual_login_view = 'Login'
    view = Column()
    email = Column()
    pwd = Column()
    login = Column()
    profiles = Column()
    select_view = Row()
    
    login_profiles = [elem for elem in map(dropdown.Option,get_creds_profiles())]
    login_profiles_select = Dropdown(
        label="PROFILES",
        hint_text="Choose the profile you want to log in",
        options=login_profiles,
        autofocus=True
    )
    login_profiles_select.width = int(pagewidth/2)
    
    def switch_login_view(event):
        login_view.actual_login_view = event.data
        refresh_view(page)

    def do_login(event):

        print("lets proceed to login")

        if login_view.actual_login_view == 'Profiles':
            if login_profiles_select.value:
                print(login_profiles_select.value)
                usrval,passval = decode_creds_file(get_creds_file(login_profiles_select.value))
        else:
            usrval  = emailInput.value
            passval = pwdInput.value
        if usrval and passval:
            print('we are ready to login!!!')
            print(usrval,passval)
        


    view.width = pagewidth
    view.horizontal_alignment ='center'
    
    email.horizontal_alignment ='center'
    emaillabel = Text(value='Email')
    emaillabel.width = int(pagewidth/2)
    emaillabel.alignment = alignment.center
    emailInput = TextField(label='Email')
    emailInput.width = int(pagewidth/2)
    emailInput.alignment = alignment.center
    email.controls=[emaillabel,emailInput]
    email.horizontal_alignment = "center"
    
    
    pwdlabel = Text(value='pwd')
    pwdlabel.width = int(pagewidth/2)
    pwdInput = TextField(label='pwd',password=True)
    pwdInput.width = int(pagewidth/2)
    pwd.controls=[pwdlabel,pwdInput]
    pwd.horizontal_alignment = "center"
    
    loginInput = ElevatedButton(text='login',on_click=do_login)
    login.controls=[loginInput]
    login.horizontal_alignment = "center"

    select_box  = Dropdown(
        label="LOGIN MODE",
        on_change=switch_login_view,
        hint_text="Choose the way you want to log in",
        value=login_view.actual_login_view,
        options=[
            dropdown.Option("Login"),
            dropdown.Option("Profiles")
        ],
        autofocus=True
    )
    select_box.width = pagewidth/2
    select_box.alignment =alignment.center

    select_view.controls = [select_box]
    select_view.width = pagewidth/2
    select_box.alignment =alignment.center


    loginview = Column()
    loginview.width = pagewidth
    loginview.horizontal_alignment ='center'
    loginview.controls = [email,pwd]
    
    profilesview = Column()
    profilesview.width = pagewidth
    profilesview.horizontal_alignment ='center'
    profilesview.controls = [login_profiles_select]

    if select_box.value == 'Login':
        actual_login_view = loginview
    else :
        actual_login_view = profilesview


    view.controls = [select_view,actual_login_view,login]
    
    return view