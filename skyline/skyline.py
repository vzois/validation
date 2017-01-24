import sys
from random import randint
from heapq import nsmallest

import random
from datetime import datetime

import os
import struct
from mbin import loadRank, loadPoints, storeRank, storePoints

MAX_VALUE = 1024

def randValue():
    global MAX_VALUE
    random.seed(datetime.now())
    return randint(1,MAX_VALUE)

def rselect(input,k):
    tmpK = k
    num = 0x0
    mask = 0x0
    tmpV = input
    
    for d in range(7,-1,-1):
        buckets = [0 for i in range(17)]
        shf = d << 2
        m = (0xF << shf)
        for i in input:
            digit = (i & m) >> shf
            inc = ((i & mask) == num )
            buckets[digit+1]+=inc
        
        pos = 0    
        for i in range(1,16):
            buckets[i+1] += buckets[i]
        
        for i in range(1,17):
            if tmpK <= buckets[i]:
                pos = i
                break
            
        if tmpK != buckets[i-1]:
            tmpK = tmpK - buckets[i-1]
        
        l = 0xFFFFFFFF&(~(shf))
        num = (num & l) | ((pos-1) <<shf)
        mask = mask | m
    return num

def DT(p,q):
    pb = False
    qb = False
    
    for i in range(len(p)):
        pb = ( p[i] < q[i] ) | pb;#At least one dimension better
        qb = ( q[i] < p[i] ) | qb;#No dimensions better
    
    return ~qb & pb

def skyline(window,points):
    x=0
    
    sky = []
    for j in range(len(points)):
        dt = False
        q = points[j]
        for i in window:
            p = points[i]
            dt = DT(p,q)
            #print p, q, dt
            #print "--------------------------------"
            if dt:
                break
        if not dt:
            sky.append(j) 
        #print "sky:",sky
        
    return sky


r = True

points = []
store = []

k = 2

if r:
    N = int(sys.argv[1])
    D = int(sys.argv[2])
    
    points = [[randValue() for i in range(D)] for j in range(N)]
    rank = [sum(points[i]) for i in range(N)]
    storeRank(rank)
    print "store rank:",rank
    storePoints(points)
    print "store points:",points
else:
    
    rank = loadRank()
    print "load rank:",rank
    points = loadPoints(len(rank))
    print "load points:",points

nsmall = nsmallest(k,rank)
heapK=max(nsmall)
rdxK=rselect(rank,k)
print "(heapK) k smallest element:", heapK,hex(heapK)
print "(rdxK) k smallest element:", rdxK,hex(rdxK)

window = []
for i in range(len(rank)):
    if rank[i]<= rdxK:
        window.append(i)
        #print window

sky = skyline(window,points)
#print sky

    






