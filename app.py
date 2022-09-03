#!/usr/bin/env python3

from flet import app
from gui.xmail import XMAIL

CLIENT = XMAIL()


app(target=CLIENT.app_loop)
