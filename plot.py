#!/usr/bin/env python3

import re
import csv
import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} <path>')
    os.sys.exit(1)
path = sys.argv[1]

data = pd.read_csv(path, parse_dates=True)
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date').tz_localize('Etc/GMT0').tz_convert('Etc/GMT-3').reset_index()
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Hour'] = data['Date'].dt.hour
apps = data['App'].unique()

fig, axs = plt.subplots(nrows=len(apps))

start_date = '2019-07-01'
end_date = data['Date'].max().to_pydatetime().date()

plt.suptitle(f'Pedidos a apps {start_date} a {end_date}', size='small')

for app, ax in zip(apps, axs):
    data_app = data[data['Date'] >= start_date]
    data_app = data_app[data_app['App'] == app]
    data_app = data_app.groupby(['Hour', 'User'], as_index=False).count()
    data_app = data_app.rename(columns={'Date': 'count'})

    ax.set_title(app)

    bottom = None
    users = data_app['User'].unique()
    for user in users:
        du = data_app[data_app['User'] == user]

        index = pd.Index(np.arange(0, 24), name='Hour')
        du = du.set_index('Hour').reindex(index)
        du = du.fillna(0).reset_index()

        values = du['count'].values

        if bottom is None:
            bottom = np.zeros(len(values))

        ax.bar(du['Hour'].values, values, bottom=bottom, alpha=0.75)
        bottom += values

    ax.legend(users)
    ax.set_ylabel('Pedidos')
    ax.set_xlabel('Hora')
    ax.set_xticks(np.arange(0, 24, 2))


plt.tight_layout()
fig.savefig('apps.png')
plt.show()
