#!/c/Python27/python

import email
import imaplib
import json

from getpass import getpass

SERVER = 'imap.gmail.com'

def fetch(user, passwd, cmd):
    """Login and fetch all the emails matching given search query"""
    
    # Login and authenticate to the Gmail server
    mail = imaplib.IMAP4_SSL(SERVER)
    print 'Connection with %s established.' % SERVER
    
    mail.login(user, passwd)
    print 'User %s authenticated.' % user
    mail.select('[Gmail]/All Mail')
    
    # Search and fetch the required emails
    print 'Searching for email matching : (%s)' % cmd
    res, data = mail.uid('search', None, '(%s)' % cmd)
    ids = data[0].split()
    print '%d results found.' % len(ids)
    
    res, data = mail.uid('fetch', ','.join(ids), '(RFC822)')
    data = filter(lambda x: type(x)!=str, data)
    print 'Fetched %d mails.' % len(ids)
    
    return data


def save(res, name='data'):
    """Save data to a file"""
    
    with open('%s.json' % name, 'w') as f:
        json.dump(res, f)
    print 'Saved emails to file : %s.json' % name

        
def process(data):
    """Extract required data from the mail"""
    
    mail = email.message_from_string(data[1])
    return {
        'date': mail['Date'], 
        'to': mail['To'], 
        'from': mail['From'], 
        'message': mail.get_payload() }


if __name__ == '__main__':
    # Input data from user
    user = raw_input('Username: ')
    passwd = getpass()
    cmd = raw_input('Search query: ') or 'ALL'
    output = raw_input('Destination: ') or 'emails.json'
    
    # Download all emails for given search query
    data = fetch(user, passwd, cmd)
    mails = map(process, data)
    save(mails, output)
