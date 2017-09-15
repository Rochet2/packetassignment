import random
import socket


class __Sender:
    def __init__(self, host, port, losspct=0.0, packetlen=100):
        self.address = (host, port)
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.losspct = losspct
        self.packetlen = packetlen
        self.packetid = -1
        self.sentbytes = 0
        self.sentpackets = 0
        self.lostpackets = 0
        assert losspct <= 1, "losspct must be in range [0,1]"
        assert losspct >= 0, "losspct must be in range [0,1]"
        assert self.packetlen > 0, "packetlen must be > 0"

    def send3(self, string):
        for p in self.split(string):
            self.send_packet(p)
            self.send_packet(p)
            self.send_packet(p)

    def split(self, string):
        n = self.packetlen - 1
        return [string[i:i + n] for i in range(0, len(string), n)]

    def send_packet(self, p):
        p = chr(self.getpacketid()) + p
        self.sentbytes += len(p)
        self.sentpackets += 1
        if random.random() < 1 - self.losspct:
            self.socket.sendto(p, self.address)
        else:
            self.lostpackets += 1

    def getpacketid(self):
        self.packetid += 1
        assert self.packetid <= 255, "Assumption is that max packet number is 255"
        assert self.packetid >= 0, "Assumption is that packet numbers start from 0"
        return self.packetid

    def getcontentlen(self):
        return self.packetlen - 1


def Send(payload, losspct):
    sender = __Sender(socket.gethostname(), 12345, losspct)
    sender.send3(payload)
    return {
        "loss_pct": losspct,
        "bytes_sent": sender.sentbytes,
        "packets_sent": sender.sentpackets,
        "packets_lost": sender.lostpackets,
    }
