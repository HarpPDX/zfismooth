import sys
import copy
import os.path
from optparse import OptionParser

import map as mapmod
    
def smooth_map_value(orig_val, adjacent_vals, weight):
    adjacent_average = sum(adjacent_vals) / len(adjacent_vals)
    new_val = ((weight * orig_val) + adjacent_average) / (weight + 1)
    return new_val

def smooth_map(original_map, weight, iterations, min_rpm_pos, max_rpm_pos, min_tps_pos, max_tps_pos):
    orig_map = original_map.copy()
    new_map = {}
    for i in range(0, iterations):
        for rpm in mapmod.RPM_POS:
            for tps in mapmod.TPS_POS:
                if min_rpm_pos <= rpm <= max_rpm_pos and min_tps_pos <= tps <= max_tps_pos: # don't change map outside of this range
                    new_map[(rpm, tps)] = smooth_map_value(orig_map[(rpm, tps)], mapmod.get_adjacent_values_ex(orig_map, tps, rpm, min_rpm_pos, max_rpm_pos, min_tps_pos, max_tps_pos), weight)
                else:
                    new_map[(rpm, tps)] = orig_map[(rpm, tps)]
        orig_map = new_map.copy()
    
    return new_map    

if __name__ == '__main__':

    usage = "usage: %prog [options] filename"
    version = "%prog 1.0"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-w", "--weight", type="int", dest="weight", default=2, help="weight given to the original map cell value (optional, default 2)")
    parser.add_option("-i", "--iterations", type="int", dest="iterations", default=1, help="number of times to smooth the map (optional, default 1)")
    parser.add_option("-d", "--dump", action="store_true", dest="dump", default=False, help="dump map to screen (optional, default off)")
    parser.add_option("-q", "--minrpm", type="choice", choices=[str(rpm) for rpm in mapmod.RPM], dest="minrpm", default='500',   help="minimum rpm to smooth (optional, default 500)")
    parser.add_option("-r", "--maxrpm", type="choice", choices=[str(rpm) for rpm in mapmod.RPM], dest="maxrpm", default='18000', help="maximum rpm to smooth (optional, default 18,000)")
    parser.add_option("-s", "--mintps", type="choice", choices=[str(tps) for tps in mapmod.TPS], dest="mintps", default='0',     help="minimum tps to smooth (optional, default 0)")
    parser.add_option("-t", "--maxtps", type="choice", choices=[str(tps) for tps in mapmod.TPS], dest="maxtps", default='100',   help="maximum tps to smooth (optional, default 100)")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("missing map filename")
    filename = args[0]

    original_map = mapmod.read_map_file(filename)

    new_map = smooth_map(original_map, options.weight, options.iterations,
                         mapmod.rpm_to_pos(int(options.minrpm)), 
                         mapmod.rpm_to_pos(int(options.maxrpm)), 
                         mapmod.tps_to_pos(int(options.mintps)), 
                         mapmod.tps_to_pos(int(options.maxtps)))
        
    if options.dump:
        mapmod.dump_map(original_map, "original")
        mapmod.dump_map(new_map, "new")
            
    head,tail = os.path.split(filename)
    newfilename = os.path.join(head, "smooth_"+tail)
    
    mapmod.save_map(filename, newfilename, new_map)
    
    print "New map file saved as %s" % newfilename
    

            
