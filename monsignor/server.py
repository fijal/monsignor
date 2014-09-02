
from twisted.internet.protocol import ServerFactory
from monsignor.msg import unpack, LoginMessage, Message, LoginReply,\
     MessageReply
from monsignor.protocol import MonsignorProtocol

class MonsignorServerProtocol(MonsignorProtocol):
    username = None

    def __init__(self, factory):
        self.factory = factory

    def stringReceived(self, data):
        msg = unpack(data)
        if isinstance(msg, LoginMessage):
            if msg.username not in self.factory.passwords:
                self.send_message(LoginReply(False,
                                  "Unknown user or wrong password"))
                return
            if msg.password != self.factory.passwords[msg.username]:
                # XXX timing attack
                self.send_message(LoginReply(False,
                                  "Unknown username or wrong password"))
                return                
            self.factory.clients[msg.username] = self
            self.username = msg.username
            self.send_message(LoginReply(True, msg.username))
            return
        # for any other message, check if it's logged in
        
        if isinstance(msg, Message):
            self.handle_message(msg)
        else:
            xxxx

    def handle_message(self, msg):
        try:
            peer = self.factory.clients[msg.receipent]
        except KeyError:
            self.send_message(MessageReply(False, "receipent unknown"))
        else:
            self.send_message(MessageReply(True, None))
            peer.send_message(msg)

class MonsignorServerFactory(ServerFactory):
    def __init__(self, passwords):
        self.clients = {}
        self.passwords = passwords
        
    def buildProtocol(self, addr):
        return MonsignorServerProtocol(self)
