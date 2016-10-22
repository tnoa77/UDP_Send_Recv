#encoding=utf-8
import MySQLdb


class MySQL(object):
    conn = ''
    cursor = ''
    option = {"host": "localhost", "username": "root", "password": "", "database": "cloudtrain"}

    def __init__(self):
        self.conn = MySQLdb.connect(self.option["host"], self.option["username"], self.option["password"],
                                    self.option["database"], charset='utf8')

    def execute(self, sqlstate):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sqlstate)
        insert_id = self.conn.insert_id()
        self.conn.commit()
        self.cursor.close()
        return insert_id

    def query(self, sqlstate):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sqlstate)
        rel = self.cursor.fetchall()
        self.cursor.close()
        return rel

    def __del__(self):
        self.conn.close()