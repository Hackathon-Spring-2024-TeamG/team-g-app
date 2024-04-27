import pymysql

class DB:
    @staticmethod
    def getConnection():
        conn = None
        try:
            conn = pymysql.connect(
                host="db",
                db="chatapp",
                user="testuser",
                password="testuser",
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except pymysql.MySQLError as e:
            print("データベース接続エラー:", e)
            if conn:
                conn.close()
            return None
