# -*- mode: python ; coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright © 2014 Tomás Godoi, <tomastxg@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import re
import cgi
import json
from aqt.qt import *
from PyQt4 import QtCore

from .util import addCardFromType

thread = None

class IntincHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if None != re.search('/anki/plugins/intinc/v1/prepareCard/*', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.getheader('content-length'))
                #data = cgi.parse_qs(self.rfile.read(length), keep_blank_values = 1)
                #recordID = self.path.split('/')[-1]
                json_str = self.rfile.read(length)
                data = json.loads(json_str, 'utf-8');
                print data
                thread.emit(SIGNAL("doPrepareCard(PyQt_PyObject, PyQt_PyObject)"), data['typeName'], data['values'])
                #addCardFromType(data['typeName'], data['values'])
            else:
                data = {}
        
                self.send_response(200)
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
#        self.end_headers()

    def log_message(self, format, *args):
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
 
    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)

class IntincServer(QtCore.QThread):
    def __init__(self, mw, parent = None):
        QtCore.QThread.__init__(self)
        self.server_address = ('', 8000)
        self.server = ThreadedHTTPServer(self.server_address, IntincHandler)
        self.mw = mw

    def startServer(self):
        global thread
        #self.server_thread = threading.Thread(target = self.server.serve_forever)
        #self.server_thread.daemon = True
        #self.server_thread.start()
        self.start()
        self.mw.connect(self, SIGNAL("doPrepareCard(PyQt_PyObject, PyQt_PyObject)"), addCardFromType)
        thread = self

    #def waitForThread(self):
    #    self.server_thread.join()

    def stopServer(self):
        self.server.shutdown()
        self.wait()

    def run(self):
        self.server.serve_forever()