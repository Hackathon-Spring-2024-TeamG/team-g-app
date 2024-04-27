import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
    @staticmethod
    def createUser(uid, name, email, password):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (name, email, crypted_password, self_introduction) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (name, password))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
