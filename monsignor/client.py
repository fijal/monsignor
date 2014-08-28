
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred
from monsignor.msg import LoginMessage, unpack
from monsignor.protocol import MonsignorProtocol

class MonsignorClientProtocol(MonsignorProtocol):
    def __init__(self, factory, username):
        self.factory = factory
        self.username = username
        self.msgs = []

    def disconnect(self):
        self.transport.loseConnection()

    def poll_message(self):
        self._msg_deferred = Deferred()
        return self._msg_deferred

    def stringReceived(self, data):
        if self._msg_deferred is not None:
            self._msg_deferred.callback(unpack(data))
            self._msg_deferred = None
        else:
            xxx

    def connectionMade(self):
        self.send_message(LoginMessage(self.username))

    def connectionLost(self, reason):
        if hasattr(self, '_waiting_deferred'):
            self._waiting_deferred.callback(None)

class MonsignorClientFactory(ClientFactory):
    def __init__(self, username):
        self.username = username
    
    def buildProtocol(self, addr):
        return MonsignorClientProtocol(self, self.username)
