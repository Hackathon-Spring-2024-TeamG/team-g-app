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

    def getUser(email):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email=%s;"
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            cur.close()
        # curとconnがNoneでないかチェックしてからcloseを呼び出す
        if cur:
            cur.close()
        if conn:
            conn.close()

    def getChannelAll():
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels;"
            cur.execute(sql)
            channels = cur.fetchall()
            return channels
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()