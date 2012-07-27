#!/usr/bin/python
# implement breadth first search with queues
import Queue
import redis
import json
from   preprocess import loadmaps,IDkey

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

# traverse with threshold
def	traverseStrahlerRedis(r, key, order):
        maplist = []
	q = Queue.Queue()
	q.put(key)
	while not q.empty():
		node = q.get()
		seg = json.loads(r.get(IDkey('n', node))) 
		maplist.append( { "id": node, "coords" : seg } )
		upnodes = json.loads(r.get(node))
		for k in upnodes:
		    if k[1] >= order:
			q.put(k[0])
        return { "Upstream" : maplist }




if __name__ == '__main__':
#	t = { 1 : [2, 3], 2 : [4, 5], 3 : [6], 4 : [], 5 : [], 6 : [] }
#	bfs(t, 1)
#       print 'Loading cPickle map'
#	bigmap = loadmaps("NigerShapefiles/NigerRiverDictionary")
        print 'Connecting to redis'
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
        print 'Traversal 1'
        print traverseStrahlerRedis(r, 16340, 5)
#       maps = loadmaps("NigerShapefiles/NigerRiverDict")
#       print traverse(maps, 220)
#	print traverseStrahler(bigmap, 1640, 5)  # this should be the same
