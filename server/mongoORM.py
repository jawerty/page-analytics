import pymongo
import app_config

class MongoCli:
    """Object to handle Mongo Connection"""
    def __init__(self, server: str):

        self.server = server
    
    def connect(self, db: str, collection: str):
        """Connect to Database and Access Declared Collection"""
        self.client = pymongo.MongoClient(self.server)
        print(f"Client Connected to server: {self.server}")
        self.database = self.client[f"{db}"]
        self.collection = self.database[f"{collection}"]
        print(f"Client Connected to database: {db} | Collection: {collection}")

    def insertMany(self, data: list):
        """Function to insert many documents"""
        self.collection.insert_many(data)
        print(f'{len(data)} Documents Added')

    def insert(self, data: dict):
        """Function to insert one document"""
        self.collection.insert(data)
        print('Document Added')

    def findAll(self) -> list:
        """Function to retrieve all documents from a collection"""
        found_data = []
        for data in self.collection.find():
            found_data.append(data)
        # the return is a list of dictionaries
        print(f'Found {len(found_data)} Documents')
        return found_data

    def findOne(self) -> dict:
        """Function to retrieve one document"""
        # this function is check
        return self.collection.find_one()

    def findBy(self, query: dict) -> list:
        """Function to retrieve all records containing an attribute"""
        found_data = []
        for data in self.collection.find(query):
            found_data.append(data)
        # the return is a list of dictionaries
        print(f'Found {len(found_data)} Documents')
        return found_data

class MongoORM(MongoCli):
    """Object to connect to local mongodb"""
    server = app_config.mongoDB

    def __init__(self, database: str, collection: str):
        super().__init__(server=MongoORM.server)
        # instantiates connection to database and collection on server
        # self.database = database
        # self.collection = collection
        self.connect(db=database, collection=collection)