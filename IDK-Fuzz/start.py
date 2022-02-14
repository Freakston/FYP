from core.Utils.mongo import Mongo
from core.Fuzzing.Fuzzing import Fuzzer
from core.Mutation.Mutation import Mutation

from threading import Thread

class startUI:
    def __init__(self) -> None:
        self.mon = Mongo()
        self.appsDict = []
    
    # Pull data from mongodb about binary types
    def listBin(self):
        print("The available binaries are: ")
        cursor = self.mon.getData("Apps", "apps")
        for document in cursor:
            print(document)
            self.appsDict.append(document)
    
    # Add data to mongodb about binary types
    def addBin(self):
        print("Enter path of the binary:")
        path = input()
        print("Enter the name of the binary:")
        name = input()
        print("Enter the extension of the binary")
        ext = input()

        appDict = {
            "appName" : name,
            "appPath" : path,
            "extension" : ext 
        }
        self.mon.addData("Apps", "apps", appDict)

    # Function that fetches the data of a specific app
    def startFuzz(self):
        self.listBin()
        print("Enter the application number:")
        appNum = int(input())
        appDict = self.appsDict[appNum]
        
        return appDict

    def trash(self):
        print("Select a valid option")

    # A UI wrapper function
    def showUI(self):
        print("IDK Fuzzer Version 0.1")
        print("----------------------")
        while(True):
            print("Select an option:-")
            print("1. Add binary information to fuzz")
            print("2. Fuzz binary")
            print("3. Show crashes")
            print("69. Exit")
            ch = int(input())
            if ch == 1:
                self.addBin()
            elif ch == 2:
                return self.startFuzz()
            elif ch == 3:
                self.listCrash()
            elif ch == 69:
                exit()
            else:
                self.trash()

def startThreads(app):
    fuzzInstances = 10
    mutateInstances = 2
    
    fuzzer = Fuzzer()
    mutation = Mutation()
    for i in range(mutateInstances):
        mutateThread = Thread(target=mutation.run(app))
        mutateThread.start()
    
    for i in range(fuzzInstances):
        fuzzThead = Thread(target=fuzzer.run(app))
        fuzzThead.start()


def displayStats():
    print("Here we will display the stats")

def main():
    FuzzUI = startUI()
    app = FuzzUI.showUI()
    print(f"Starting to fuzz application {app['appName']}")
    startThreads(app)
    displayStats()
    


if __name__ == "__main__":
    main()
