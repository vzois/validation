import sys
import struct
from subprocess import call
import time

N = int(sys.argv[1])
D = int(sys.argv[2])
distr = sys.argv[3]
scale = 1024 * 1024 * 1024

def genData(N,D,distr):
    global scale
    print time.time()
    filename = "d_"+str(N)+"_"+str(D)+"_"+distr
    print filename
    #Call d
    f = open(filename, "w")
    arg_call = ["./randdataset", "-"+distr,"-n",str(N),"-d",str(D),"-s",str(int(time.time()))]
    print arg_call
    call(arg_call,stdout=f)
    f.close()

##################################
# CREATE BINARY FILE
##################################
    #scale = 1024*1024 # SCALE VALUES
    infile = filename
    outfile=filename+".bin"
    f = open(infile,"r")
    fw = open(outfile,"w")
    print "Creating bin file: ",infile, N, D, ">>>>", outfile

    val_size = 22
    lines = 1024*32
    buffer = f.read(val_size*D*lines)
    while len(buffer) > 0:
        outlist=list()
        for line in buffer.strip().split("\n"):
            data = line.strip().split(",")
            for v in data:
                outlist.append(int(round(float(v)*scale)))
        fw.write(struct.pack('i'*len(outlist),*outlist))
        buffer = f.read(val_size*D*lines)
    fw.close()
    f.close()

##################################
# CREATE CSV FILE
##################################

    points=[]
    infile = filename+".bin"
    outfile=filename+".csv"
    f = open(infile,"rb")
    fw = open(outfile,"w")
    print "Creating csv: ",infile, N, D, ">>>>", outfile

    point_num = 1024*32
    buffer = f.read(point_num*D)

    while buffer:
        bytes = len(buffer)
        values = bytes / 4
        data=struct.unpack(values*'i',buffer);
        lines = []
    
        for i in range(0,len(data),D):
            points.append(list(data[i:i+D]))            
            lines.append(",".join([str(v) for v in data[i:i+D]]))
            lines.append("\n")
        fw.writelines(lines)
        buffer = f.read(point_num*D)
    f.close()
    fw.close()
    return points

genData(N,D,distr)




