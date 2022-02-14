# Some notes on how to setup environment and other things needed

## Rabbitmq

```
podman run -p 5672:5672 -p 15672:15672 -d --hostname sexyrab --name sexyrab-rabbit rabbitmq:3-management
```

## Setting up Registry

Run this command to create the directory
```
sudo mkdir -p /var/lib/registry
```

Now run this command to start the registry

```
sudo podman run --privileged -d --name registry -p 5000:5000 -v /var/lib/registry:/var/lib/registry --restart=always registry:2
```

Now that this is done we need to edit the registries file on the podman vm.

```
sudo nano /etc/containers/registries.conf
```

In this addd the follwing
```
registries = ['localhost:5000']
```

## Pushing image to registry

Pull down the NGINX image with the command:

```
podman pull nginx
```

Before we push the NGINX image to the registry, we’re going to make some changes to it (so it’s our own image). First, deploy a container based on the newly-downloaded image with the command:

```
sudo podman run --name nginx-template-base -p 8080:80 -e TERM=xterm -d nginx
```

Once the container deploys, you’ll be presented with its ID. Access the running container with the command:

```
sudo podman exec -it CONTAINER_ID bash
```

Where CONTAINER_ID is the ID of the container given to you when it was initially deployed.

Now we’ll install nano, build-essential, and php with the commands:

```
apt-get update

apt-get install nano

​apt-get install build-essential

​apt-get install php5
```

When that completes, exit the container with the command:

```
exit
```

Commit the changes to the container (thereby creating a new image) with the command:

```
sudo podman commit CONTAINER_ID nginx-template
```

Where CONTAINER_ID is the ID of the container given to you when it was initially deployed.

To see your new image, issue the command:

```
sudo podman images
```

You should see a listing for:

`localhost/nginx-template`

We can now tag the image and push it to the locally hosted registry.

```
sudo podman tag localhost/nginx-template localhost:5000/nginx-template
```

Now, if you issue the command:

```
sudo podman images
```