#!/usr/bin/env python3

from flet import app, TextField, Text, Column, Row, Page, ElevatedButton, colors, alignment, Dropdown, dropdown
from os import getcwd
from gui.login_view import *


pagewidth  = 0
pageheight = 0
is_logged  = 0
actual_view = '/login'

 
def logged_view(page,refresh_page,refresh_view):
    view = Column()
    return view



views = {
    "/login": login_view,
    "/home": logged_view
}


def  refresh_view(page):
    global pagewidth
    global pageheight
    global actual_view
    login_view.refresh_view = refresh_view
    pagewidth = int(page.__dict__['_Control__attrs']['windowwidth'][0].split('.')[0])
    pageheight = int(page.__dict__['_Control__attrs']['windowheight'][0].split('.')[0])
    page.clean()
    if actual_view == '/login' and is_logged : update_actual_view('/home') 
    page.add(views[actual_view](page,refresh_page,refresh_view))
    refresh_page(page)

def refresh_page(page):
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
        refresh_view(page)

