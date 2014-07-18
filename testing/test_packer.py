
from monsignor.packer import Packer, Unpacker

class TestPacker(object):
    def test_pack_string(self):
        p = Packer()
        p.pack_string("xyz")
        buf = p.finish()
        u = Unpacker(buf)
        assert u.unpack_string() == "xyz"
        assert u.done()
