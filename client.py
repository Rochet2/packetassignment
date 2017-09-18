#!/usr/bin/python

import json

import pandas as pd

import inputgenerator
import receiver

records = []
try:
    while True:
        packets = receiver.Receive()

        success_packets = filter(lambda x: x[1], packets)
        total = len(packets)
        succeeded = len(success_packets)
        bytessuccdecoded = sum(map(lambda x: len(x[0]), success_packets))
        record = {
            "packets_successfully_decoded_pct": succeeded / float(total),
            "packets_successfully_decoded": succeeded,
            "bytes_successfully_decoded_pct": bytessuccdecoded / float(inputgenerator.length),
            "bytes_successfully_decoded": bytessuccdecoded,
        }
        records.append(record)
        print(record)
except KeyboardInterrupt:
    pass

df = pd.read_json(json.dumps(records))  # type: pd.DataFrame
df.to_json("output_client.json")
print("wrote records!")
