
import sys
from twisted.python import log
from twisted.trial.unittest import TestCase
from twisted.protocols.loopback import loopbackAsync
from twisted.internet.defer import inlineCallbacks
from monsignor.server import MonsignorServerFactory
from monsignor.client import MonsignorClientProtocol
from monsignor.msg import Message

log.startLogging(sys.stderr, setStdout=0)

def get_connection(server_fact, name, password):
    server_prot = server_fact.buildProtocol(None)
    client_prot = MonsignorClientProtocol(name, password)
    return loopbackAsync(server_prot, client_prot), client_prot

class TestServerClientNoNet(TestCase):
    @inlineCallbacks
    def test_basic_message(self):
        fact = MonsignorServerFactory({"bob": "p", "alice": "p2"})
        finished, bob = get_connection(fact, "bob", "p")
        finished2, alice = get_connection(fact, "alice", "p2")
        result = yield alice.poll_message()
        assert result.username == "alice"
        result = yield bob.poll_message()
        assert result.username == "bob"
        bob.send_message(Message("alice", "content"))
        result = yield alice.poll_message()
        assert result.receipent == "alice"
        assert result.content == "content"
        bob.disconnect()
        alice.disconnect()
        yield finished
        yield finished2

    @inlineCallbacks
    def test_missing_receipent(self):
        fact = MonsignorServerFactory({"bob": "p"})
        finished, bob = get_connection(fact, "bob", "p")
        result = yield bob.poll_message()
        assert result.username == "bob"
        bob.send_message(Message("alice", "content"))
        result = yield bob.poll_message()
        assert not result.success
        bob.disconnect()
        yield finished

    @inlineCallbacks
    def test_not_logged_in(self):
        fact = MonsignorServerFactory({})
        finished, bob = get_connection(fact, "bob", "p")
        bob.disconnect()
        result = yield bob.poll_message()
        assert not result.success
        assert result.username == "Unknown user or wrong password"
        yield finished
