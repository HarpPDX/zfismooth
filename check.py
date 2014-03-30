import sys
import copy
import os.path
from optparse import OptionParser

import map as mapmod
    
def check_map(orig_map, outlier_indicator, min_rpm_pos, max_rpm_pos, min_tps_pos, max_tps_pos):
    for rpm in mapmod.RPM_POS:
        for tps in mapmod.TPS_POS:
            if min_rpm_pos <= rpm <= max_rpm_pos and min_tps_pos <= tps <= max_tps_pos: # don't check map outside of this range
                current_val = orig_map[(rpm, tps)]
                adjacent_vals = mapmod.get_adjacent_values_ex(orig_map, tps, rpm, min_rpm_pos, max_rpm_pos, min_tps_pos, max_tps_pos)
                adjacent_average = sum(adjacent_vals) / len(adjacent_vals)
                
                if current_val > adjacent_average + outlier_indicator or current_val + outlier_indicator < adjacent_average:
                    print "Outlier -> RPM: %5d, TPS: %3d, VAL: %3d, AVG: %3d" % (mapmod.RPM[rpm], mapmod.TPS[tps], current_val, adjacent_average)        
    
if __name__ == '__main__':

    usage = "usage: %prog [options] filename"
    version = "%prog 1.0"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-o", "--outlier", type="int", dest="outlier", default=10, help="% fuel change to indicate an outlier (optional, default 10)")
    parser.add_option("-d", "--dump", action="store_true", dest="dump", default=False, help="dump map to screen (optional, default off)")
    parser.add_option("-q", "--minrpm", type="choice", choices=[str(rpm) for rpm in mapmod.RPM], dest="minrpm", default='500',   help="minimum rpm to check (optional, default 500)")
    parser.add_option("-r", "--maxrpm", type="choice", choices=[str(rpm) for rpm in mapmod.RPM], dest="maxrpm", default='18000', help="maximum rpm to check (optional, default 18,000)")
    parser.add_option("-s", "--mintps", type="choice", choices=[str(tps) for tps in mapmod.TPS], dest="mintps", default='0',     help="minimum tps to check (optional, default 0)")
    parser.add_option("-t", "--maxtps", type="choice", choices=[str(tps) for tps in mapmod.TPS], dest="maxtps", default='100',   help="maximum tps to check (optional, default 100)")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("missing map filename")
    filename = args[0]

    original_map = mapmod.read_map_file(filename)

    if options.dump:
        mapmod.dump_map(original_map)

    check_map(original_map, options.outlier,
              mapmod.rpm_to_pos(int(options.minrpm)), 
              mapmod.rpm_to_pos(int(options.maxrpm)), 
              mapmod.tps_to_pos(int(options.mintps)), 
              mapmod.tps_to_pos(int(options.maxtps)))
            
