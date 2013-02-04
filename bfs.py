#!/usr/bin/python
# implement breadth first search with queues
import Queue
import json
from   preprocess import loadmaps
#from   quickhull import qhull
from   constants import Const
from   numpy import array
from   osgeo import ogr    # GDAL functions for ConvexHull() and Intersection()

# upstream traversal creates a map whose key is 
# "Upstream" and whose values are a list of maps of the form 
#
# { "id": ID, "coords" : [[LAT1,LON1],[LAT2,LON2]] }
#

def	traverse(maps, key):
	tree = maps[0]
        pointmap = maps[1]
        maplist = []
	q = Queue.Queue()
	q.put(key)
	while not q.empty():
		node = q.get()
		seg = pointmap[node]
		maplist.append( { "id": node, 
        # JSON dumps won't work with a list of lists directly!
                  "coords" : [[seg[0][0],seg[0][1]],[seg[1][0],seg[1][1]]] } )
		for k in tree[node]:
			q.put(k)
        return { "Upstream" : maplist }


# traverse with threshold
def	traverseStrahler(maps, key, order):
	tree = maps[0]
        pointmap = maps[1]
        maplist = []
	q = Queue.Queue()
	q.put(key)
	while not q.empty():
		node = q.get()
		seg = pointmap[node]
		maplist.append( { "id": node, 
        # JSON dumps won't work with a list of lists directly!
                  "coords" : [[seg[0][0],seg[0][1]],[seg[1][0],seg[1][1]]] } )
		for k in tree[node]:
		    if k[1] >= order:
			q.put(k[0])
        return { "Upstream" : maplist }

# traverse with threshold and return perimeter of convex hull
def subbasinPerimeter1(maps, key, order):
  """Return perimeter of convex hull of subbasin """
  tree = maps[0]
  pointmap = maps[1]
  q = Queue.Queue()
  q.put(key)
  # create multipoiny geometry
  multipoint = ogr.Geometry(ogr.wkbMultiPoint)
  point = ogr.Geometry(ogr.wkbPoint)
  while not q.empty():
    node = q.get()
    seg = pointmap[node]
    point.AddPoint(seg[0][1], seg[0][0])  # Lon, Lat -- note reversal
    multipoint.AddGeometry(point)
    point.AddPoint(seg[1][1], seg[1][0])  # Lon, Lat -- note reversal
    multipoint.AddGeometry(point)
    for k in tree[node]:
      if k[1] >= order:
        q.put(k[0])
  # now we have the subbasin. Apply ConvexHull and return the polygon
  polygon = multipoint.ConvexHull()
  basin = maps[2]
  print type(basin)
  if polygon.Intersects(basin): 
    bdry = basin.GetGeometryRef(0)
    print basin.GetGeometryName(), bdry.GetGeometryName()
    intersection = basin.Intersection(polygon)
    count = intersection.GetGeometryCount()
    print count
    if count == 1:
      print 'Intersection succeeds'
      polygon = intersection

  ring = polygon.GetGeometryRef(0)
  points = ring.GetPointCount()
  # Convert to list
  subbasin = []
  for p in xrange(points):
    lon, lat,  _ = ring.GetPoint(p)
    subbasin.append([lat, lon])  # note reversal to lat lon!
  return { 'polygon': subbasin }



deg = 0.016666666666666
hdeg = deg/2

# This has a fudge factor to ensure overlap
def	subbasin(maps, key, order):
	tree = maps[0]
        pointmap = maps[1]
        maplist = []
	q = Queue.Queue()
	q.put(key)
	while not q.empty():
	    node = q.get()
	    seg = pointmap[node]
	    lat = seg[0][0]
	    lon = seg[0][1]
	    # json forces this on us
	    maplist.append( {"polygon" : [[lat-hdeg, lon-hdeg], [lat-hdeg, lon+hdeg],
			                  [lat+hdeg, lon+hdeg], [lat+hdeg, lon-hdeg]] } )
	    for k in tree[node]:
	        if k[1] >= order:
		    q.put(k[0])
        return { "multipolygon" : maplist }

def gridPolygon(lon, lat):
  ff = 0.0085
  ring = ogr.Geometry(ogr.wkbLinearRing)
  ring.AddPoint(lon-ff, lat-ff)
  ring.AddPoint(lon+ff, lat-ff)
  ring.AddPoint(lon+ff, lat+ff)
  ring.AddPoint(lon-ff, lat+ff)
  ring.CloseRings() 
  poly = ogr.Geometry(ogr.wkbPolygon)
  poly.AddGeometry(ring)
  return poly
  

# traverse with threshold and return perimeter of littleboxes
def subbasinPerimeter(maps, key, order):
  """Return perimeter of subbasin """
  order = max(order, 3)
  tree = maps[0]
  pointmap = maps[1]
  q = Queue.Queue()
  q.put(key)
  seg = pointmap[key]
  polygon = gridPolygon(seg[0][1], seg[0][0])
  while not q.empty():
    node = q.get()
    seg = pointmap[node]
    polygon = polygon.Union(gridPolygon(seg[0][1], seg[0][0]))
    for k in tree[node]:
      if k[1] >= order:
        q.put(k[0])
  # now we have the subbasin. See if it intersects
#  basin = maps[2]
#  print type(basin)
#  if polygon.Intersects(basin): 
#    bdry = basin.GetGeometryRef(0)
#    print basin.GetGeometryName(), bdry.GetGeometryName()
#    intersection = basin.Intersection(polygon)
#    count = intersection.GetGeometryCount()
#    print count
#    if count == 1:
#      print 'Intersection succeeds'
#      polygon = intersection

  ring = polygon.GetGeometryRef(0)
  points = ring.GetPointCount()
  # Convert to list
  subbasin = []
  for p in xrange(points):
    lon, lat,  _ = ring.GetPoint(p)
    subbasin.append([lat, lon])  # note reversal to lat lon!
  return { 'polygon': subbasin }





if __name__ == '__main__':
        print 'Loading cPickle map'
	bigmap = loadmaps(Const.DICTIONARY)
#	print 'traversal'
#	print traverseStrahler(bigmap, 1640, 5)  # this should be the same
	print 'perimeter'
	print subbasinPerimeter(bigmap, 1727, 1)
#       print 'Connecting to redis'
##	r = redis.StrictRedis(host='localhost', port=6379, db=0)
#       print 'Traversal 1'
#       print traverseStrahlerRedis(r, 220, 7)
#       print traverseStrahlerRedis(r, 1650, 7)
