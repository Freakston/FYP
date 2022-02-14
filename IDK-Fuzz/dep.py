from podman import PodmanClient
from core.Utils.utils import rabConnect
import json
from core.Utils.poder import podmanManager
#from core.Utils.mongo import Mongo

class dep():
    def __init__(self) -> None:
        self.rab = rabConnect()
        #self.mong = Mongo()

    def callback(self,ch, method, properties, body):
        '''
            Fuzzjob = {
                "FuzzNo": 1,
                "appName": "name",
                "count": 3,
                "Image": "hello-world:latest"
            }
        '''
        fuzzjob = json.loads(body)
        print(fuzzjob)
        pod = podmanManager()
        pod.createPod(fuzzjob)

    def start(self):
        self.rab.basic_consume(queue='dep-queue', on_message_callback=self.callback, auto_ack=True)
        self.rab.start_consuming()
    
Dep = dep()
Dep.start()
