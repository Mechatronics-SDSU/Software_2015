import sqlite3
import time

id_column = 'id'
name_column = 'name'
ri_column = "RedID"
mc_column = "Major"
def rollList():
    robo_names = []
    mech_names = []
    db = sqlite3.connect('sign_in_sheet')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS robo_sheet(RedID INTEGER PRIMARY KEY, name TEXT,
                           Major TEXT)
    ''')
    db.commit
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mech_101_sheet(RedID INTEGER PRIMARY KEY, name TEXT,
                           Major TEXT)
    ''')    
    cursor.execute('SELECT name FROM robo_sheet')
    for row in cursor:
        robo_names += row
    cursor.execute('SELECT name FROM mech_101_sheet')
    for row in cursor:
        mech_names += row
    db.close
    return robo_names, mech_names

def insertNewMember(table_name, name, redID, major):
    data = sqlite3.connect('sign_in_sheet')
    cur = data.cursor()
    if table_name == 'Robosub':
        cur.execute("INSERT OR IGNORE INTO robo_sheet (RedID, name, Major) VALUES (?, ?, ?)", (redID, name, major))
    if table_name == 'Mechatronics 101':
        cur.execute("INSERT OR IGNORE INTO mech_101_sheet (RedID, name, Major) VALUES (?, ?, ?)", (redID, name, major))
    #cursor.execute("UPDATE %s SET %s=%s WHERE %s=?"%(table_name, name_column, name, id_column, redID))

    data.commit()
    data.close()
    
def rollCallFinished(names, tab):
    date = time.strftime("%b%d%Y")
    if tab == "Robosub":
        table = "robo_sheet"
    else:
        table = "mech_101_sheet"
    data = sqlite3.connect('sign_in_sheet')
    cur = data.cursor()
    try:
        cur.execute("ALTER TABLE "+table+" ADD COLUMN '"+date+"' TEXT")
    except:
        print "Sign in sheet has already been turned in today"
    data.commit()
    for name in names:
        cur.execute("UPDATE "+table+" set '"+date+"' = 'Present' where name=(?)", (name,))
        data.commit
    data.close()
    
if __name__ == '__main__':
    names = []
    db = sqlite3.connect('sign_in_sheet')
    cur = db.cursor()
    cur.execute('SELECT name FROM robo_sheet')
    for row in cur :
        print row
        names += row
    print row
'''all_rows = cursor.fetchall()
for row in all_rows:
    # row[0] returns the first column in the query (name), row[1] returns email column.
    print('{0}'.format(row[0]))'''