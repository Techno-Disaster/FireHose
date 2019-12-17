import sqlite3
import __main__
try:
    db = sqlite3.connect('Firehose')
    cursor = db.cursor()
    cursor.execute('''create table stocks1 (ticker varchar(50),date datetime,open float,high float, low float,
close float,volume float,dividends float,closeunadj float,lastupdated datetime)''')

except Exception as E:
    print('Error :', E)
else:
    print('table created')


try:
    cursor.executemany('insert into stocks values(?,?,?,?,?,?,?,?,?,?)', data)
except Exception as E:
    print('Error : ', E)
else:
    db.commit()
    print('data inserted')


try:
    db = sqlite3.connect('Firehose')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM stocks1 ''')
except Exception as E:
    print('Error: ', E)
else:
    for row in cursor.fetchall():
      print(row)
db.close()
