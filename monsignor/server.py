
from twisted.internet.protocol import ServerFactory
from monsignor.msg import unpack, LoginMessage, Message, LoginSuccessful
from monsignor.protocol import MonsignorProtocol

class MonsignorServerProtocol(MonsignorProtocol):    
    def __init__(self, factory):
        self.factory = factory

    def stringReceived(self, data):
        msg = unpack(data)
        if isinstance(msg, LoginMessage):
            self.factory.clients[msg.username] = self
            self.send_message(LoginSuccessful(msg.username))
        elif isinstance(msg, Message):
            self.handle_message(msg)
        else:
            xxxx

    def handle_message(self, msg):
        try:
            peer = self.factory.clients[msg.receipent]
        except KeyError:
            xxx
        peer.send_message(msg)

class MonsignorServerFactory(ServerFactory):
    def __init__(self):
        self.clients = {}
        
    def buildProtocol(self, addr):
        return MonsignorServerProtocol(self)
