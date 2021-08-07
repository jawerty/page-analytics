import mysql.connector as connection
from .sqlCreds import SQL_Credentials

class SQL_Cli:

    def __init__(self, db: str):
        self.credentials = SQL_Credentials()
        self.credentials.authenticate(db=db)
        self.__db = self.sqlConnect(db=db)

    @property
    def db(self):
        return self.__db

    def sqlConnect(self, db: str) -> object:

        return connection.connect(

                host = self.credentials.auth['host'],
                user = self.credentials.auth['user'],
                password = self.credentials.auth['password'],
                database = self.credentials.auth['database']
            )

    def execute(self, query: str,
                      data: tuple,
                      bulkInfo: list = None, 
                      commit: bool = False, 
                      read: bool = False) -> list:
        
        result = []
        cursor=self.db.cursor()
        if bulkInfo:
            cursor.excutemany(query, bulkInfo)
        else:
            print("begin")
            print(query, data)
            print("end")
            cursor.execute(query, data)
        if commit:
            self.db.commit()
        if read:
            result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self):
        self.db.commit() 