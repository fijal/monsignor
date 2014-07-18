
from monsignor.msg import Message

class TestMsg(object):
    def test_basic_msg(self):
        msg = Message("some content")
        buf = msg.pack()
        assert Message.unpack(buf).content == "some content"
