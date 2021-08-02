from sqlCli import SQL_Cli

class sqlORM(SQL_Cli):

    commands = 'queries.sql'
    buildDB = 'createDB.sql'

    def __init__(self, db: str):
        
        self.db = db
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
        self.SQL.execute(query=self.commands[0].format(str(data)), commit=True)

    def insertVideo(data: tuple):
        self.SQL.execute(query=self.commands[1].format(str(data)), commit=True)

    def insertKeywords(self, data: list):

        for word in data:
            
            res = self.SQL.execute(query=self.commands[3].format(word), read=True)
            newRow = True
            if len(res) > 0:
                cnt = int(res[0][1])
                newRow = False
            else:
                cnt = 0
            if newRow:
                self.SQL.execute(query=self.commands[2].format(tuple(word, cnt)))
            else:
                self.SQL.execute(query=self.commands[4].format(tuple(cnt, word)))

        self.SQL.commit()