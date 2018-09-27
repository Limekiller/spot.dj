import imaplib

from_email = 'gcprogrammingclub@gmail.com'
from_pwd = 'YAYPYTHON'
smtp_server = 'imap.gmail.com'
smtp_port = 993

def readmail():
    # This function reads the email account for spot.dj requests
    mail = imaplib.IMAP4_SSL(smtp_server)
    mail.login(from_email,from_pwd)
    mail.select('inbox')

    type, data = mail.search(None, '(SUBJECT "spotipy")')
    print(type, data)
    mail_ids = data[0]
    id_list = mail_ids.split()

readmail()
