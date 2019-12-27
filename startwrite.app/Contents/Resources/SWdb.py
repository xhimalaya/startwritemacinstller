import sqlite3

# --- md5 encryption ---
# import hashlib
# my_txt = 'Kuntal'
# txt = my_txt.encode() or txt = bytes(my_txt, 'utf-8')
# z = hashlib.md5(txt).hexdigest()

conn = ''
c = ''


def create_db():
    global conn, c
    try:
        conn = sqlite3.connect('sw.db')
        c = conn.cursor()
    except(sqlite3.DatabaseError, sqlite3.ProgrammingError):
        print("DB Connection Error")


def create_license_table():
    global conn, c
    try:
        conn = sqlite3.connect('sw.db')
        c = conn.cursor()
        stmt = "CREATE TABLE LicenseTable (username text, mail text, serial_key text, lin_status integer)"
        c.execute(stmt)
    except:
            print("Table Error")


# Insert Value In Table
def insert_data_into_license_table(username='', mail='', serial_key='00000000', lin_status=0):
    global conn, c
    try:
        conn = sqlite3.connect('sw.db')
        c = conn.cursor()
        c.execute("INSERT INTO LicenseTable VALUES (?,?,?,?);", (username, mail, serial_key, lin_status))
        conn.commit()
    except:
        print("Value Error")


def update_data_into_license_table():
    global conn, c
    try:
        conn = sqlite3.connect('sw.db')
        c = conn.cursor()
        c.execute("UPDATE LicenseTable SET lin_status = 1 where lin_status = 0")
        conn.commit()
    except:
        print("Value Error")


def update_data_into_license_table_with_key(username, mail, serial_key, lin_status=2):
    global conn, c
    try:
        conn = sqlite3.connect('sw.db')
        c = conn.cursor()
        c.execute("UPDATE LicenseTable SET username=?, mail=?, serial_key=?, lin_status=? where lin_status=1;",
                  (username, mail, serial_key, lin_status))
        conn.commit()
    except:
        print("Value Error")


# Fetching Data From DB
def fetching_data_from_license_table():
    global conn, c
    try:
        conn = sqlite3.connect('sw.db')
        c = conn.cursor()
        c.execute("SELECT * FROM LicenseTable")
        row = c.fetchone()
        return row[0], row[1], row[2], row[3]
    except:
        print("Data Fetching Error")
        return -1, -1, -1, -1


''' 
Working With Data
row = cur.fetchone()
date = row[0]
'''