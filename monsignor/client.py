
from twisted.internet.protocol import ClientFactory, Protocol

class MonsignorClientProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def disconnect(self):
        self.transport.loseConnection()

    def connectionLost(self, reason):
        if hasattr(self, '_waiting_deferred'):
            self._waiting_deferred.callback(None)

class MonsignorClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return MonsignorClientProtocol(self)
