
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
from monsignor.msg import Message

log.startLogging(sys.stderr, setStdout=0)

class TestServerClient(TestCase):    
    @inlineCallbacks
    def test_server_basic(self):
        endpoint = TCP4ServerEndpoint(reactor, 0)
        server = MonsignorServerFactory()
        port = yield endpoint.listen(server)
        addr = port.getHost()
        client_endpoint = TCP4ClientEndpoint(reactor, "localhost", addr.port)
        client_prot = yield client_endpoint.connect(MonsignorClientFactory("bob"))
        d = Deferred()
        client_prot._waiting_deferred = d
        client_prot.disconnect()
        yield d
        yield port.stopListening()

    @inlineCallbacks
    def test_send_message_to_self(self):
        endpoint = TCP4ServerEndpoint(reactor, 0)
        server = MonsignorServerFactory()
        port = yield endpoint.listen(server)
        addr = port.getHost()
        client_endpoint = TCP4ClientEndpoint(reactor, "localhost", addr.port)
        client_prot = yield client_endpoint.connect(MonsignorClientFactory("bob"))

        client_prot.send_message(Message("bob", "foo"))
        res = yield client_prot.poll_message()
        assert res.username == "bob"
        res = yield client_prot.poll_message()
        assert res.receipent == "bob"
        assert res.content == "foo"

        d = Deferred()
        client_prot._waiting_deferred = d
        client_prot.disconnect()
        yield d
        yield port.stopListening()

    @inlineCallbacks
    def test_send_messages_two_clients(self):
        endpoint = TCP4ServerEndpoint(reactor, 0)
        server = MonsignorServerFactory()
        port = yield endpoint.listen(server)
        addr = port.getHost()
        client_endpoint = TCP4ClientEndpoint(reactor, "localhost", addr.port)
        client_prot = yield client_endpoint.connect(MonsignorClientFactory("bob"))
        client_prot2 = yield client_endpoint.connect(MonsignorClientFactory("alice"))
        res = yield client_prot2.poll_message()
        assert res.username == "alice"
        res = yield client_prot.poll_message()
        assert res.username == "bob"
        client_prot.send_message(Message("alice", "foo"))
        client_prot.send_message(Message("alice", "bar"))
        client_prot.send_message(Message("alice", "baz"))
        res = yield client_prot2.poll_message()
        assert res.receipent == "alice"
        assert res.content == "foo"
        res = yield client_prot2.poll_message()
        assert res.receipent == "alice"
        assert res.content == "bar"
        res = yield client_prot2.poll_message()
        assert res.receipent == "alice"
        assert res.content == "baz"

        d = Deferred()
        client_prot._waiting_deferred = d
        client_prot.disconnect()
        yield d
        d = Deferred()
        client_prot2._waiting_deferred = d
        client_prot2.disconnect()
        yield d
        yield port.stopListening()
