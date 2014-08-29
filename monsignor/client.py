
from collections import deque
from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred, succeed
from monsignor.msg import LoginMessage, unpack
from monsignor.protocol import MonsignorProtocol

class MonsignorClientProtocol(MonsignorProtocol):
    def __init__(self, factory, username):
        self.username = username
        self.msgs = deque()

    def disconnect(self):
        self.transport.loseConnection()

    def poll_message(self):
        if not self.msgs:
            self._msg_deferred = Deferred()
            return self._msg_deferred
        else:
            return succeed(self.msgs.popleft())

    def stringReceived(self, data):
        if self._msg_deferred is not None:
            d = self._msg_deferred
            self._msg_deferred = None
            d.callback(unpack(data))
        else:
            self.msgs.append(unpack(data))

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
