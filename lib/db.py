import sqlite3
from sqlite3 import Error
import sys

def db_create():
    try:
        conn = sqlite3.connect(r'/opt/gs-payload/listeners.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE listeners (key_id varchar(25) PRIMARY KEY, created varchar(40), connection_succesful varchar(7), last_connected varchar(40));')
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        sys.exit()

def db_list():
    try:
        conn = sqlite3.connect(r'/opt/gs-payload/listeners.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM listeners;')
        results = cur.fetchall()
        for row in results:
            print('|  ' + row[0] + '  |  ' + row[1] + '  |  ' + row[2] + '  |  ' + row[3] + '  |')
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        sys.exit()

def db_add(key, date, connection_status, last_connected):
    try:
        conn = sqlite3.connect(r'/opt/gs-payload/listeners.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO listeners(key_id, created, connection_succesful, last_connected) VALUES(?,?,?,?);', (key, date, connection_status, last_connected))
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        sys.exit()

def db_update(key, connection_status, last_connected):
    try:
        conn = sqlite3.connect(r'/opt/gs-payload/listeners.db')
        cur = conn.cursor()
        cur.execute('UPDATE listeners SET connection_succesful=?, last_connected=? WHERE key_id=?;', (connection_status, last_connected, key))
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        sys.exit()

def db_delete(key):
    try:
        conn = sqlite3.connect(r'/opt/gs-payload/listeners.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM listeners WHERE key_id=?;', (key,))
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        sys.exit()
