
import imaplib2 as imaplib
imaplib.Untagged_status = imaplib.re.compile(br'\*[ ]{1,2}(?P<data>\d+) (?P<type>[A-Z-]+)( (?P<data2>.*))?')
IMAP4_SSL = imaplib.IMAP4_SSL
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ConnectionManager:
    host='pop.gmail.com'
    send_host='smtp.gmail.com'
    _is_connected = False
    _is_logged    = False 
    server       = None 
    loginerror   = None
    connecterror = None

    def send_mail(self,maildata):

        port = 587  

        context = ssl.create_default_context()
        res = None,None
        try:
            server = smtplib.SMTP(self.send_host,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(self.creds.get_cred('user'), self.creds.get_cred('pass'))

            message = MIMEMultipart("alternative")
            message["Subject"] = maildata['subject']
            message["From"] = self.creds.get_cred('user')
            message["To"] = maildata['to']

            message.attach(MIMEText(maildata['message'],'text'))
            res = None,server.sendmail(
                self.creds.get_cred('user'), maildata['to'], message.as_string()
            )
        except Exception as e:
            print(e)
            res = e,None
        finally:
            server.quit() 
        return res

    def get_server(self):
        return self.server

    def get_login_error(self):
        return self.loginerror

    def get_connect_error(self):
        return self.connecterror

    def is_connected(self):
        return self._is_connected

    def is_logged(self):
        return self._is_logged  

    def login(self):
        self.loginerr = None
        try:
            self.server.login(self.creds.get_cred('user'), self.creds.get_cred('pass'))
            self._is_logged  =   True
            self.loginerror =   None
        except Exception as e:
            self._is_logged  =   False
            self.loginerror = str(e).split('[AUTHENTICATIONFAILED]' if 'AUTHENTICATIONFAILED' in str(e) else ']')[1].replace('\'','') 
        return self.is_logged()

    def connect(self):
        try:
            self.server = IMAP4_SSL(self.host)
            self._is_connected  =   True
            self.loginerror =   None
        except Exception as e:
            self._is_connected  =   False
            self.connecterror = str(e).split('[AUTHENTICATIONFAILED]' if 'AUTHENTICATIONFAILED' in str(e) else ']')[1].replace('\'','') 
        
    def __init__(self,creds,host,send_host):
        self.host   = host if host else self.host
        self.send_host   = send_host if send_host else self.send_host
        self.creds  = creds