#For DevConsole
import sys, time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from urllib.parse import urlparse
import json
import importlib

hostName = "localhost"
hostPort = 9000

class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        try:
                import simpleApps
                importlib.reload(simpleApps)
                self.myApp = simpleApps.myApplicationModule()
                self.inputs = self.getInputs()
                self.response = self.myApp.doProcessing(self.inputs)                
                self.wfile.write(bytes(str(self.response),'utf-8'))
        except:
                self.wfile.write(bytes('Some error' ,'utf-8'))
        
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
        