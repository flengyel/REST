#!/usr/bin/python
# implement breadth first search with queues
from __future__ import division
import Queue
from   idmap import IDmap
from   preprocess import loadmaps
import redis # a waste, this should not be needed



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

NOVALUE=-9999  # a magic number. Consolodate these.

def	_histo1(maps, myIDmap, key, order, myField, bins):
	tree=maps[0]
	nodelist=[]
	q = Queue.Queue()
	q.put(key)
	mini=myIDmap.field(key, myField)  # should be an integer field or else
	maxi=mini   # set min = max.
	count = 0
	while not q.empty():
		count += 1
		node  = q.get()
		value = myIDmap.field(node,myField)
		mini  = min(mini,value)
		maxi  = max(maxi,value)
		nodelist.append((node,value))	# append node ID and the value for next pass
		for k in tree[node]:
			if k[1] >= order:
				q.put(k[0])
	width = (maxi-mini)/bins
	# correct if the min and max values are equal
	if width <= 0:
		width=1
		bins=1
	return ( count, width, bins, mini, maxi, nodelist )		

# borrowed from stackoverflow, where it was named batch_gen
# http://stackoverflow.com/questions/760753/iterate-over-a-python-sequence-in-multiples-of-n
# Yield is not without overhead. Better to append (node,value) pairs directly
# in nodelist than incur the overhead.

def iterate_by_n(data, n):
    for i in range(0, len(data), n):
            yield data[i:i+n]

def	_histo2(arglist):
	count, width, bins, mini, maxi, nodelist = arglist
	frequencies = [0]*bins
	endpoints   = [mini]*(bins+1)

        IDValueBinMap = []
	for i in range(bins):
	    j = i+1
	    endpoints[j] = endpoints[j]+j*width
	
	for pair in nodelist:
	    ID = pair[0]
	    value = pair[1]
	    index = int((value-mini)/width)
	    if index >= bins:
		index = bins-1  # index correction -- this happens at the last interval
	    frequencies[index] += 1
	    IDValueBinMap.append((ID, value, index))    
	return (frequencies, endpoints, IDValueBinMap)

def	histogram(maps, myIDmap, key, order, myField, bins):
	return _histo2(_histo1(maps, myIDmap, key, order, myField, bins))

if __name__ == '__main__':
#	t = { 1 : [2, 3], 2 : [4, 5], 3 : [6], 4 : [], 5 : [], 6 : [] }
#	bfs(t, 1)
        print 'Loading cPickle map'
	maps = loadmaps("NigerShapefiles/NigerRiverDictionary")
	print 'cPickle map loaded'
        print traverseStrahler(maps, 7549, 5)
	myfields = ['ID', 'q_dist_1m_annual' , 'q_dist25_1m_annual', 'q_dist50_1m_annual',      
                'CropLandAreaAcc','Pop2000','PopAcc2000','Runoff-01','Runoff-02','Runoff-03',
                'Runoff-04','Runoff-05','Runoff-06','Runoff-07','Runoff-08','Runoff-09',
                'Runoff-10','Runoff-11','Runoff-12','Runoff25-01','Runoff25-02','Runoff25-03',
                'Runoff25-04','Runoff25-05','Runoff25-06','Runoff25-07','Runoff25-08',  
                'Runoff25-09','Runoff25-10','Runoff25-11','Runoff25-12','Runoff50-01',
                'Runoff50-02','Runoff50-03','Runoff50-04','Runoff50-05','Runoff50-06',
                'Runoff50-07','Runoff50-08','Runoff50-09','Runoff50-10','Runoff50-11',
                'Runoff50-12','Discharge-01','Discharge-02','Discharge-03','Discharge-04',
                'Discharge-05','Discharge-06','Discharge-07','Discharge-08','Discharge-09',
                'Discharge-10','Discharge-11','Discharge-12','Discharge25-01','Discharge25-02',
                'Discharge25-03','Discharge25-04','Discharge25-05','Discharge25-06',
                'Discharge25-07','Discharge25-08','Discharge25-09','Discharge25-10',
                'Discharge25-11','Discharge25-12','Discharge50-01','Discharge50-02',
                'Discharge50-03','Discharge50-04','Discharge50-05','Discharge50-06',    
                'Discharge50-07','Discharge50-08','Discharge50-09','Discharge50-10',    
                'Discharge50-11','Discharge50-12']
	print 'loading IDmap'
	myIDmap = IDmap('NigerShapefiles/NigerRiverActive1m.txt',myfields)
	print 'testing 1st pass of histogram'
	arglist =  _histo1(maps,myIDmap, 7549, 5, 'CropLandAreaAcc',3) 
	print arglist
	print 'testing 2nd pass of histogram'
	print _histo2(arglist)
