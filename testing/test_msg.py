
from monsignor.msg import Message, unpack

class TestMsg(object):
    def test_basic_msg(self):
        msg = Message("bob", "some content")
        buf = msg.pack()
        remsg = unpack(buf) 
        assert isinstance(remsg, Message)
        assert remsg.content == "some content"
