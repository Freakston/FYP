import requests

print("Sending request for the information")

r = requests.get("http://localhost:8008/")
print("Required Variables are: " + r.text + "\n")
# Use eval(r.text) to access as a list