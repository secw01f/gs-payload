import sys
import os
import subprocess
import datetime
import db

def gs_connect(key):
    try:
        subprocess.call(('gs-netcat -s ' + '"' + key +'" -i'), shell=True)
        db.db_update(key, 'TRUE', datetime.datetime.now())
        sys.exit()
    except subprocess.CalledProcessError as e:
        print('[ ! ] Connection Failed')
        db.db_update(key, 'FALSE', 'UNKNOWN')
        sys.exit()

def gs_reverse_connect(key):
    try:
        subprocess.call(('gs-netcat -w -s ' + '"' + key +'" -i'), shell=True)
        db.db_update(key, 'TRUE', datetime.datetime.now())
        sys.exit()
    except subprocess.CalledProcessError as e:
        print('[ ! ] Connection Failed')
        db.db_update(key, 'FALSE', 'UNKNOWN')
        sys.exit()
