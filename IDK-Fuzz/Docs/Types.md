## Data types

### Crash

blob will be base64 encoded
```
struct crash{
    int signal
    char* blob
}
```

### Application data

```
struct appData{
    char* appName
    char* appPath
    char* extension
}
```

## Message Types

Job entry
```
Fuzzjob = {
    "FuzzNo": 1,
    "appName": "name",
    "count": 3,
    "Image": "idk-fuzz:latest"
}
```

Sent by mutator to the queue for consumption
```
blob = {
    appName = "sample"
    input = "data"
}

```

