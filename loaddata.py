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
        if len(l) == 5: 
 	    ID,cropland,q,q25,q50 = [x for x in l]
	    dct[ID] = (float(cropland),float(q),float(q25),float(q50))
    return dct

if __name__ == '__main__':
    dct = loadIDdictionary('NigerShapefiles/NigerIDCropD2550.txt')
    print dct['220']
