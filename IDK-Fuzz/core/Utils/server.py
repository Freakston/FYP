from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv
from mongo import Mongo

'''
Cluster camp{
    "ip" : <IP>,
    "camp : <Campaign Name>
}

Cluster env{
    "camp" : <Campaign Name>,
    "var1" : <Varibale Value>
    "var2" : <Varibale Value> 
}

'''

BIND_HOST = 'localhost'
PORT = 8008

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        dat = Mongo()
        #ip = self.client_address[0]
        ip = "22"    
        var = dat.getData('fyp','camp')
        for i in var:
            if i['ip'] == ip:
                campaign = i['camp']

        env_var = dat.getData('fyp','env')
        for i in env_var:
            ret_var = []
            if i['camp'] == campaign:                
                ret_var.append(i['var']) 

        self.write_response(bytes(str(ret_var),'utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)

        self.write_response(body)

    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        print(self.headers)
        print(content.decode('utf-8'))


if len(argv) > 1:
    arg = argv[1].split(':')
    BIND_HOST = arg[0]
    PORT = int(arg[1])

print(f'Listening on http://{BIND_HOST}:{PORT}\n')

httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()
