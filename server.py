#!/usr/bin/python3

import socket
import random
import time
import sys
import inputgenerator


class Sender:
    def __init__(self, host, port, losspct=0, packetlen=100):
        self.address = (host, port)
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.losspct = losspct
        self.packetlen = packetlen
        self.packetid = -1
        assert losspct <= 1, "losspct must be in range [0,1]"
        assert losspct >= 0, "losspct must be in range [0,1]"
        assert self.packetlen > 0, "packetlen must be > 0"
        self.sentbytes = 0

    def send3(self, string):
        for p in self.split(string):
            p = chr(self.getpacketid())+p
            self.send_packet(p)
            self.send_packet(p)
            self.send_packet(p)

    def split(self, string):
        n = self.packetlen-1
        return [string[i:i + n] for i in range(0, len(string), n)]

    def send_packet(self, p):
        self.sentbytes += len(p)
        if random.random() < 1 - self.losspct:
            self.socket.sendto(p, self.address)

    def getpacketid(self):
        self.packetid += 1
        assert self.packetid <= 255, "Assumption is that max packet number is 255"
        assert self.packetid >= 0, "Assumption is that packet numbers start from 0"
        return self.packetid

    def getcontentlen(self):
        return self.packetlen-1

    @staticmethod
    def getlosspct():
        return len(sys.argv) > 1 and float(sys.argv[1]) or 0


expected = inputgenerator.randomstring(300)

while not str(input()):
    sender = Sender(socket.gethostname(), 12345, Sender.getlosspct())
    sender.send3(expected)





    # how to decode aaabbbcccddd can we insert additional data to the packets besides the payload?
    # Can we expect that no data is corrupted (only lost) so
    # that we can simply match if the contents of the packets
    # are same between 3 consecutive packets?
    # how do we determine when the packet stream ends?
    # how accurately should we match? If for example we compare
    # abde
    # abcde
    # then are only 2 characters(packets) correct or 4,
    # even though they are at wrong positions?
    # what should we do with missing characters if we are not be able to detect them


    # assumptions:
    # single burst of packets (asked in QA)
    # we can assume no more than 256 packets will ever arrive (asked in QA)
    # a packet takes no longer than 1 second for the receiver to receive (asked in QA)
    # ending of the packet stream is marked by not receiving packets for 1 second (asked in QA)
    # packet number can be from 0 to 255 (a single char)
    # first packet sent to the receiver is packet number 0 and the packet number is increased by 1
    # for each packet
    # inputgenerator.lostindicator does not occur in the input data and can be used to indicate
    # that there was a missing packet

    # document packet structure!