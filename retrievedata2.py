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



#log returns

rets = np.log(data / data.shift(1)) 
print rets.head()

#regression! 
xdat = rets['EUROSTOXX']
ydat = rets['VSTOXX']
model = pd.ols(y=ydat, x=xdat)
print model


import matplotlib.pyplot as plt
plt.plot(xdat, ydat, 'r.')
ax = plt.axis()  # grab axis values
x = np.linspace(ax[0], ax[1] + 0.01)
plt.plot(x, model.beta[1] + model.beta[0] * x, 'b', lw=2)
plt.grid(True)
plt.axis('tight')
#plt.savefig('graph4.png', format='png', bbox_inches='tight')


import matplotlib as mpl
mpl_dates = mpl.dates.date2num(rets.index)
plt.figure(figsize=(8, 4))
plt.scatter(rets['EUROSTOXX'], rets['VSTOXX'], c=mpl_dates, marker='o')
plt.grid(True)
plt.xlabel('EUROSTOXX')
plt.ylabel('VSTOXX')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
          format=mpl.dates.DateFormatter('%d %b %y'))

