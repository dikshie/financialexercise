#!/usr/bin/env python

import numpy as np
import pandas as pd
import datetime as dt
from urllib import urlretrieve
import pylab



#high frequency data (APPLE)

try:
    url = 'http://hopey.netfonds.no/posdump.php?'
    url += 'date=%s%s%s&paper=AAPL.O&csv_format=csv' % ('2014', '03', '12')
    # you may have to adjust the date since only recent dates are available
    urlretrieve(url, 'aapl.csv')
except:
    pass

AAPL = pd.read_csv('aapl.csv', index_col=0, header=0, parse_dates=True)
print AAPL.info()

AAPL['bid'].plot()
#pylab.savefig('graph7.png')
AAPL = AAPL[AAPL.index > dt.datetime(2014, 3, 12, 10, 0, 0)]
  # only data later than 10am at that day

# this resamples the record frequency to 5 minutes, using mean as aggregation rule
AAPL_5min = AAPL.resample(rule='5min', how='mean').fillna(method='ffill')
AAPL_5min.head()

AAPL_5min['bid'].plot()

AAPL_5min['bid'].apply(lambda x: 2 * 530 - x).plot()
  # this mirrors the stock price development at 


