#!/usr/bin/python

import json
import math
import sys
import time

import pandas as pd

import inputgenerator
import sender


def getlosspct():
    return len(sys.argv) > 1 and float(sys.argv[1]) or None


losspct = getlosspct()
payload = inputgenerator.randomstring()

if losspct:
    record = sender.Send(payload, losspct)
    print(record)
    df = pd.read_json(json.dumps([record]))  # type: pd.DataFrame
    df.to_json("output_server.json")
else:
    records = []
    step = 0.01
    for i in (x * step for x in range(0, int(math.floor(1 / step)) + 1)):
        for n in [-0.001, 0, 0.001]:
            record = sender.Send(payload, max(min(i+n, 1), 0))
            records.append(record)
            print(record)
            time.sleep(0.15)
    df = pd.read_json(json.dumps(records))  # type: pd.DataFrame
    df.to_json("output_server.json")
