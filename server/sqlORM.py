from .sqlCli import SQL_Cli

class sqlORM(SQL_Cli):

    commands = 'queries.sql'
    buildDB = 'createDB.sql'

    def __init__(self, db: str):
        self._db = db
        self.commands = self.read_sql(sqlORM.commands)
        self.buildDB = self.read_sql(sqlORM.buildDB)
        super().__init__(db=db)
        self.__SQL = super()

    @property
    def SQL(self):
        return self.__SQL

    def read_sql(self, f: str) -> list:
        sql = open(f)
        sql = sql.read()
        return sql.split(';')

    def insertSearch(self, data: tuple):
        self.SQL.execute(query=self.commands[0], data=data, commit=True)

    def insertVideo(self, data: tuple):
        self.SQL.execute(query=self.commands[1], data=data, commit=True)

    def insertKeywords(self, data: list):
        for word in data:
            res = self.SQL.execute(query=self.commands[3], data=word, read=True)
            newRow = True
            if len(res) > 0:
                cnt = int(res[0][1])
                newRow = False
            else:
                cnt = 0
            if newRow:
                self.SQL.execute(query=self.commands[2], data=(word, cnt))
            else:
                self.SQL.execute(query=self.commands[4], data=(word, cnt))

        self.SQL.commit()