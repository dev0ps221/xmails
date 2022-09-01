import imaplib
# Connect to inbox
imap_server = imaplib.IMAP4_SSL(host='pop.gmail.com')
usr = 'tektechlofficiel@gmail.com'
mp = 'cgmsnnhqpvraegpg'
loginerror = None
def dologin(u,p):
    try:
        imap_server.login(u, p)
        return (None,imap_server)
    except Exception as e:
        loginerror = str(e).split('[AUTHENTICATIONFAILED]' if 'AUTHENTICATIONFAILED' in str(e) else ']')[1].replace('\'','') 
    finally:
        if loginerror:
            return (loginerror,None)

loginerr,imap_server = dologin(usr,mdp)

if loginerr:
    print('login error')
    print(loginerr)
else:
    imap_server.select()  # Default is `INBOX`
    # Find all emails in inbox and print out the raw email data
    _, message_numbers_raw = imap_server.search(None, 'ALL')
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')
        print(msg[0][1])