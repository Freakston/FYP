import json
import requests
from colorama import Fore
from colorama import init
import os

'''
https://mohitgoyal.co/2021/04/23/spinning-up-and-managing-pods-with-multiple-containers-with-podman/

podman system service tcp:localhost:6969 --log-level=debug --time=0

https://docs.podman.io/en/latest/_static/api.html

Podman naming convention as of now

Container_names => appName_FuzzPorjNo._ContainerNo.
Podname => appName_FuzzPorjNo.

so ideally to launch a container we need the following details;

Appname
FuzzPorj No.

This actually helps us in storing less details related to the Fuzzporject;

Now we only need to store the total number of container for each Fuzzproject.
The rest of the information needed to access each pod is already present;

The image is ideally named after the application but hey we can modify it
Fuzzjob{
    "FuzzNo" : 1,
    "appName" : "Name",
    "count" : 3,
    "Image" : "ubuntu"
}

'''

class podmanManager():
    def __init__(self) -> None:
        self.url = f"http://{os.environ['POD']}:16969/v1.40.0/libpod/"
        self.conts = {}
        self.popContainers()
    
    def popContainers(self):
        response = requests.get(self.url+"containers/json?all=true")
        if response.status_code != 200:
            print(f"{Fore.RED}Failed to query containers")
        containers = json.loads(response.text)
        for c in containers:
            self.conts[c['Id']] = c['Names'][0]
    
    def listContainers(self):
        for id in self.conts.keys():
            print(f"Name:{self.conts[id]:<40} Id:{id}")

    def startContainer(self,cont):
        name = self.conts[id]
        response = requests.post(self.url+f"containers/{name}/start")
        if response.status_code != 204:
            print(f"{Fore.RED}Failed staring the container -> {response.text}")

    def stopContainer(self,id):
        name = self.conts[id]
        response = requests.post(self.url+f"containers/{name}/stop?Ignore=True")
        if response.status_code != 204:
            print(f"{Fore.RED}Failed stoping the container -> {response.text}")
            

    def restartContainer(self,id):
        name = self.conts[id]
        response = requests.post(self.url+f"containers/{name}/restart")
        if response.status_code != 204:
            print(f"{Fore.RED}Failed restarting the container -> {response.text}")
    
    def resumeContainer(self,cont):
        name = self.conts[id]
        response = requests.post(self.url+f"containers/{name}/unpause")
        if response.status_code != 204:
            print(f"{Fore.RED}Failed resuming the container -> {response.text}")

    def pauseContainer(self,id):
        name = self.conts[id]
        response = requests.post(self.url+f"containers/{name}/pause")
        if response.status_code != 204:
            print(f"{Fore.RED}Failed pausing the container -> {response.text}")

    def removeContainer(self,id):
        name = self.conts[id]
        response = requests.delete(self.url+f"containers/{name}")
        if response.status_code > 204:
            print(f"{Fore.RED}Failed removing the container -> {response.text}")

    def createContainer(self, Image="docker.io/library/ubuntu:latest"):
        '''
            Here the Image name needs to passed from the backend
        '''
        cont = {
            "Image": Image
        }
        response = requests.post(self.url+"containers/create",json=cont)
        id = json.loads(response.text)["Id"]
        print(f"{Fore.GREEN}Trying to launch container with id -> {id}")
        cont['Id'] = id
        self.startContainer(cont)
    
    def listPods(self):
        response = requests.get(self.url+"pods/json")
        pods = json.loads(response.text)
        for pod in pods:
            print(f"{Fore.BLUE}Podname: {pod['Name']} Number of containers {len(pod['Containers'])}")
    
    def listPodContainers(self,podName):
        # This only lists the running containers
        response = requests.get(self.url+f"pods/{podName}/top")
        if response.status_code == 201:
            podCons = json.loads(response.text)
        else:
            print(f"{Fore.RED}Failed fetching Containers of pod {podName} reason {response.text}")
        
    def createPod(self,Fuzzjob):
        # Our first step is to create the pod
        pod = {
            "Name": Fuzzjob['appName']+'_'+str(Fuzzjob['FuzzNo']),
        }
        response = requests.post(self.url+"pods/create",json=pod)
        if response.status_code != 201:
            print(f"{Fore.RED}Failed to create the pod {response.text}")

        # Now that we have the pod lets launch the containers
        Image = Fuzzjob['Image']
        podName = pod['Name']
        for podcnt in range(Fuzzjob['count']):
            cont = {
                "Image": Image,
                "Name": podName+'_'+str(podcnt),
                "pod": podName
            }
            print(f"{Fore.GREEN} Calling create pod with cont as {cont}")
            response = requests.post(self.url+"containers/create", json=cont)
            if response.status_code != 201:
                print(f"{Fore.RED}Failed to launch container No. {podcnt} reason {response.text}")
                return
        
        print(f"{Fore.BLUE} Finished creating containers")

    def healthCheck(self,name):
        # HEALTHCHECK [OPTIONS] CMD command
        response = requests.post(self.url+f"containers/{name}/healthcheck")
        if response.status_code != 200:
            print(f"{Fore.RED}Failed running healthcheck -> {response.text}")
        pass

init(autoreset=True)
