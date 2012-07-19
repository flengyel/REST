#!/usr/bin/python
from __future__ import division
# return river network segment ID to (cropland area, q, q+25%, q+50%)
# Note that many segments have nothing upstream -- we must supply the
# nodata values -- they do not appear in the output processed by RGIS.


# Note: if there are missing values, this shows up as empty!
def loadIDdictionary(fname):
    dct = dict()
    for line in open(fname,'r'):
	l = line.split()
        if len(l) == 6: 
 	    ID,q,q25,q50,pop,crop = [x for x in l]
	    dct[ID] = (float(q),float(q25),float(q50),float(pop),float(crop))
    return dct

if __name__ == '__main__':
    dct = loadIDdictionary('NigerShapefiles/ID2q+q25+q50+pop+crop.txt')
    print dct['220']
    print dct['2202']
