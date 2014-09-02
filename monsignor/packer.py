
import struct
from cStringIO import StringIO

SIZE_OF_LONG = struct.calcsize("l")

class UnpackingError(Exception):
    pass

class Packer(object):
    def __init__(self):
        self.buf = StringIO()

    def pack_string(self, s):
        if not s:
            self.pack_int(0)
        else:
            self.pack_int(len(s))
            self.buf.write(s)

    def pack_byte(self, b):
        self.buf.write(struct.pack("b", b))

    def pack_int(self, i):
        # XXX more compact encoding
        self.buf.write(struct.pack("l", i))

    def finish(self):
        retval = self.buf.getvalue()
        self.buf = None
        return retval

class Unpacker(object):
    def __init__(self, buf):
        self.buf = buf
        self.pos = 0

    def _check_size(self, size):
        if self.pos + size > len(self.buf):
            raise UnpackingError("Not enough bytes")

    def unpack_string(self):
        length = self.unpack_int()
        self._check_size(length)
        if not length:
            retval = None
        else:
            retval = self.buf[self.pos:self.pos + length]
            self.pos += length
        return retval

    def unpack_int(self):
        self._check_size(SIZE_OF_LONG)
        retval, = struct.unpack("l", self.buf[self.pos:self.pos + SIZE_OF_LONG])
        self.pos += SIZE_OF_LONG
        return retval

    def unpack_byte(self):
        self._check_size(1)
        retval, = struct.unpack("b", self.buf[self.pos:self.pos + 1])
        self.pos += 1
        return retval

    def unpack_bool(self):
        return bool(self.unpack_byte())

    def done(self):
        return self.pos == len(self.buf)
