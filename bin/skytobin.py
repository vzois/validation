import sys
import struct

file = sys.argv[1]
N = int(file.split("_")[1])
D = int(file.split("_")[2])

outfile=file.split(".")[0]+".bin"
f = open(file,"r")
fw = open(outfile,"w")
print file, N, D, ">>>>", outfile

val_size = 22
lines = 1024
buffer = f.read(val_size*D*lines)
while len(buffer) > 0:
    #print buffer
    
    outlist=list()
    for line in buffer.strip().split("\n"):
        data = line.strip().split(",")
        #print data
        for v in data:
            #print v,"--->",
            #print hex(int(round(float(v)*128)))
            outlist.append(int(round(float(v)*128)))
    fw.write(struct.pack('i'*len(outlist),*outlist))
        
    buffer = f.read(val_size*D*lines)



fw.close()
f.close()



