
import struct
from twisted.protocols.basic import Int32StringReceiver

class MonsignorProtocol(Int32StringReceiver):
    def send_message(self, msg):
        s = msg.pack()
        self.transport.write(struct.pack("!I", len(s)) + s)

