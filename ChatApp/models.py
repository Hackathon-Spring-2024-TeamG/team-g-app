import pymysql
from util.DB import DB
from flask import abort

class dbConnect:
    # @staticmethodデコレータを使用して、インスタンス化せずに直接クラスから呼び出せるメソッドを定義
    @staticmethod
    def createUser(name, email, crypted_password):
        conn = None
        cur = None
        new_user_id = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            # トランザクション開始
            cur.execute("START TRANSACTION")
            # ユーザー登録
            sql = "INSERT INTO users (name, email, crypted_password) VALUES (%s, %s, %s);"
            cur.execute(sql, (name, email, crypted_password))
            new_user_id = cur.lastrowid # INSERT操作後に生成された自動増分idを取得
            # パーソナルチャンネル作成
            channel_name = f"{name}'s Channel"
            sql = "INSERT INTO personal_channels (user_id, name) VALUES (%s, %s)"
            cur.execute(sql, (new_user_id, channel_name))
            # トランザクションコミット
            conn.commit()
        except Exception as e:
            # エラー発生時はロールバック
            if conn:
                conn.rollback()
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return new_user_id  # 生成されたユーザーのidを返す

    @staticmethod
    def getUser(email):
        conn = None
        cur = None
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
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    def getChannelAll():
        conn = None
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
            if conn is not None:
                conn.close()

    def getChannelByName(channel_name):
        conn = None
        cur = None
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
            if conn is not None:
                conn.close()

    def addChannel(newChannelName, newChannelDescription, newStartDate):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (name, description, start_date) VALUES (%s, %s, %s);"
            cur.execute(sql, (newChannelName, newChannelDescription, newStartDate))
            conn.commit()
            # 作成したチャンネルのIDを取得
            new_channel_id = cur.lastrowid
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return new_channel_id

    def deleteChannel(channel_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (channel_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    def getChannelById(channel_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cur.execute(sql, (channel_id,))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()


    def updateChannel(newChannelName, newChannelDescription, channel_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE channels SET name=%s, description=%s WHERE id=%s;"
            cur.execute(sql, (newChannelName, newChannelDescription, channel_id,))
            conn.commit()
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    def getMessageAll(channel_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = """
                        SELECT m.id, u.name AS user_name, m.message, m.created_at
                        FROM messages m
                        JOIN users u ON m.user_id = u.id
                        WHERE m.channel_id = %s
                        ORDER BY m.created_at;
                    """
            cur.execute(sql, (channel_id,))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    def addMessage(user_id, channel_id, message):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages (user_id, channel_id, message) VALUES (%s, %s, %s)"
            values = (user_id, channel_id, message)
            cur.execute(sql, values)
            print(f"SQL: {sql}")
            print(f"Values: {values}")
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

# -----------------------------ここから下は個人チャンネルに関連する関数-----------------------------------
    @staticmethod
    def getPersonalChannelAll():
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM personal_channels;"
            cur.execute(sql)
            personal_channels = cur.fetchall()
            return personal_channels
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def getPersonalChannelById(personal_channel_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM personal_channels WHERE id=%s;"
            cur.execute(sql, (personal_channel_id,))
            personal_channel = cur.fetchone()
            return personal_channel
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def getPersonalChannelByUserId(user_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT id, user_id FROM personal_channels WHERE user_id=%s;"
            cur.execute(sql, (user_id,))
            personal_channel = cur.fetchone()
            return personal_channel
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def createPersonalChannel(user_id, newChannelName, newChannelDescription):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO personal_channels (user_id, name, description) VALUES (%s, %s, %s);"
            cur.execute(sql, (user_id, newChannelName, newChannelDescription,))
            conn.commit()
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def updatePersonalChannel(user_id, newChannelName, newChannelDescription, personal_channel_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE personal_channels SET user_id=%s, name=%s, description=%s WHERE id=%s;"
            cur.execute(sql, (user_id, newChannelName, newChannelDescription, personal_channel_id,))
            conn.commit()
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def deletePersonalChannel(personal_channel_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM personal_channels WHERE id=%s;"
            cur.execute(sql, (personal_channel_id,))
            conn.commit()
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def getPersonalMessageAll(personal_channel_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT pm.id, u.id, u.name, pm.message FROM personal_messages AS pm INNER JOIN users AS u ON pm.user_id = u.id WHERE channel_id = %s;"
            cur.execute(sql, (personal_channel_id,))
            p_messages = cur.fetchall()
            return p_messages
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

# -----------------------------ここから下はアカウント機能関連-----------------------------------
    @staticmethod
    def getUserAccount(user_id):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT name, email FROM users WHERE id=%s;"
            cur.execute(sql, (user_id,))
            account = cur.fetchone()
            return account
        except Exception as e:
            print(str(e), 'が発生しています')
            abort(500)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
