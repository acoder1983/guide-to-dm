import pandas as pd
import numpy as np
from data import *
from math import sqrt


def manhattan(rating1, rating2):
    dist = 0.
    for i in xrange(rating1.size):
        if not(np.isnan(rating1[i])) and not(np.isnan(rating2[i])):
            dist += abs(rating1[i] - rating2[i])
    return dist


def recommend(user):
    # find most look-alike user in users
    dist = 999999
    neighbor = None
    for u in users:
        if u != user:
            d = manhattan(ratings[user], ratings[u])
            if d < dist:
                dist = d
                neighbor = u

    print 'neighbor is %s' % neighbor

    # find neighbor's bands not in user's
    recommends = []
    if neighbor != None:
        for b in bands:
            if np.isnan(ratings[user][b]) and not(np.isnan(ratings[neighbor][b])):
                recommends.append((b, ratings[neighbor][b]))
    return recommends


def pearson(rating1, rating2):
    '''
    r=a/(c*d)
    a = sig[1..n]{ (x-avg(x))*(y-avg(y))}
    c = sqrt(sig[1..n]{pow(x-avg(x),2)})
    d = sqrt(sig[1..n]{pow(y-avg(y),2)})
    '''
    r1 = []
    r2 = []
    for i in xrange(len(rating1)):
        if not(np.isnan(rating1[i]))and not(np.isnan(rating2[i])):
            r1.append(rating1[i])
            r2.append(rating2[i])
    r1 = np.array(r1)
    r2 = np.array(r2)
    a = c = d = 0.

    for i in xrange(r1.size):
        a += (r1[i] - r1.mean()) * (r2[i] - r2.mean())
        c += (r1[i] - r1.mean())**2
        d += (r2[i] - r2.mean())**2
    print a, c, d

    c = sqrt(c)
    d = sqrt(d)
    if c * d != 0.:
        r = a / (c * d)
        print r
        return r


def cossim(rating1, rating2):
    '''
    r=a/(b*c)
    a=dot(x,y)
    b=sqrt(sig(x**2))
    c=sqrt(sig(y**2))
    '''
    r1 = np.array(rating1)
    r2 = np.array(rating2)
    a = np.dot(r1, r2)
    b = c = 0.
    for x in xrange(r1.size):
        b += r1[x]**2
        c += r2[x]**2
    b = sqrt(b)
    c = sqrt(c)
    if b * c != 0.:
        r = a / (b * c)
        print r
        return r
