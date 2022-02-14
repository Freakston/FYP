import pymongo

class Mongo:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient("mongodb+srv://Fuzzme:7TF1ULwjWkDidiOE@cluster0.olexg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    def addData(self, tabName, collectionName, dictVal):
        try:
            table = self.client[tabName]
            col = table[collectionName]
            col.insert_one(dictVal)
        except Exception as e:
            print(f"Failed to insert data into the table {e}")
    
    def getData(self, tabName, collectionName):
        try:
            table = self.client[tabName]
            col = table[collectionName]
            cursor = col.find({})
        except Exception as e:
            print(f"Failed getting the collection {e}")
        
        return cursor
