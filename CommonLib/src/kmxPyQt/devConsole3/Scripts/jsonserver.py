#For DevConsole
import sys, time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from urllib.parse import urlparse
import json
import importlib
import sys
import traceback
sys.path.append('J:\our-py-lib\CommonLib\src\kmxPyQt\devConsole3\Scripts')

hostName = "localhost"
hostPort = 9000


def errorReport():
    # Show/Return Error Report
    traceback_lines = traceback.format_exc().split('\n')
    data = '\n'.join(traceback_lines)
    print(data)
    return data

def crashHandle():
        # Prepare Report
        data = errorReport()
        f = open('ServerCrashReport.txt', 'w')
        f.write(str(data))
        f.close()
        sys.exit(0)
        
class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        try:
                import simpleAppsc
                importlib.reload(simpleApps)
                self.myApp = simpleApps.myApplicationModule()
                self.inputs = self.getInputs()
                self.response = self.myApp.doProcessing(self.inputs)                
                self.wfile.write(bytes(str(self.response),'utf-8'))
        except:
                errorReport()
                crashHandle()
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
        #ans = input()         
        #x.stop()
        