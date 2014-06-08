#!/usr/bin/env python

import math   
from scipy import stats  

# Function Definition
def BS73_Call_Value(S0, K, T, r, sigma, dy):
    S0 = float(S0)
    denominator = sigma * math.sqrt(T)
    d1 = (math.log(S0 / K) + (r - dy + 0.5 * sigma ** 2) * T) / denominator
    d2 = d1 - sigma * math.sqrt(T)
    BS_C1 = S0 * math.exp(-dy * T) * stats.norm.cdf(d1, 0.0, 1.0)
    BS_C2 = K * math.exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0)
    BS_C = BS_C1 - BS_C2
    return BS_C

print "Call Value %8.3f" % BS73_Call_Value(100., 100., 1.0, 0.05, 0.25, 0.03)
