import sys
from random import randint
from heapq import nsmallest

import random
from datetime import datetime

import threading
import time

PRINT_ = True

MAX_VALUE = 1024

def randValue():
    global MAX_VALUE
    random.seed(datetime.now())
    return randint(0,MAX_VALUE)

def hexDigit(x,d):
    shf = d << 2
    mask = (0xF << (shf));
    return (x & mask) >> shf

def setHex(x,d,v):
    shf = d << 2
    mask = 0xFFFFFFFF&(~(0xF << shf))
    return (x & mask) | (v <<shf)

def swith(x,p,m):
    return ((x & m) == p )

def radixselect(input,k):
    buckets = [0 for i in range(17)]
    tmpK = k
    num = 0x0
    mask = 0x0

    debug = False
    for d in range(7,-1,-1):
        buckets = [0 for i in range(17)]
        for i in input:
            #if i <= num:
            if swith(i,num,mask):
                digit = hexDigit(i,d)
                buckets[digit+1]+=1
        if debug:
            print "<1>",d,buckets
        for i in range(1,16):
            buckets[i+1] += buckets[i]
        if debug:
            print "<2>",d,buckets
        
        pos = 0
        for i in range(1,17):
            if tmpK <= buckets[i]:
                pos = i
                break
        if debug:
            print "digit:",hex(pos),hex((pos-1))
            print "tmpK:",tmpK,"buckets:",buckets[i-1]
            
        if tmpK != buckets[i-1]:
            tmpK = tmpK - buckets[i-1]
        if debug:
            print "{",tmpK,"}"
        
        num = setHex(num,d,(pos-1))
        if debug:
            print "num:",hex(num)
        mask = mask | (0xF << (d << 2))
        if debug:
            print "m:",hex(mask)
            print "---------------------------------------------------------------------"

    global PRINT_
    if PRINT_:
        print "(rd) k-smallest element:", num,hex(num)
    return num


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
            #digit = (tmpV[i] & m) >> shf
            #inc = ((tmpV[i] & mask) == num )
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
        
        #num = setHex(num,d,(pos-1))
        mask = mask | m

    global PRINT_
    if PRINT_:
        print "(rd2) k-smallest element:", num,hex(num)
    return num


def par_rselect(input,k,p):
    size = len(input)
    
    global PRINT_
    PRINT_ = False
    k_list = [0 for i in range(p)]
    #print "_k:",_k
    for id in range(p):
        #print "id:",id
        low = (id * size)/p
        high =((id+1) * size)/p
        #print "(",low,",",high,")"
        #print input[low:high]
        k_list[id]=rselect(input[low:high],k)
    
    num = max(k_list)
    #print k_list,num,hex(num)
    
    rinput = list()
    for i in input:
        if i <= num:
            rinput.append(i)
    
    num =rselect(rinput,k)
    print "(rdp) k-smallest element:",num,hex(num)
    
if len(sys.argv) < 3:
    print "Please provide a valid vector size and k-th element value!!!"
    exit(1)
    
size = int(sys.argv[1])
k = int(sys.argv[2])


print "Size:", size


data = [randValue() for i in range(size)]
#print data

#for d in data:
#    print hex(d),hex(hexDigit(d,3))

heaptime = time.time()
nsmall = nsmallest(k,data)
kmax=max(nsmall)
heaptime = time.time() - heaptime
#print "k smallest elements:", nsmall,kmax, hex(kmax)
print "(py) k smallest element:", kmax,hex(kmax)

rdxtime = time.time()
radixselect(data,k)
rdxtime = time.time() - rdxtime

rdxopttime = time.time()
rselect(data,k)
rdxopttime = time.time() - rdxopttime

rdxpopttime = time.time()
par_rselect(data,k,4)
rdxpopttime = time.time() - rdxpopttime

print "heap time:", heaptime
print "rdxtime time:", rdxtime
print "rdxopttime time:", rdxopttime
print "rdxpopttime time:",rdxpopttime

#print data
#data.sort()
#print data







