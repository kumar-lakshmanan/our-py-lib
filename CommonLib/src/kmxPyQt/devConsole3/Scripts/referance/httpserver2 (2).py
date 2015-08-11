#For DevConsole
import sys, time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from urllib.parse import urlparse

hostName = "localhost"
hostPort = 9000

class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()        
        self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))   
        print("Testing, we got request")     
        self.rq = self.getInputs()               
        print("Foo:"+str(self.rq['foo']))
                
    def getInputs(self):
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        return query_components      
        
class HttpDaemon(QtCore.QThread):
    def run(self):
        self._server = HTTPServer((hostName, hostPort), MyServer)       
        self._server.serve_forever()
    def stop(self):
        self._server.shutdown()
        self._server.socket.close()
        self.wait()
            
if __name__ == '__main__':
        self.x= HttpDaemon()
        self.x.start()
        print("Started HTTP Server")
        print("Try the url...")
        print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))            
        #self.x.stop()
        