import struct


TPS = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
RPM = range(500, 18500, 500)

TPS_POS = range(0,len(TPS))
RPM_POS = range(0, len(RPM))

def rpm_to_pos(rpm):
    return RPM.index(rpm)

def tps_to_pos(tps):
    return TPS.index(tps)

def dump_map(map, label=""):
    rev_TPS_POS = TPS_POS[:]
    rev_TPS_POS.reverse()
    if (len(label)):
        print label + ":"
    for tps in rev_TPS_POS:
        print "%3d:" % TPS[tps],
        for rpm in RPM_POS:
            print "%5d" % map[(rpm, tps)],
        print "\n",
    print "     ",
    for rpm in RPM:
        print "%5d" % rpm,
    print "\n",

def get_adjacent_values(map, tps, rpm):
    vals = []
    for r in range(-1,2):
        for t in range(-1,2):
            if (rpm+r, tps+t) in map and (rpm+r, tps+t) != (rpm, tps):
                vals.append(map[(rpm+r, tps+t)])
    return vals

def get_adjacent_values_ex(map, tps, rpm, min_rpm, max_rpm, min_tps, max_tps):
    vals = []
    for r in range(-1,2):
        for t in range(-1,2):
            if (rpm+r, tps+t) in map and (rpm+r, tps+t) != (rpm, tps) and min_rpm <= rpm+r <= max_rpm and min_tps <= tps+t <= max_tps:
                vals.append(map[(rpm+r, tps+t)])
    return vals

def read_map_file(filename):
    mapfile = open(filename, "rb")
    mapfile.seek(15) # skip first 15 bytes in file
    
    map = {}
    
    for rpm in RPM_POS:
        for tps in TPS_POS:
            byte = mapfile.read(1)
            num = struct.unpack('b', byte)[0]
            map[(rpm, tps)] =  num
        mapfile.seek(1, 1) # skip byte
    
    mapfile.close()
    
    return map

def save_map(orig, new, map):
    origfile = open(orig, "rb")
    newfile  = open(new, "wb")

    # keep same first 15 bytes
    for i in range(15):
        byte = origfile.read(1)
        num = struct.unpack('b', byte)[0]
        newfile.write(struct.pack('b', num))
        
    
    # write the map
    for rpm in RPM_POS:
        for tps in TPS_POS:
            newfile.write(struct.pack('b', map[(rpm, tps)]))
            origfile.seek(1,1)
        newfile.write(struct.pack('b', 0))
        origfile.seek(1,1)
        
    newfile.write(origfile.read())
    
    newfile.close()
    origfile.close()
