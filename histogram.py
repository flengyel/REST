#!/usr/bin/python
# implement breadth first search with queues
from __future__ import division
import Queue
from   idmap import IDmap
from   preprocess import loadmaps
from   constants import Const
#import redis # a waste, this should not be needed



# traverse with threshold (here for reference .. not needed)
def	_traverseStrahler(maps, key, order):
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


def	_histo1(maps, myIDmap, key, order, myField, bins):
	tree=maps[0]
	nodelist=[]
	q = Queue.Queue()
	q.put(key)
	mini=myIDmap.field(key, myField)  # should be an integer field or else
	maxi=mini   # set min = max.
	count = 0
	while not q.empty():
	    node  = q.get()
	    value = myIDmap.field(node,myField)
            if value != Const.NOVALUE:
		count += 1
		mini  = min(mini,value)
		maxi  = max(maxi,value)
		nodelist.append((node,value))	# append node ID and the value for next pass
	    for k in tree[node]:		# you may want to traverse upstream in any case - debatable
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
	print count, width, bins, mini, maxi

	frequencies = [0]*bins
	endpoints   = [mini]*(bins+1)

        IDValBinList = []
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
	    IDValBinList.append((ID, value, index))    
	return (count, frequencies, endpoints, IDValBinList)

def	histogram(maps, myIDmap, key, order, myField, bins):
	"""Returns count, freq array, bin endpints, (ID, Value, Bin) list"""
	return _histo2(_histo1(maps, myIDmap, key, order, myField, bins))

if __name__ == '__main__':
#	t = { 1 : [2, 3], 2 : [4, 5], 3 : [6], 4 : [], 5 : [], 6 : [] }
#	bfs(t, 1)
        print 'Loading cPickle map'
	maps = loadmaps(Const.DICTIONARY)
	print 'cPickle map loaded'
        print _traverseStrahler(maps, 7549, 5)
	print 'loading IDmap'
	myIDmap = IDmap(Const.DATABASE, Const.FIELDS)
#	print 'testing 1st pass of histogram'
#	arglist =  _histo1(maps,myIDmap, 7549, 5, 'GRUMP_Pop_2000',5) 
#	print arglist
#	print 'testing 2nd pass of histogram'
#	count, frequencies, endpoints, _ = _histo2(arglist)
#	print _histo2(arglist)
	import numpy
	import pylab as p
#	count, frequencies, endpoints, _ = histogram(maps, myIDmap, 202, 3, 'GRUMP_Pop_2000', 50)
# bad field produces error case of 0 1 1 -9999.0 -9999.0
#	count, frequencies, endpoints, _ = histogram(maps, myIDmap, 202, 3, 'runoff_10', 50)
	count,frequencies, endpoints, _ = histogram(maps, myIDmap, 202, 3, 'Runoff-10', 25)
	ends = numpy.array(endpoints)
	freqs = numpy.array(frequencies)
        x = .5*(ends[1:]+ends[:-1])
        y = freqs/count

	# basic uninteresting plot
	#pylab.plot(x,y)
	#pylab.show()

	print 'Runoff Oct 2000 at ID 220'
	print 'count:', count
	print 'frequencies:',frequencies
	print 'bin endpoints:', endpoints
	print 'derived output:'
	print 'bin midpoints:', x
	print 'proportions within each bin:', y

	# plot barchart with a red line
	p.plot(x, y, 'r', linewidth=1)
	p.bar(x,y,align='center', width=5) 
	p.title('Histogram of runoff')
	p.xlabel('Runoff')
	p.ylabel('Probability') 
	p.show()
