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
def subbasinPerimeter(maps, key, order):
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
  ring = polygon.GetGeometryRef(0)
  points = ring.GetPointCount()
  # Convert to list
  subbasin = []
  for p in xrange(points):
    lon, lat,  _ = ring.GetPoint(p)
    subbasin.append([lat, lon])  # note reversal to lat lon!
  return { 'polygon': subbasin }




# traverse with threshold
#from    preprocess_redis import IDkey
#def	traverseStrahlerRedis(r, key, order):
#        maplist = []
#	q = Queue.Queue()
#	q.put(key)
#	 while not q.empty():
#		node = q.get()
#		seg = r.lrange(IDkey('n', node),0,-1) 
#		maplist.append( { "id": int(node), 
#                             "coords" :  [[float(seg[0]),float(seg[1])],
#                                          [float(seg[2]),float(seg[3])]] } )
#                upnodes = r.lrange(node, 0, -1)
#                ordtoggle = False
#		for item in upnodes:
#                    if ordtoggle:
#                        if int(item) >= order:
#                           q.put(lastnode)
#                    else:
#                        lastnode = item    
#		    ordtoggle = not ordtoggle
#        return { "Upstream" : maplist }




if __name__ == '__main__':
#	t = { 1 : [2, 3], 2 : [4, 5], 3 : [6], 4 : [], 5 : [], 6 : [] }
#	bfs(t, 1)
#       maps = loadmaps("NigerShapefiles/NigerRiverDict")
#       print traverse(maps, 220)
        print 'Loading cPickle map'
	bigmap = loadmaps(Const.DICTIONARY)
	print 'traversal'
	print traverseStrahler(bigmap, 1640, 5)  # this should be the same
	print 'perimeter'
	print subbasinPerimeter(bigmap, 1640, 5)
#       print 'Connecting to redis'
##	r = redis.StrictRedis(host='localhost', port=6379, db=0)
#       print 'Traversal 1'
#       print traverseStrahlerRedis(r, 220, 7)
#       print traverseStrahlerRedis(r, 1650, 7)
