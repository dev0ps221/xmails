#!/usr/bin/env python3

from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown
from os import getcwd
from gui.login_view import *
from gui.home_view import *
from imaplib import IMAP4_SSL

imap_server = IMAP4_SSL(host='pop.gmail.com')
is_logged  = 0
actual_view = '/login'


def login_success(page,profile):
    global imap_server
    global is_logged
    is_logged = 1
    update_actual_view('/home')
    refresh_view(page,imap_server)

def logout(page,profile):
    print('disconnecting ',profile)

views = {
    "/login": login_view,
    "/home": home_view
}

def  refresh_view(page,imap_server):
    global actual_view
    page.clean()
    if actual_view == '/login' and is_logged : update_actual_view('/home')
    getbackfunc = login_success if actual_view == '/login' else logout    
    page.add(views[actual_view](page,imap_server,refresh_page,refresh_view,getbackfunc))
    refresh_page(page,imap_server)

def refresh_page(page,imap_server):
    login_view.refresh_page = refresh_page
    page.update()

def view_exists(view):
    return view in views

def update_actual_view(view):
    global actual_view
    if view_exists(view) : actual_view = view



def app_loop(page: Page):
    global actual_view
    page.vertical_alignment = "center"
    if view_exists(actual_view):
        refresh_view(page,imap_server)

