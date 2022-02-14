import pyradamsa
from base64 import b64encode
from core.Utils.utils import rabConnect, rabPublishMessage

class Mutation():
    def __init__(self, data):
        self.data = data
        self.rad = pyradamsa.Radamsa()
        self.channel = rabConnect()
        self.channel.queue_declare(queue="task-queue", durable=True)

    def set_data(self, data):
        self.data = data

    def getinp(self):
        return self.rad.fuzz(self.data)

    def getsinp(self, seed):
        return self.rad.fuzz(self.data, seed)

    def run(self, app):
        for _ in range(100):
            self.send_blob(self.getinp)

    def send_blob(self, data):
        message = {
            "blob": b64encode(data)
        }
        rabPublishMessage(message)

