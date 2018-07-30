import sqlite3

class Db:
    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS pictures     (id INTEGER PRIMARY KEY,name TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS oldFiles     (id INTEGER PRIMARY KEY,name TEXT, cksum TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS newFiles     (id INTEGER PRIMARY KEY,name TEXT, cksum TEXT)")
        self.conn.commit()

    def insertPic(self,name):
        self.cur.execute("INSERT INTO pictures VALUES (NULL,?)",(name,))
        self.conn.commit()

    def insertDir(self,name,cksum):
        self.cur.execute("INSERT INTO oldFiles VALUES (NULL,?,?)",(name,cksum,))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM oldFiles")
        rows=self.cur.fetchall()
        print(rows)
        return rows

    def __del__(self):
        self.conn.close()