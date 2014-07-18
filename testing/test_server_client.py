
""" Integration tests that spawn real TCP connections
"""

import sys
from twisted.python import log
from twisted.trial.unittest import TestCase
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, Deferred
from monsignor.server import MonsignorServerFactory
from monsignor.client import MonsignorClientFactory

log.startLogging(sys.stderr, setStdout=0)

class TestServerClient(TestCase):
    @inlineCallbacks
    def test_server_basic(self):
        endpoint = TCP4ServerEndpoint(reactor, 0)
        server = MonsignorServerFactory()
        port = yield endpoint.listen(server)
        addr = port.getHost()
        client_endpoint = TCP4ClientEndpoint(reactor, "localhost", addr.port)
        client_prot = yield client_endpoint.connect(MonsignorClientFactory())
        d = Deferred()
        client_prot._waiting_deferred = d
        client_prot.disconnect()
        yield d
        yield port.stopListening()
