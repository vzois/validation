import sys
from random import randint
from heapq import nsmallest


MAX_VALUE = 1024

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
    max_value = 0xFFFFFFFF
    mask = 0x0
    pred = 0x0
    
    buckets = [0 for i in range(16)]
    tmpK = k
    
    for d in range(7,-1,-1):
        buckets = [0 for i in range(16)]
        for i in input:
            if swith(i,pred,mask):         
                digit = hexDigit(i,d)
                buckets[digit]+=1

        print "<1>",d,buckets
        
        digit = 0
        for i in range(0,15):
            buckets[i+1] += buckets[i]
            
        for i in range(0,15):
            if buckets[i] >= tmpK:
                digit=i
                break
        
        tmpK = tmpK - buckets[i-1]
        print tmpK
        #pred = setHex(pred,d,digit)
        #print "<2>{",d,"}(",hex(digit),")",hex(pred),buckets
        mask = mask | ( 0xF << (d << 2))
        
        #print "---------------------------------------------------"

    #print buckets
    print "k-th largest",max_value,hex(max_value)

if len(sys.argv) < 3:
    print "Please provide a valid vector size and k-th element value!!!"
    exit(1)
    
size = int(sys.argv[1])
k = int(sys.argv[2])


print "Size:", size


data = [randint(0,MAX_VALUE) for i in range(size)]
#print data

for d in data:
    print hex(d),hex(hexDigit(d,3))

nsmall = nsmallest(k,data)
kmax=max(nsmall)
print "k smallest elements:", nsmall,kmax, hex(kmax)
#print "k smallest element:", kmax,hex(kmax)

radixselect(data,k)










