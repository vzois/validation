import sys
from random import randint
from heapq import nsmallest


MAX_VALUE = 1024*1024

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

    print "(rd) k-smallest element:", num,hex(num)
    
if len(sys.argv) < 3:
    print "Please provide a valid vector size and k-th element value!!!"
    exit(1)
    
size = int(sys.argv[1])
k = int(sys.argv[2])


print "Size:", size


data = [randint(0,MAX_VALUE) for i in range(size)]
#print data

#for d in data:
#    print hex(d),hex(hexDigit(d,3))

nsmall = nsmallest(k,data)
kmax=max(nsmall)

radixselect(data,k)

#print "k smallest elements:", nsmall,kmax, hex(kmax)
print "(py) k smallest element:", kmax,hex(kmax)