import os
import struct

def loadRank():
    rank=[]
    f = open("rank.bin","rb")
    bytes = f.read(1024)
    while bytes:
        count = len(bytes)/4
        num=struct.unpack(count*'i',bytes);
        rank = rank + list(num)
        bytes = f.read(16)
    #print rank
    f.close()
    return rank

def loadPoints(N):
    points = []
    #print os.path.getsize("points.bin")
    
    D = (os.path.getsize("points.bin")/4)/N
    #print "dimension:",D
    
    f = open("points.bin","rb")
    bytes = f.read(4*D)
    
    while bytes:
         num=struct.unpack(D*'i',bytes);
         #print num
         bytes = f.read(4*D)
         points = points + [list(num)]
    f.close()
    return points

def storeRank(rank):
    f = open("rank.bin","wb")
    for r in rank:
        f.write(struct.pack('i', r))
    f.close()

def storePoints(points):
    f = open("points.bin","wb")
    for p in points:
        for d in p:
            f.write(struct.pack('i', d))
    f.close()