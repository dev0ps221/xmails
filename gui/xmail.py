#!/usr/bin/env python3

from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown
from os import getcwd
# from gui.login_view import *
from gui.home_view import *
from gui.Login import Login
from imaplib import IMAP4_SSL
from coreman import *

is_logged  = 0
actual_view = '/login'
views = None
login_view = None
logged_profile = None
def login_success(page,profile):
    global imap_server
    global is_logged
    global logged_profile
    is_logged = 1
    logged_profile = profile
    update_actual_view('/home')
    refresh_view(page,logged_profile)

def logout(page,profile):
    print('disconnecting ',profile)




def  refresh_view(page,imap_server):
    global actual_view
    global logged_profile
    page.clean()
    if actual_view == '/login' and is_logged : update_actual_view('/home')
    getbackfunc = login_success if actual_view == '/login' else logout
    args = (page,credsprofiles,refresh_page,refresh_view,login_success) if actual_view == '/login' else (page,logged_profile,refresh_page,refresh_view,getbackfunc)
    view = views[actual_view](*args)
    page.add(view)

    refresh_page(page)

def refresh_page(page):
    page.update()

def view_exists(view):
    return view in views

def update_actual_view(view):
    global actual_view
    if view_exists(view) : actual_view = view



def app_loop(page: Page):
    global actual_view
    global views
    login_view = Login(page,credsprofiles,refresh_page,refresh_view,login_success)
    page.vertical_alignment = "center"
    views = {
        "/login": login_view.show,
        "/home": home_view
    }
    if view_exists(actual_view):
        refresh_view(page,None)



