#from core.Utils.mongo import Mongo
from back import binInfo

class startUI:
    def __init__(self) -> None:
        self.bin = binInfo()

    def trash(self):
        print("Select a valid option")

    # A UI wrapper function
    def showUI(self):
        print("IDK Fuzzer Version 0.2")
        print("----------------------")
        while(True):
            print("Select an option:-")
            print("1. Add binary information")
            #print("2. Show crashes")
            print("69. Exit")
            ch = int(input())
            if ch == 1:
                self.bin.addBin()
            #elif ch == 2:
            #    self.listCrash()
            elif ch == 69:
                exit()
            else:
                self.trash()

#def displayStats():
#    print("Here we will display the stats")

def main():
    FuzzUI = startUI()
    app = FuzzUI.showUI()
    #displayStats()

if __name__ == "__main__":
    main()
