#!/usr/bin/env python

import numpy as np
import pandas as pd
import pandas.io.data as pdd
from urllib import urlretrieve
import pylab

try:    
    index = pdd.DataReader('^GDAXI', data_source='yahoo', start='2007/3/30')
    # e.g. the EURO STOXX 50 ticker symbol -- ^SX5E
except:
    index = pd.read_csv('dax.txt', index_col=0, parse_dates=True)

print index.info()
print index.tail()

#log returns for whole time series
index['Returns'] = np.log(index['Close'] / index['Close'].shift(1))

#plot
index[['Close', 'Returns']].plot(subplots=True, style='b', figsize=(8, 5))
pylab.savefig('graph1.png', format='png', bbox_inches='tight')

# annual volatility changes over time
index['Mov_Vol'] = pd.rolling_std(index['Returns'], window=252) * np.sqrt(252)
# plot volatility
index[['Close', 'Returns', 'Mov_Vol']].plot(subplots=True, style='b', figsize=(8, 5))
pylab.savefig('graph2.png', format='png', bbox_inches='tight')


