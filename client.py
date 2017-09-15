#!/usr/bin/python

import socket
import inputgenerator
import resultchecker
import pandas as pd


class Receiver:
    def __init__(self, host, port, packetlen=100, timeout=1):
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
        i = 0
        while True:
            try:
                id, data = self.recv()
            except socket.timeout:
                break
            if id == i:
                decoded.append((data, True, id))
                i += 1
            if id > i:
                while id > i:
                    decoded.append((self.getcontentlen() * inputgenerator.lostindicator, False, id))
                    i += 1
                decoded.append((data, True, id))
                i += 1
                    # skip packets with lower id than we have already received
                    # they are duplicates.
        return decoded

    def getcontentlen(self):
        return self.packetlen-1


def printresult(msg):
    right, wrong, equal, expectedlen, msglen = resultchecker.check(msg)
    print("MSG! len: {}/{} equal: {} right: {} wrong: {}".format(msglen, expectedlen, "yes" if equal else "NO", right, wrong))


messages = []

try:
    while True:
        r = Receiver(socket.gethostname(), 12345)
        packets = r.receive()
        r.socket.close()
        success_packets = filter(lambda x: x[1], packets)
        total = len(packets)
        succeeded = len(success_packets)
        bytessuccdecoded = sum(map(lambda x: len(x[0]), success_packets))
        print("Succeeded decodes: {}%, payload bytes decoded: {}%".format(succeeded/float(total), bytessuccdecoded/float(inputgenerator.length)))
except KeyboardInterrupt:
    pass

#corrtrans, corrdata = resultchecker.stats(messages)
#print("Results! totally correct transmissions: {} pct of correct data: {}".format(corrtrans, corrdata))
