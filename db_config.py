import mysql.connector

MYSQL_HOST = 'prd1sp.cbjbefi9uiit.us-east-1.rds.amazonaws.com'
MYSQL_USER = 'fd_admin'
MYSQL_PASSWORD = 'fd@admin01'
MYSQL_DB = 'faceDetectorDB'
MYSQL_PORT = 3306


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
