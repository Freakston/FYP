from core.Utils.utils import rabConnect, rabPublishMessageInfo
#from core.Utils.mongo import Mongo
appCount = 0

class binInfo():
    def __init__(self) -> None:
        #self.mon = Mongo()
        self.rab = rabConnect()
        self.rab.queue_declare(queue="dep-queue", durable=True)
        self.fuzzjob = {"FuzzNo":None,"appName":None,"count":None,"mcount":None,"fcount":None,"Image":None}
    
    def addBin(self):
        global appCount
        print("Enter the name of the binary:")
        name = input()
        self.fuzzjob["appName"] = name
        print("Enter count:")
        count = int(input())
        self.fuzzjob["count"] = count
        print("Enter mutator count:")
        mcount = int(input())
        self.fuzzjob["mcount"] = mcount
        print("Enter fuzzer count:")
        fcount = int(input())
        self.fuzzjob["fcount"] = fcount
        print("Enter the Image name:")
        imgname = input()
        self.fuzzjob["Image"] = imgname + ":latest"
        appCount = appCount + 1
        self.fuzzjob["FuzzNo"] = appCount

        rabPublishMessageInfo(self.fuzzjob)