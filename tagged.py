#!/c/Python27/python

import json
import os
import time
import urllib

import facebook

TOKEN = ''
ID = 'CreativeIdeass'

def get_photos():
    """Returns a dict of url of photos in your friend's visble albums 
    Change width to get different sizes of pics"""
    
    graph = facebook.GraphAPI(TOKEN)
    query = "SELECT src FROM photo_src WHERE photo_id IN (SELECT object_id FROM photo WHERE aid IN (SELECT aid FROM album WHERE owner IN (SELECT uid2 FROM friend WHERE uid1= me()))) AND width > 1000 LIMIT 1000"

    payload = {'q': query, 'access_token': TOKEN}
    response = requests.get('https://graph.facebook.com/fql', params=payload)
    result = json.loads(response.text)

    return result['data']

def download(res):
    start = time.clock()
    os.mkdir(ID)
    for p in res:
        # try to get a higher resolution of the photo
        p['src'] = p['src'].replace('_s', '_n')
        urllib.urlretrieve(p['src'], p['name'])
    print "Downloaded %s pictures in %.3f sec." % (len(res), time.clock()-start)

if __name__ == '__main__':
    # download all tagged photos 
    lst = get_photos()
    download(lst)
