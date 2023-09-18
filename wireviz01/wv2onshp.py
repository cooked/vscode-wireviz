#!/usr/bin/env python3

import os
import sys
import argparse
import yaml
import csv

def expand_range(my_str):
    #= "1, 4-5, 7-11, 11"
    #print("The original string is : " + my_str) 
    temp = [(lambda sub: range(sub[0], sub[-1] + 1))(list(map(int, ele.split('-')))) for ele in my_str.split(', ')] 
    res = [b for a in temp for b in a]  
    return res

def main(arguments):

    #parser = argparse.ArgumentParser(
    #    description=__doc__,
    #    formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    #parser.add_argument('-o', '--outfile', help="Output file",
    #                    default=sys.stdout, type=argparse.FileType('w'))

    #args = parser.parse_args(arguments)
    filename = 'wvtest'

    with open(filename+'.yml', 'r') as file:
        wv = yaml.safe_load(file)

    with open(filename+'-from-to.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # header
        wr.writerow(['From Ref', 'From Pin', 'To Ref', 'To Pin', 'Wire ID', 'Diameter',	'Area',	'Gauge', 'Insulation',	'Bend Radius',	'Color'])

        for cnx in wv['connections']:
            
            fm = cnx[0]
            fm_ref = list(fm.keys())[0]
            fm_pins = str(list(fm.values())[0])[2:-2]
            fm_pins = expand_range(fm_pins)

            wi = cnx[1]
            wi_ref = list(wi.keys())[0]
            wi_nrs = str(list(wi.values())[0])[2:-2]
            wi_nrs = expand_range(wi_nrs)
            
            to = cnx[2]
            to_ref = list(to.keys())[0]
            to_pins = str(list(to.values())[0])[2:-2]
            to_pins = expand_range(to_pins)

            for fm_pin, wi_nr, to_pin in zip(fm_pins, wi_nrs, to_pins):
                wr.writerow([fm_ref, fm_pin, to_ref, to_pin, 
                            wi_ref+"_"+str(wi_nr), 1,	1,	1, 0.5,	10,	'#FF0000'])

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))