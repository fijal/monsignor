
from monsignor.packer import Packer, Unpacker, UnpackingError

class BaseMessage(object):
    def __init__(self):
        pass

class Message(BaseMessage):
    def __init__(self, content):
        self.content = content

    def pack(self):
        p = Packer()
        p.pack_string(self.content)
        return p.finish()

    @staticmethod
    def unpack(buf):
        u = Unpacker(buf)
        content = u.unpack_string()
        if not u.done():
            raise UnpackingError("supefluous bytes")
        return Message(content)
