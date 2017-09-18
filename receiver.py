import math
import socket

import inputgenerator


class __Receiver:
    def __init__(self, host, port, packetlen=100, timeout=0.1):
        """
        timeout is set only after receiving one packet.
        """
        self.address = (host, port)
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.socket.bind(self.address)
        self.packetlen = packetlen
        self.timeout = timeout
        self.timeoutisset = False
        assert self.packetlen > 0, "packetlen must be > 0"

    def recv(self):
        """
        Throws socket.timeout when timeout is exceeded.
        """
        packet, _ = self.socket.recvfrom(self.packetlen)
        if len(packet) < 2:
            return self.recv()
        if not self.timeoutisset:
            self.socket.settimeout(self.timeout)
            self.timeoutisset = True
        return ord(packet[0]), packet[1:]

    def receive(self):
        """
        Receives data until 1 second has passed since last packet.
        Then returns the tuples of (decoded data, successful, packetid).
        """
        decoded = []
        i = 1
        while True:
            try:
                id, data = self.recv()
            except socket.timeout:
                break
            idd = math.ceil((id + 1) / 3)
            if idd == i:
                decoded.append((data, True, id))
                i += 1
            if idd > i:
                while idd > i:
                    decoded.append((self.getcontentlen() * inputgenerator.lostindicator, False, id))
                    i += 1
                decoded.append((data, True, id))
                i += 1
            # skip packets with lower id than we have already received
            # they are duplicates.
        return decoded

    def getcontentlen(self):
        return self.packetlen - 1


def Receive():
    r = __Receiver(socket.gethostname(), 12345)
    packets = r.receive()
    r.socket.close()
    return packets
