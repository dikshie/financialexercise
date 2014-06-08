## Python Implementation of LSM
from pylab import *
# Parameters
M = 50
I = 10*4096
S0 = 36.
r = 0.06
vol = 0.2
K = 40.
T = 1.0
dt = T / M
df = exp(-r * dt)
# Simulation of Index Levels
S = zeros((M + 1, I), 'd')
S[0, :] = S0
for t in range(1, M + 1):
    ran = standard_normal(I)
    S[t, :] = S[t - 1, :] * exp((r - vol ** 2 / 2) * dt
                    + vol * ran * sqrt(dt))
h = maximum(K - S, 0)  # Inner Values
V = zeros_like(h)
V[-1] = h[-1]
# Valuation by LSM
for t in range(M - 1, 0, -1):
    rg = polyfit(S[t, :], V[t + 1, :] * df, 3)
    C = polyval(rg, S[t, :])
    V[t, :] = where(h[t, :] > C, h[t, :],
                     V[t + 1, :] * df)
V0 = sum(V[1, :] * df) / I  # LSM Estimator
print "Option Value %8.3f" % V0
