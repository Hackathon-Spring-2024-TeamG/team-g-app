import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
    @staticmethod
    def createUser(name, email, crypted_password):
        conn = None
        cur = None
        id = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            # トランザクション開始
            cur.execute("START TRANSACTION")
            # ユーザー登録
            sql = "INSERT INTO users (name, email, crypted_password) VALUES (%s, %s, %s);"
            cur.execute(sql, (name, email, crypted_password))
            id = cur.lastrowid # INSERT操作後に生成された自動増分idを取得
            # パーソナルチャンネル作成
            channel_name = f"{name}'s Channel"
            sql = "INSERT INTO personal_channels (user_id, name) VALUES (%s, %s)"
            cur.execute(sql, (id, channel_name))
            # トランザクションコミット
            conn.commit()
        except Exception as e:
            # エラー発生時はロールバック
            if conn:
                conn.rollback()
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        return id  # 生成されたユーザーのidを返す

    @staticmethod
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

    def getChannelByName(channel_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()

    def addChannel(newChannelName, newChannelDescription, newStartDate):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (name, description, start_date) VALUES (%s, %s, %s);"
            cur.execute(sql, (newChannelName, newChannelDescription, newStartDate))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()

    def getPersonalChannelALL():
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM personal_channels;"
            cur.execute(sql)
            p_channels = cur.fetchall()
            return p_channels
        except Excepton as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()