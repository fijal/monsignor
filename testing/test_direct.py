
from twisted.trial.unittest import TestCase
from twisted.protocols.loopback import loopbackAsync
from twisted.internet.defer import inlineCallbacks
from monsignor.server import MonsignorServerFactory
from monsignor.client import MonsignorClientProtocol
from monsignor.msg import Message

class TestServerClientNoNet(TestCase):
    @inlineCallbacks
    def test_basic_message(self):
        server_fact = MonsignorServerFactory()
        bob_prot = server_fact.buildProtocol(None)
        alice_prot = server_fact.buildProtocol(None)
        bob = MonsignorClientProtocol(None, "bob")
        alice = MonsignorClientProtocol(None, "alice")
        finished = loopbackAsync(bob_prot, bob)
        finished2 = loopbackAsync(alice_prot, alice)
        bob.send_message(Message("alice", "content"))
        result = yield alice.poll_message()
        assert result.receipent == "alice"
        assert result.content == "content"
        bob.disconnect()
        alice.disconnect()
        yield finished
        yield finished2
