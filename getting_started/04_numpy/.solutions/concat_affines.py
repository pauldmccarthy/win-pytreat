#!/usr/bin/env python

import numpy        as np
import numpy.linalg as npla

def concat(*xforms):
    """Combines the given matrices (returns the dot product)."""

    result = xforms[0]

    for i in range(1, len(xforms)):
        result = np.dot(result, xforms[i])

    return result


def transform(xform, coord):
    """Transform the given coordinates with the given affine. """
    return np.dot(xform[:3, :3], coord) + xform[:3, 3]


s1func2struc = np.loadtxt('04_numpy/xfms/subj1/example_func2highres.mat')
s1struc2std  = np.loadtxt('04_numpy/xfms/subj1/highres2standard.mat')
s2func2struc = np.loadtxt('04_numpy/xfms/subj2/example_func2highres.mat')
s2struc2std  = np.loadtxt('04_numpy/xfms/subj2/highres2standard.mat')

s1func2std    = concat(s1struc2std, s1func2struc)
s2func2std    = concat(s2struc2std, s2func2struc)
s2std2func    = npla.inv(s2func2std)
s1func2s2func = concat(s2std2func, s1func2std)

print('Subject 1 functional -> Subject 2 functional affine:')
print(s1func2s2func)

testcoords = np.array([[ 0,   0,  0],
                       [-5, -20, 10],
                       [20,  25, 60]], dtype=np.float32)


def dist(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))



for c in testcoords:
    xc = transform(s1func2s2func, c)
    d  = dist(c, xc)
    c  = '{:6.2f} {:6.2f} {:6.2f}'.format(*c)
    xc = '{:6.2f} {:6.2f} {:6.2f}'.format(*xc)
    print('Transform: [{}] -> [{}] (distance: {})'.format(c, xc, d))
