
from monsignor.packer import Packer, Unpacker, UnpackingError

LOGIN, LOGIN_REPLY, CONTENT, CONTENT_REPLY = range(1, 5)

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
    elif msg_type == CONTENT_REPLY:
        success = u.unpack_byte()
        retval = MessageReply(success)
    elif msg_type == LOGIN:
        username = u.unpack_string()
        retval = LoginMessage(username)
    elif msg_type == LOGIN_REPLY:
        success = u.unpack_bool()
        username = u.unpack_string()
        retval = LoginReply(success, username)
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

class MessageReply(BaseMessage):
    def __init__(self, success):
        self.success = success

    def pack(self):
        p = Packer()
        p.pack_byte(CONTENT_REPLY)
        p.pack_byte(self.success)
        return p.finish()

class LoginMessage(BaseMessage):
    def __init__(self, username):
        self.username = username
    
    def pack(self):
        p = Packer()
        p.pack_byte(LOGIN)
        p.pack_string(self.username)
        return p.finish()

class LoginReply(BaseMessage):
    def __init__(self, success, username):
        self.username = username
        self.success = success

    def pack(self):
        p = Packer()
        p.pack_byte(LOGIN_REPLY)
        p.pack_byte(self.success)
        p.pack_string(self.username)
        return p.finish()
