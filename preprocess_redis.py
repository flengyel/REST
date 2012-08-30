#!/usr/bin/python
# preprocess ESRI shape file for 1min resolution niger river network
import shapefile
import cPickle as pickle     # dump and load data structures
import json		     # encode data structures with json strings
import redis                 # so that redis can store them efficiently
from   constants import Const

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

def IDkey(name,ID):
    """create 'name:ID'"""
    return name+str(ID)

def seg2json(rec):
    """Create json string corresponding to rec.shape.points"""
    seg = rec.shape.points
    # json needs this list structure spelled out -- it cannot parse floats in lists  
    # TypeError: [6.074999809265137, 4.391670227050781] is not JSON serializable
    return json.dumps([[seg[0][0], seg[0][1]], [seg[1][0], seg[1][1]]])

# create two dictionaries dct and pntMap
# dct maps an upstream coordinate to  [ID (upstreamID, order), (upstreamID, order),...]
# and the map pntMap, which maps a shape ID to a coordinate pair map
# the intention is that during the search, only coordinates > order will included.
# The final pass loops through the unique upstream endpoint coordinate identifiers
# and returns an ID -> [(upstream ID, order), (upstream ID, order), ... ] pairs so that
# the recursive loop can decide whether to include these.

# given a redis database r and a shapefile structure shapes
# return the dictionary but save the nigermap in redis

def pass1(r, shapes):
    dct = dict()
    print 'Pass 1: create redis map ID -> [[ux,uy],[dx,dy]]'
    for rec in shapes.shapeRecords():
    	tgt = upstream(rec)
        sID = shapeID(rec)
	dct[tgt] = [sID]    # target goes to segment shape ID and empty list
        r.set(IDkey('n',sID), seg2json(rec))
    return dct

def pushCoords(r, aKey, aRec):
    seg = aRec.shape.points
    r.rpush(aKey, seg[0][0]) 
    r.rpush(aKey, seg[0][1]) 
    r.rpush(aKey, seg[1][0]) 
    r.rpush(aKey, seg[1][1]) 


def pass1a(r, shapes):
    dct = dict()
    print 'Pass 1: create redis map ID -> [[ux,uy],[dx,dy]]'
    for rec in shapes.shapeRecords():
    	tgt = upstream(rec)
        sID = shapeID(rec)
	dct[tgt] = [sID]    # target goes to segment shape ID and empty list
        pushCoords(r, IDkey('n',sID), rec)
    return dct

# So far no upstream (id, ORDER) pairs have been appended
def pass2(shapes, dct):
    """Pass 2: create dictionary ID -> [[id, strahler],...]"""
    print "Pass 2: create dictionary ID -> [[id, strahler],...]"
    for rec in shapes.shapeRecords():
	src = downstream(rec)
	if src in dct:
	    IDlist = dct[src]
            IDlist.append((shapeID(rec), streamOrder(rec))) 
	    dct[src] = IDlist 
    return dct	 
	
# So far no upstream (id, ORDER) pairs have been appended
def pass2a(shapes, dct):
    """Pass 2a: create dictionary ID -> [id, strahler,...]"""
    print "Pass 2: create dictionary ID -> [[id, strahler],...]"
    for rec in shapes.shapeRecords():
	src = downstream(rec)
	if src in dct:
	    IDlist = dct[src]
            IDlist.append(shapeID(rec)) 
            IDlist.append(streamOrder(rec)) 
	    dct[src] = IDlist 
    return dct	 
	
def pass3(r, dct):
    """Map ID -> upstream id, stream order pairs in redis"""
    print 'Pass 3: Convert dictionary to redis map niger:ID -> [[id, strahler order],...]'
    for item in dct:
      IDlist = dct[item]
      r.set(IDlist[0], json.dumps(IDlist[1:]))

def pass3a(r, dct):
    """Map ID -> upstream id, stream order pairs in redis"""
    print 'Pass 3: Convert dictionary to redis map niger:ID -> [[id, strahler order],...]'
    for item in dct:
      IDlist = dct[item]
      IDstr = str(IDlist[0])
      for item in IDlist[1:]:
         r.rpush(IDstr, item)


def preprocess(shapefilename):
    """Load redis client, read shapefile and create redis dictionary mappings"""
    print 'Starting redis client'
    # one possibility is to use two databases, one for segments and one for the tree
    r = redis.StrictRedis(host='localhost',port=6379,db=0)
    print 'Reading shapefile'
    sh = shapefile.Reader(Const.SHAPEFILE)
    pass3(r, pass2(sh, pass1(r, sh)))

def preprocessA(shapefilename):
    """Load redis client, read shapefile and create redis dictionary mappings"""
    print 'Starting redis client'
    # one possibility is to use two databases, one for segments and one for the tree
    r = redis.StrictRedis(host='localhost',port=6379,db=0)
    r.flushdb()
    print 'Reading shapefile'
    sh = shapefile.Reader(Const.SHAPEFILE)
    pass3a(r, pass2a(sh, pass1a(r, sh)))


if __name__ == '__main__':
#    preprocess("Niger_River_Active_1min.shp")
    preprocessA(Const.SHAPEFILE)
    exit(0)

