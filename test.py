    # imap_server.select()  # Default is `INBOX`
    # # Find all emails in inbox and print out the raw email data
    # _, message_numbers_raw = imap_server.search(None, 'ALL')
    # for message_number in message_numbers_raw[0].split():
    #     _, msg = imap_server.fetch(message_number, '(RFC822)')
    #     print(msg[0][1])