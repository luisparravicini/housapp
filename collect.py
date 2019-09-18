#!/usr/bin/env python3

import re
import csv
import sys
import os
from datetime import datetime
import gzip
#from datetime import timezone, timedelta


def open_file(path):
    if path.endswith('.gz'):
        return gzip.open(path, 'rt')
    else:
        return open(path)


if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} <file1>[ <file2> [.. <fileN>]]')
    os.sys.exit(1)

log_re = re.compile(r'[\d+\.]+ - ([^-\s]+) \[(.+?)\] "[^"]+" \d+ \d+ "https?://(.+?)\.[^\.]+\.com/')
times = dict()
writer = csv.writer(sys.stdout)
writer.writerow(('Date', 'User', 'App'))

for path in sys.argv[1:]:
    with open_file(path) as f:
        for line in f:
            m = log_re.match(line)
            if m is None:
                continue

            d = datetime.strptime(m.group(2), '%d/%b/%Y:%H:%M:%S %z')
            # change timestamps to GMT-3
            # d = d.astimezone(timezone(-timedelta(hours=3)))
            ds = d.strftime('%Y-%m-%d %H:%M')

            datum = (ds, m.group(1), m.group(3))

            writer.writerow(datum)
