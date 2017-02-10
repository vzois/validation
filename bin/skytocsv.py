import sys
import struct

file = sys.argv[1]
N = int(file.split("_")[1])
D = int(file.split("_")[2])

outfile=file.split(".")[0]+".csv2"
f = open(file,"rb")
fw = open(outfile,"w")
print file, N, D, ">>>>", outfile

point_num = 1024
buffer = f.read(point_num*D)

while buffer:
    bytes = len(buffer)
    values = bytes / 4
    data=struct.unpack(values*'i',buffer);
    lines = []
    
    for i in range(0,len(data),D):
        #print data[i:i+D]
        #print ",".join([str(v) for v in data[i:i+D]])
        lines.append(",".join([str(v) for v in data[i:i+D]]))
        lines.append("\n")
        #points.append(data[i:i+D])
    fw.writelines(lines)
    
    buffer = f.read(point_num*D)



f.close()
fw.close()