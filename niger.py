#!/usr/bin/python
import shapefile
import cPickle as pickle     # dump and load data structures
from pprint import pprint

# !EEE 64 bit numbers
def latlonstr(lat,lon):
    fspec = '%.15f'
    return fspec % lat + ',' + fspec % lon

def shapeID(sr):
    return sr.record[7]	# a magic number 

def downstreamID(sr):   
    return sr.record[14] # This magic number refers to TRAVEL

# the points [[a,b],[c,d]] data structure represents
# a vector from the upstream coordinate to the downstream
# coordinate

# create key based on upstream point
def upstream(rec):
    latlon = rec.shape.points[0]
    return latlonstr(latlon[0],latlon[1])

def downstream(rec):
    latlon = rec.shape.points[1]
    return latlonstr(latlon[0],latlon[1])

# create initial upstream coordinate -> cell map
# and cell -> coordinate pair map
def pass1(shapes):
    dct = dict()
    pntMap = dict()
    for rec in shapes.shapeRecords():
	tgt = upstream(rec)
        sID = shapeID(rec)
	dct[tgt] = [sID]    # target goes to segment shape ID and empty list
        pntMap[sID] = rec.shape.points
    return (dct, pntMap)

def pass2(shapes, dct):
    for rec in shapes.shapeRecords():
	src = downstream(rec)
	if src in dct:
	    IDlist = dct[src]
            IDlist.append(shapeID(rec)) # gotcha: this modifies the list and returns none
	    dct[src] = IDlist 
    return dct	 
	
def pass3(dct):
    idmap = dict()
    for item in dct:
      IDlist = dct[item]
      idmap[IDlist[0]] = IDlist[1:]   # make the first map to the rest
    return idmap

def preprocess(shapefilename):
    sh = shapefile.Reader(shapefilename)
    maps = pass1(sh)
    return (pass3(pass2(sh, maps[0])), maps[1])

if __name__ == '__main__':
    maps = preprocess("Niger_River_Active_1min.shp")
    mapfile = open("NigerDictionary", "w")  # write dictionaries
    pickle.dump(maps, mapfile)
    mapfile.close()

    print "Written to disk. Delete the map data structure."
    del maps
    print "Read back"

    mapfile = open("NigerDictionary.pck", "r")
    newmaps = pickle.load(mapfile)
    pprint(newmaps[0])
    pprint(newmaps[1])
    exit(0)

    shape = sh.shapes()
    print len(sh.fields), " fields: ", sh.fields
    print "Loading records..."
    sr = sh.shapeRecords()
    rec0 = sr[0]
    print "shapeType: ", rec0.shape.shapeType
    print len(rec0.shape.points), "points: ", rec0.shape.points
    print "bbox:", rec0.shape.bbox
    print len(rec0.record), "record: ", rec0.record
    for sr in sh.shapeRecords():
        shp = sr.shape
        print shp.bbox
        print shp.bbox[2]-shp.bbox[0],shp.bbox[3]-shp.bbox[1]
	print "ID: ", sr.record[7]
	print "NAME:", sr.record[8]
	print "UPSTREAM:", sr.record[9]
