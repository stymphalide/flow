from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import src.controller as c

class SimpleEcho(WebSocket):

    def handleMessage(self):
      print(self.data)
      json_msg = c.parser(self.data)
      if(json_msg):
        self.sendMessage(json_msg)

    def handleConnected(self):
      print(self.address, 'connected')
      print(self.address, 'send initial game')
      self.sendMessage(c.parser('"start"'))

    def handleClose(self):
      print(self.address, 'closed')

server = SimpleWebSocketServer('', 5000, SimpleEcho)
server.serveforever()