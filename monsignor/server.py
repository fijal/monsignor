
from twisted.internet.protocol import ServerFactory, Protocol

class MonsignorServerProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

class MonsignorServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return MonsignorServerProtocol(self)
