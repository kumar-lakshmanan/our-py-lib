#For DevConsole
import sys
from urllib.request import urlopen
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
HOST, PORT = '127.0.0.1', 12345

class HttpDaemon(QtCore.QThread):
    def run(self):
        self._server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
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
        print("http://%s:%s"%(HOST,PORT))
        #self.x.stop()
        