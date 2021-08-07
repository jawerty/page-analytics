from .config import sql_credentials

class SQL_Credentials:

    def __init__(self):

        self.creds = sql_credentials()
        self.auth = {

            'host': 'localhost',
            'user': self.creds['user'],
            'password': self.creds['password']
        }
    
    def authenticate(self, db= str):

        self.auth.update({'database': db})