import pyradamsa
from base64 import b64encode
from core.Utils.utils import rabConnect, rabPublishMessage

class Mutation():
    def __init__(self, data):
        self.data = data.encode()
        self.rad = pyradamsa.Radamsa()
        self.channel = rabConnect()
        self.channel.queue_declare(queue="task-queue", durable=True)

    def set_data(self, data):
        self.data = data

    def getinp(self):
        tmp = self.rad.fuzz(self.data)
        print(tmp , "-" ,type(tmp))
        return tmp

    def getsinp(self, seed):
        tmp = self.rad.fuzz(self.data, seed)
        print(tmp , "-" ,type(tmp))
        return tmp

    def run(self):
        self.data = "This is the initial string".encode()
        for _ in range(10000):
            self.data = self.getinp()
            self.send_blob(self.getinp())

    def send_blob(self,data):
        message = {
            "exe": "simple-inp",
            "input": b64encode(data).decode()
        }
        rabPublishMessage(self.channel,message)
