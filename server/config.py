import load_dotenv, os

def sql_credentials():

    return {
        
        'user': os.getenv('SQL_ROOT'),
        'password': os.getenv('SQL_PW')
    }