#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd

server = pd.read_json("output_server.json")  # type: pd.DataFrame
client = pd.read_json("output_client.json")  # type: pd.DataFrame
df = pd.concat([server, client], axis=1)  # type: pd.DataFrame
df = df.fillna(0)

print(df)

df["packets_not_decoded_pct"] = 1-df.packets_successfully_decoded_pct

df.plot(x='loss_pct', y=['packets_successfully_decoded_pct', 'packets_not_decoded_pct']).plot()
plt.show()
