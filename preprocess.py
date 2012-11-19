#!/usr/bin/python
# preprocess ESRI shape file for 1min resolution niger river network
import shapefile
import cPickle as pickle     # dump and load data structures
import json		     # encode data structures with json strings
from   constants import Const
from   osgeo import ogr      # load the Niger RIver boundary

# !EEE 64 bit numbers
def latlonstr(lat,lon):
    fspec = '%.15f'
    return fspec % lat + ',' + fspec % lon

def shapeID(sr):
    return sr.record[7]	# a magic number 

# Return the Stahler stream order of the segment
def streamOrder(sr):
    return sr.record[11] # another magic number.

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

# create two dictionaries dct and pntMap
# dct maps an upstream coordinate to  [ID (upstreamID, order), (upstreamID, order),...]
# and the map pntMap, which maps a shape ID to a coordinate pair map
# the intention is that during the search, only coordinates > order will included.
# The final pass loops through the unique upstream endpoint coordinate identifiers
# and returns an ID -> [(upstream ID, order), (upstream ID, order), ... ] pairs so that
# the recursive loop can decide whether to include these.

def pass1(shapes):
    dct = dict()
    pntMap = dict()
    for rec in shapes.shapeRecords():
    	tgt = upstream(rec)
        sID = shapeID(rec)
	dct[tgt] = [sID]    # target goes to segment shape ID and empty list
        pntMap[sID] = rec.shape.points
    return (dct, pntMap)

# So far no upstream (id, ORDER) pairs have been appended
def pass2(shapes, dct):
    for rec in shapes.shapeRecords():
	src = downstream(rec)
	if src in dct:
	    IDlist = dct[src]
            IDlist.append((shapeID(rec), streamOrder(rec))) 
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
  # now load the 15 second Niger Basin boundary
  driver = ogr.GetDriverByName("ESRI Shapefile")
  # get data source object
  dataSource = driver.Open(Const.SHAPEFILE15s, 0)
  if dataSource is None:
    print 'Could not open ' + Const.SHAPEFILE15s
    sys.exit(1)
  layer = dataSource.GetLayer(0)    # always 0 for ShapeFiles
  feature  = layer.GetFeature(0)    # hope it contains the big polygon
  geometry = feature.GetGeometryRef()
  ring  = geometry.GetGeometryRef(0)   # we want the geometry, not the ring it contains
  points = ring.GetPointCount()
  newring = ogr.Geometry(ogr.wkbLinearRing) # create a new ring -- needed since the
  for p in xrange(points):                  # data source geometry is destroyed
    lon, lat, _ = ring.GetPoint(p)          # once the function exits
    newring.AddPoint(lat, lon)  # note reversal
  newgeom = ogr.Geometry(ogr.wkbPolygon)  # a new geometry must be created
  newgeom.AddGeometry(newring)            # or the code will segfault
  dataSource.Destroy()              # close the data source
  downmap = {}	# invert the map. Note there is only one item downstream
  for down in maps[0]:
    for up in  maps[0][down]:   # up is a list of pairs [(id, strahler),...]
      downmap[up[0]] = down
  # downmap sends  ID to the unique ID downstream
  return (maps[0], maps[1], newgeom, downmap)   
                                    # compatibility with other code

if __name__ == '__main__':
    maps = preprocess(Const.SHAPEFILE)
    mapfile = open(Const.DICTIONARY, "w")  # write dictionaries
    pickle.dump(maps, mapfile)
    mapfile.close()
    exit(0)

