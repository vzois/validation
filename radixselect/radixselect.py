import sys
from random import randint
from heapq import nsmallest

import random
from datetime import datetime

import os
import struct
from mbin import loadRank, loadPoints, storeRank, storePoints

import time

MAX_VALUE = 1024*1024*1024

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

###############################
#        MAIN FUNCTION        #
###############################
Debug = True
r = True
points = []
store = []

#print "Generating or reading data...."
if r:
    print "Generating data...."
    fp = open("config.h","r")
    for line in fp.readlines():
        if line.strip().startswith("#define N"):
            N = int(line.strip().split(" ")[2])
        elif line.strip().startswith("#define K"):
            k = int(line.strip().split(" ")[2])

    fp.close()

    rank = [randValue() for i in range(N)]
    if Debug:
        for i in range(0,128,8):
            print [ hex(rank[v]) for v in range(i,i+8)]
    storeRank(rank)

else:
    print "Reading data...."
    rank = loadRank()
    print "load rank:"#,rank
    
    if Debug:
        for i in range(0,128,8):
            print [ hex(rank[v]) for v in range(i,i+8)]
        
    points = loadPoints(len(rank))



heaptime = time.time()
nsmall = nsmallest(k,rank)
heaptime = time.time() - heaptime

heapK=max(nsmall)
rdxselecttime = time.time()
rdxK=rselect(rank,k)

print "(heapK) time", heaptime
print "(rdxK) time", time.time() - rdxselecttime

print "(heapK) k smallest element:", heapK,hex(heapK)
print "(rdxK) k smallest element:", rdxK,hex(rdxK)


    






