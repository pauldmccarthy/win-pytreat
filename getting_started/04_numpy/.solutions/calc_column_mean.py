#!/usr/bin/env python
import numpy as np

data     = np.loadtxt('04_numpy/2d_array.txt', comments='%')
colmeans = data.mean(axis=0)
msg      = ''.join([chr(int(round(m))) for m in colmeans])

print('Column means')
print('\n'.join(['{}: {}'.format(i, m) for i, m in enumerate(colmeans)]))
print('Secret message:', msg)
