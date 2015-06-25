'''
Created on Jun 20, 2015

@author: Robert
@todo: Consider changing from using threading to using multiprocessing/thread combination
https://docs.python.org/2/library/multiprocessing.html
# Port: 60606
'''
import SocketServer
import time
import socket
import threading
from core.centralAPI import APIConnection

class EchoRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        self.request.send(data)
        return

'''
@summary: Central Server Socket Operator
'''
class AdvancedServerListener(threading.Thread):
    port = 60606
    url = 'localhost'
    backlog = 5
    initiated = False
    myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    myAPIConnections = []
    contListen = False
    
    # Constructor
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stop = threading.Event()
    
    '''
    # Thread Operation
    # listens on designated socket and creates connection threads
    @todo: Create cleanup of connection threads stored in the array
    '''
    def run(self):
        print 'Starting Run'
        self.contListen = True
        if self.initiated == False:
            self.initiate()
        while self.contListen:
            print 'Waiting on Connection'
            (clientsocket, address) = self.myServerSocket.accept()
            print 'New Connection Established'
            tempAPIConnection = APIConnection(len(self.myAPIConnections), 'APIConnectionThread-' + str(len(self.myAPIConnections)), clientsocket)
            tempAPIConnection.start()
            self.myAPIConnections.append(tempAPIConnection)
    
    def initiate(self):
        print 'Initiating Listener'
        if self.initiated:
            self.myServerSocket.close()
        self.myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.myServerSocket.bind((self.url, self.port))
        self.myServerSocket.listen(self.backlog)
        self.initiated = True
    
    def shutdown(self):
        if self.initiated:
            print 'Shutdown Listener'
            for connection in self.myAPIConnections:
                connection.shutdown()
            self.contListen = False
            self.myServerSocket.close()
        self.stop.set()
    
    def setNewPort(self, newPort):
        self.port = newPort
        self.initiate()
        
    def setNewUrl(self, newURL):
        self.url = newURL
        self.initiate()
        
    def setNewBacklog(self, newBack):
        self.backlog = newBack
        self.initiate()

if __name__ == '__main__':
    
    myServer = AdvancedServerListener(1, "Listener-1")
    myServer.start()
    time.sleep(1)
    print 'Creating Client Connection'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((myServer.url, myServer.port))
    print 'Client Connection Established'
    
    time.sleep(1)
    s.send("Hello")
    time.sleep(1)
    s.send("Meow")
    time.sleep(1)
    s.close()
    
    myServer.shutdown()
    
    exit()