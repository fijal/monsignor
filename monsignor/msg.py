
from monsignor.packer import Packer, Unpacker, UnpackingError

LOGIN, CONTENT = range(1, 3)

class BaseMessage(object):
    def __init__(self):
        pass

def unpack(buf):
    u = Unpacker(buf)
    msg_type = u.unpack_byte()
    if msg_type == CONTENT:
        receipent = u.unpack_string()
        content = u.unpack_string()
        retval = Message(receipent, content)
    elif msg_type == LOGIN:
        username = u.unpack_string()
        retval = LoginMessage(username)
    else:
        raise UnpackingError("wrong message type %d" % msg_type)
    if not u.done():
        raise UnpackingError("supefluous bytes")
    return retval

class Message(BaseMessage):
    def __init__(self, receipent, content):
        self.receipent = receipent
        self.content = content

    def pack(self):
        p = Packer()
        p.pack_byte(CONTENT)
        p.pack_string(self.receipent)
        p.pack_string(self.content)
        return p.finish()

class LoginMessage(BaseMessage):
    def __init__(self, username):
        self.username = username
    
    def pack(self):
        p = Packer()
        p.pack_byte(LOGIN)
        p.pack_string(self.username)
        return p.finish()
