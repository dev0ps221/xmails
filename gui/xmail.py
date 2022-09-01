#!/usr/bin/env python3

from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown
from os import getcwd
from gui.login_view import *
from imaplib import IMAP4_SSL

imap_server = IMAP4_SSL(host='pop.gmail.com')
pagewidth  = 0
pageheight = 0
is_logged  = 0
actual_view = '/login'


def login_success(profile):
    print(profile,' is connected')
def logout(profile):
    print('disconnecting ',profile)

def logged_view(page,imap_server,refresh_page,refresh_view):
    view = Column()
    return view

views = {
    "/login": login_view,
    "/home": logged_view
}


def  refresh_view(page,imap_server):
    global pagewidth
    global pageheight
    global actual_view
    pagewidth = int(page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
    pageheight = int(page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
    page.clean()
    if actual_view == '/login' and is_logged : update_actual_view('/home')
    getbackfunc = login_success if actual_view == '/login' else logout    
    page.add(views[actual_view](page,imap_server,refresh_page,refresh_view,getbackfunc))
    refresh_page(page,imap_server)

def refresh_page(page,imap_server,logout):
    login_view.refresh_page = refresh_page
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
        refresh_view(page,imap_server)

