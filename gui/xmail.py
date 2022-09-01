#!/usr/bin/env python3
from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown
from os import getcwd
from credsman import *



pagewidth  = 0
pageheight = 0
is_logged  = 0
actual_view = '/login'

 
def logged_view(page):
    view = Column()
    return view

def login_view(page):
    if not hasattr(login_view,'actual_login_view'):
        login_view.actual_login_view = 'Login'
    view = Column()
    email = Column()
    pwd = Column()
    login = Column()
    select_view = Row()
    login_profiles = get_creds_profiles()

    print(login_profiles)


    def switch_login_view(event):
        login_view.actual_login_view = event.data
        refresh_view(page)

    def do_login(event):
        print("lets proceed to login")
        print(login)


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

    if select_box.value == 'Login':
        actual_login_view = loginview
    else :
        actual_login_view = Column()


    view.controls = [select_view,actual_login_view,login]
    
    return view


views = {
    "/login": login_view,
    "/home": logged_view
}


def  refresh_view(page):
    global pagewidth
    global pageheight
    global actual_view
    pagewidth = int(page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
    pageheight = int(page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
    page.clean()
    if actual_view == '/login' and is_logged : update_actual_view('/home') 
    page.add(views[actual_view](page))
    refresh_page(page)

def refresh_page(page):
    page.update()
    global pagewidth
    global pageheight
    pagewidth = int(page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
    pageheight = int(page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])

def view_exists(view):
    return view in views

def update_actual_view(view):
    if view_exists(view) : actual_view = view




def app_loop(page: Page):
    global actual_view
    page.vertical_alignment = "center"
    if view_exists(actual_view):
        refresh_view(page)

