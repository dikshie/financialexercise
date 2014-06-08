#!/usr/bin/env python

import numpy as np
import pandas as pd
import datetime as dt
from urllib import urlretrieve
import pylab

try:
    es_url = 'http://www.stoxx.com/download/historical_values/hbrbcpe.txt'
    vs_url = 'http://www.stoxx.com/download/historical_values/h_vstoxx.txt'
    urlretrieve(es_url, 'es.txt')
    urlretrieve(vs_url, 'vs.txt')
except:
    pass

lines = open('es.txt').readlines()  # reads the whole file line-by-line
lines = open('es.txt').readlines()  # reads the whole file line-by-line
new_file = open('es50.txt', 'w')  # opens a new file
new_file.writelines('date' + lines[3][:-1].replace(' ', '') + ';DEL' + lines[3][-1])
    # writes the corrected third line (additional column name)
    # of the orginal file as first line of new file
new_file.writelines(lines[4:])  # writes the remaining lines of the orginal file
list(open('es50.txt'))[:5]  # opens the new file for inspection
es = pd.read_csv('es50.txt', index_col=0, parse_dates=True, sep=';', dayfirst=True)
del es['DEL']  # delete the helper column
print es.info()

vs = pd.read_csv('vs.txt', index_col=0, header=2, parse_dates=True, sep=',', dayfirst=True)

# you can alternatively read from the Web source directly
# without saving the csv file to disk:
# vs = pd.read_csv(vs_url, index_col=0, header=2,
#                  parse_dates=True, sep=',', dayfirst=True)


import datetime as dt
data = pd.DataFrame({'EUROSTOXX' :
            es['SX5E'][es.index > dt.datetime(1999, 12, 31)]})
data = data.join(pd.DataFrame({'VSTOXX' :
            vs['V2TX'][vs.index > dt.datetime(1999, 12, 31)]}))
print data.info()


print data.head()
data.plot(subplots=True, grid=True, style='b', figsize=(10, 5))
pylab.savefig('graph3.png', format='png', bbox_inches='tight')

#An investor has total wealth of say 100,000 EUR
#He invests, say, 70% of that into a diversified equity portfolio
#The remainder, i.e. 30%, is invested in the VSTOXX index directly
#Through (daily) trading the investor keeps the proportions constant
#No transaction costs apply, all assets are infinitely divisible

#Drop NAN

data = data.dropna()
data = data / data.ix[0] * 100
print data.head()
invest = 100
cratio = 0.3
data['Equity'] = (1 - cratio) * invest / data['EUROSTOXX'][0]
data['Volatility'] = cratio * invest / data['VSTOXX'][0]

data['Static'] = (data['Equity'] * data['EUROSTOXX']
                + data['Volatility'] * data['VSTOXX'])
data[['EUROSTOXX', 'Static']].plot(figsize=(10, 5))
pylab.savefig('graph5.png')


#daily adjustment

for i in range(1, len(data)):
    evalue = data['Equity'][i - 1] * data['EUROSTOXX'][i]
      # value of equity position
    vvalue = data['Volatility'][i - 1] * data['VSTOXX'][i]
      # value of volatility position
    tvalue = evalue + vvalue
      # total wealth 
    data['Equity'][i] = (1 - cratio) * tvalue / data['EUROSTOXX'][i]
      # re-allocation of total wealth to equity ...
    data['Volatility'][i] = cratio * tvalue / data['VSTOXX'][i]
      # ... and volatility position

#total wealth position
data['Dynamic'] = (data['Equity'] * data['EUROSTOXX']
                + data['Volatility'] * data['VSTOXX'])
print data.head()
#check ratio
print (data['Volatility'] * data['VSTOXX'] / data['Dynamic'])[:5]
print (data['Equity'] * data['EUROSTOXX'] / data['Dynamic'])[:5]

#check performance strategy
data[['EUROSTOXX', 'Dynamic']].plot(figsize=(10, 5))
pylab.savefig('graph6.png')

