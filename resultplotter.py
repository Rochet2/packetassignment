#!/usr/bin/python

import pandas as pd
import matplotlib.pyplot as plt

server = pd.read_json("output_server.json")  # type: pd.DataFrame
client = pd.read_json("output_client.json")  # type: pd.DataFrame
df = pd.concat([server, client], axis=1)  # type: pd.DataFrame
df = df.fillna(0)

print(df)

df.plot(x='loss_pct', y=['packets_successfully_decoded_pct', 'bytes_successfully_decoded_pct']).plot()
plt.show()
