'''
Created on Jun 22, 2015

@author: Robert
'''
import SocketServer
import time
import socket
import threading

'''
@summary: API Connection Thread, manages communication between client and server
'''
class APIConnection(threading.Thread):
    contListen = False
        
    def __init__(self, threadID, name, newConnection):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.myConnection = newConnection
        self.stop = threading.Event()
        print self.name + ' - Established Connection: '
        
    def run(self):
        self.contListen = True
        while(self.contListen):
            message = self.myConnection.recv(1024)
            if len(message) > 0:
                self.processAPIRequest(message)
    
    def shutdown(self):
        self.contListen = False
        self.myConnection.close()
        print self.name + ' - Shutdown'
        self.stop.set()
    
    def processAPIRequest(self, newRequest):
        print self.name + ' - Received Message: ' + newRequest