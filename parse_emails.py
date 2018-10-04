import imaplib
import email

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
    id_list = data[0].split()

    typ, data = mail.fetch(id_list[-1], '(RFC822)')

    for response in data:
        if isinstance(response, tuple):
            msg = email.message_from_string(response[1].decode('utf8'))
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    final_msg = part.get_payload()

    return final_msg


def parse_email(msg):
    # This function reads the final message and interprets line one as artist, line two as song

    msg = msg.splitlines()
    print("Artist: "+msg[0])
    print("Title: "+msg[1])

last_email = readmail()
parse_email(last_email)
