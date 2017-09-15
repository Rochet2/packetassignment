#!/usr/bin/python3

import socket
import inputgenerator
import resultchecker


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
        Then returns the data string received so far.
        """
        result = ""
        i = 0
        while True:
            try:
                id, data = self.recv()
            except socket.timeout:
                break
            print(id, i)
            if id == i:
                result += data
                i += 1
            if id > i:
                while id > i:
                    result += self.getcontentlen() * inputgenerator.lostindicator
                    i += 1
                    # skip packets with lower id than we have already received
                    # they are duplicates.
        return result

    def getcontentlen(self):
        return self.packetlen-1


def printresult(msg):
    right, wrong, equal, expectedlen, msglen = resultchecker.check(msg)
    print("MSG! len: {}/{} equal: {} right: {} wrong: {}".format(msglen, expectedlen, "yes" if equal else "NO", right, wrong))


messages = []

try:
    while True:
        r = Receiver(socket.gethostname(), 12345)
        msg = r.receive()
        r.socket.close()
        printresult(msg)
        messages.append(msg)
except KeyboardInterrupt:
    pass

print(resultchecker.check(messages))
