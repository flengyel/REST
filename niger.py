#!/usr/bin/python
# preprocess ESRI shape file for 1min resolution niger river network
import shapefile
import cPickle as pickle     # dump and load data structures

# !EEE 64 bit numbers
def latlonstr(lat,lon):
    fspec = '%.15f'
    return fspec % lat + ',' + fspec % lon

def shapeID(sr):
    return sr.record[7]	# a magic number 

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
    return (pass3(pass2(sh, maps[0])), maps[1]) # id -> [upstream list], id -> [[upstream coords[,[downstream coords]]

# the breadth first search should import this
def loadmaps(pickleFile):
    mapfile = open(pickleFile, "r")
    maps =  pickle.load(mapfile)
    mapfile.close()
    return maps

if __name__ == '__main__':
    maps = preprocess("Niger_River_Active_1min.shp")
    mapfile = open("NigerRiverDict", "w")  # write dictionaries
    pickle.dump(maps, mapfile)
    mapfile.close()
    exit(0)

