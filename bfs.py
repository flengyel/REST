#!/usr/bin/python
# implement breadth first search with queues
import Queue
from   niger import loadmaps

def	bfs(tree, key):
	q = Queue.Queue()
	q.put(key)
	while not q.empty():
		node = q.get()
		print node
		for k in tree[node]:
			q.put(k)	

# upstream traversal
def	traverse(maps, key):
	tree = maps[0]
        pointmap = maps[1]
	q = Queue.Queue()
	q.put(key)
	while not q.empty():
		node = q.get()
		print node, pointmap[node]
		for k in tree[node]:
			q.put(k)

if __name__ == '__main__':
#	t = { 1 : [2, 3], 2 : [4, 5], 3 : [6], 4 : [], 5 : [], 6 : [] }
#	bfs(t, 1)
        maps = loadmaps("NigerRiverDict")
        traverse(maps, 220)
