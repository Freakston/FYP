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