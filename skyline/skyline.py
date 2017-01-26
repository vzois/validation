import sys
from random import randint
from heapq import nsmallest

import random
from datetime import datetime

import os
import struct
from mbin import loadRank, loadPoints, storeRank, storePoints

import time

MAX_VALUE = 1024*1024

Debug = False

def randValue():
    global MAX_VALUE
    random.seed(datetime.now())
    return randint(1,MAX_VALUE)

def rselect(input,k):
    tmpK = k
    num = 0x0
    mN = 0x0
    mD = 0x0
    tmpV = input
    
    for d in range(7,-1,-1):
        buckets = [0 for i in range(17)]
        shf = d << 2
        mD = (0xF << shf)
        for i in input:
            digit = (i & mD) >> shf
            inc = ((i & mN) == num )
            buckets[digit+1]+=inc
        
        #print buckets
        pos = 0    
        for i in range(1,16):
            buckets[i+1] += buckets[i]
        
        global Debug
        if Debug:
            print [ hex(v) for v in buckets ]
        
        for i in range(1,17):
            if tmpK <= buckets[i]:
                pos = i
                break
            
        if tmpK != buckets[i-1]:
            tmpK = tmpK - buckets[i-1]
        
        #l = 0xFFFFFFFF&(~(shf))
        #num = (num & l) | ((pos-1) <<shf)
        num = num | ((pos-1) <<shf)
        mN = mN | mD
        #print hex(mN), hex(mD)
    return num

def DT(p,q):
    pb = False
    qb = False
    
    for i in range(len(p)):
        pb = ( p[i] < q[i] ) | pb;#At least one dimension better
        qb = ( q[i] < p[i] ) | qb;#No dimensions better
    
    return ~qb & pb

def BNL(points):
    sky=[0]

    for i in range(1,len(points)):
        q = points[i]
        dt = False
        rm = list()
        #print sky
        #sky = [sky[j] for j in range(len(sky)) if not DT(q,points[sky[j]]) ]
        
        for j in range(len(sky)):
            p = points[sky[j]]
            #print p,"<+!",q,
            if DT(p,q):
                #print "1 < 2"
                dt = True
            elif DT(q,p):
                #print "2 < 1"
                rm.append(j)
            #else:
            #    print ""
        #print rm, sky
        #print "rm:",rm,"sky:",sky
        sky = [sky[j] for j in range(len(sky)) if j not in rm]
        #for k in rm:
        #    #print k
        #    del sky[k]
        #    #print "del:",sky
        if not dt:
            sky.append(i)
    
    return sky       

def kss(window,points):
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
    
    
    #print sky_p
    #sky = BNL(sky_p)
    
    return sky

def sfs(points, rank):
    keys = range(len(rank))
    #print "k:",keys
    #print "k:",len(keys)," r:",len(rank)
    keys = [k for (r,k) in sorted(zip(rank,keys))]
    #pairs = sorted(pairs)
    #for i in range(len(rank)):
    #    print pairs[i],rank[pairs[i]]
        #print pairs[1],rank[pairs[1]]
        #print pairs[2],rank[pairs[2]]
    sky = [keys[0]]
    for i in keys:
        q = points[i]
        dt = False
        #print "sky:",sky
        for j in sky:
            #print j
            p = points[j]
            #print i,"=",p,",",q
            if DT(p,q):
                #print "dt---------->",p,",",q
                dt = True
                break
        if not dt and (i not in sky):
            sky.append(i)
    
    return sky  
        
def skySet(points,sky,rank):
    for j in sky:
        p = points[j]
        for i in range(len(points)):
            q = points[i]
            if DT(q,p):
                print i,"(",rank[i],")<",j,"(",rank[j],")"," : ",q,"<",p
    
r = True
points = []
store = []

#print "Generating or reading data...."
if r:
    print "Generating data...."
    N = int(sys.argv[1])
    D = int(sys.argv[2])
    
    for line in fp.readlines():
        if line.strip().startswith("#define N"):
            N = int(line.strip().split(" ")[2])
        elif line.strip().startswith("#define D"):
            D = int(line.strip().split(" ")[2])
        elif line.strip().startswith("#define K"):
            k = int(line.strip().split(" ")[2])

    fp.close()
    
    points = [[randValue() for i in range(D)] for j in range(N)]
    rank = [max(points[i]) for i in range(N)]
    storeRank(rank)
    #print "store rank:",rank
    storePoints(points)
    #print "store points:",points
else:
    print "Reading data...."
    rank = loadRank()
    print "load rank:"#,rank
    
    
    if Debug:
        for i in range(0,128,8):
            print [ hex(rank[v]) for v in range(i,i+8)]
        
    points = loadPoints(len(rank))
    #print "load points:",points



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

sfstime = time.time()
sky = sfs(points,rank)
sfstime = time.time() - sfstime
print "sfs:",len(sky)
print "sfs time",sfstime
print "sfs:",sorted(sky)
#skySet(points,sky,rank)

ksstime = time.time()
sky = kss(window,points)
ksstime = time.time()-ksstime
print "kss:",len(sky)
print "kss time:",ksstime
sky_p = [ points[i] for i in sky ]
sky_ = BNL(sky_p)
sky = [ sky[i] for i in sky_ ]
print "kss:",len(sky)
print "kss:",sorted(sky)
#skySet(points,sky,rank)


#print points[0]
#sky = BNL(points)
#print "bnl:",len(sky)
#print "bnl:",sorted(sky)
#skySet(points,sky,rank)


    






