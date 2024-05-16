# import pymysql

# class DB:
#     @staticmethod
#     def getConnection():
#         conn = None
#         try:
#             conn = pymysql.connect(
#                 host="",
#                 database="",
#                 port=3306,
#                 user="",
#                 password="",
#                 charset="utf8",
#                 cursorclass=pymysql.cursors.DictCursor
#             )
#             return conn
#         except pymysql.MySQLError as e:
#             print("データベース接続エラー:", e)
#             if conn:
#                 conn.close()
#             return None







import pymysql

class DB:
    def getConnection():
        try:
            conn = pymysql.connect(
#            host="db",
            host="hackathonspring2024teamg-web.cdkwg66k0zmv.ap-northeast-1.rds.amazonaws.com",
            database="chatapp",
            port=3306,
            user="testuser",
            password="testuser",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except (ConnectionError):
            print("コネクションエラーです")
            conn.close()

