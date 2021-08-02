from mysql.connector import conn
from sqlCreds import SQL_Credentials

class SQL_Cli:

    def __init__(self, db: str):

        self.credentials = SQL_Credentials()
        self.credentials.authenticate(db=db)
        self.__db = self.sqlConnect(db=db)

    @property
    def db(self):
        return self.__db

    def sqlConnect(self, db: str) -> object:

        return conn.connect(

                host = credentials.auth['host'],
                user = credentials.auth['user'],
                password = credentials.auth['password'],
                database = credentials.auth['database']
            )

    def execute(self, query: str,
                      bulkInfo: list = None, 
                      commit: bool = False, 
                      read: bool = False) -> list:
        
        data = []
        cursor=self.db.cursor()
        if bulkInfo:
            cursor.excutemany(query, bulkInfo)
        else:
            cursor.execute(query)
        if commit:
            self.db.commit()
        if read:
            data = cursor.fetchall()
        cursor.close()
        return data

    def commit(self):
        self.db.commit() 