
from imaplib import IMAP4_SSL

class ConnectionManager:
    host='pop.gmail.com'
    is_connected = False
    is_logged    = False 
    server       = None 

    def is_connected(self):
        return self.is_connected

    def is_logged(self):
        return self.is_logged  
    def connect(self):
        imap_server = IMAP4_SSL(self.host)

    def __init__(self):