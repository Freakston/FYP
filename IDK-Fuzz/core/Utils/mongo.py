import pymongo

CLIENT = "mongodb+srv://user:user@camp.tmbbk.mongodb.net/fyp?retryWrites=true&w=majority"

class Mongo:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(CLIENT)

    def addData(self, datName, collectionName, dictVal):
        try:
            database = self.client[datName]
            col = database[collectionName]
            col.insert_one(dictVal)
        except Exception as e:
            print(f"Failed to insert data into the table {e}")
    
    def getData(self, datName, collectionName):
        try:
            database = self.client[datName]
            col = database[collectionName]
            cursor = col.find({})
        except Exception as e:
            print(f"Failed getting the collection {e}")
        
        return cursor

