import pymysql

class DB:
    @staticmethod
    def getConnection():
        conn = None
        try:
            conn = pymysql.connect(
                host="",
                database="",
                port=3306,
                user="",
                password="",
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except pymysql.MySQLError as e:
            print("データベース接続エラー:", e)
            if conn:
                conn.close()
            return None
