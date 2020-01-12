#!/usr/bin/python2.4
#
# Random Regular Graph genrator
# Indpendent pairing method (Bollobas)
# RB December 2005
# ------------------------------------
def generateRandomEdge(cell, cells):
	global degreeseq
	x = cell[0]
	edges = []
	copycells = copy.copy(cells)
	#print 'copycells',copycells,copycells[0]
	while degreeseq[x] > 0 and len(copycells) > 0:
		other = random.choice(copycells)
		edges.append((x,other[0]))
		degreeseq[other[0]] -= 1
		degreeseq[x] -= 1
		copycells.remove(other)
	return (edges,cells)
def generateRandomCell(cells):
	cell = random.choice(cells)
	return cell

def main():
	global degreeseq
	#-------------------------
	narg = len(sys.argv)
	if narg < 3:
		print 'Usage: genRandRegGraph.py <order> <degree>'
		return 1
        order = eval(sys.argv[1])
	degree = eval(sys.argv[2])
        print '###################################'
        print '# random regular graph generator  #'
        print '# RB december 2005                #'
        print '###################################'
        print '# Graph order : ', str(order)
	print '# Degree      : ', str(degree)
	# check feasability
	r = (order * degree) % 2
	if degree >= order or r == 1:
		print 'Graph not feasable (1) !!'
		return 1
	# create temporary actionset and relation
	actions = range(order+1)
	actions.remove(0)
	f2 = open('tmp.py','w')
	f2.write('actionset = [\n')
	for x in actions:
		f2.write('\'' + str(x) + '\',\n') 
	f2.write(']\n')
	f2.write('relation = {\n')
	for x in actions:
		f2.write("\'" + str(x) + "\': {\n")	
		for y in actions:
			f2.write("\'" + str(y) + "\':" + str(0.0) + ',\n')
		f2.write('},\n')
	f2.write('}')
	f2.close()
	modname = __import__('tmp')
	actionset = modname.actionset
	relation = modname.relation
	#print actionset
	#print relation
	# create a random pairing
	feasable = 0
	while feasable == 0:
		edges = []
		cells = []
		degreeseq = {}
		for x in actionset:
			degreeseq[x] = degree
			cells.append((x,degree))
		while len(cells) > 1:
		      #cell = random.choice(cells)
		      cell = generateRandomCell(cells)
		      #print 'cell',cell
		      cells.remove(cell)
		      #print 'cells',cells
		      (celledges,cells) = generateRandomEdge(cell,cells)
		      #print 'celledges',celledges
		      edges += celledges
		      #print 'degreeseq', degreeseq
		      #degreeseq[cell[0]] = 0
		      for c in cells:
			      if degreeseq[c[0]] == 0:
				      cells.remove(c)
	        # print edges
	        # check feasability from unsatisfied degrees
		print '# Degree satisfaction : ', degreeseq
		feasable = 1
		for x in actionset:
			if degreeseq[x] != 0:
				feasable = 0
				break
	if feasable == 0:
		print 'Graph not feasable (2) !!'
		return 2

        # insert random edges into relation
	for edge in edges:
		#print edge[0],edge[1]
		relation[edge[0]][edge[1]] = 2.0
		relation[edge[1]][edge[0]] = 2.0

	# final stdout of graph
        print 'actionset = ['
        for x in actionset:
            print '\'' + str(x) + '\',' 
        print ']'
        print 'valuationdomain = {\'min\':0.0, \'med\':1.0, \'max\':2.0}' 
        print 'relation = {'
        for x in actionset:
            print "\'" + str(x) + "\': {"	
            for y in actionset:
		print "\'" + str(y) + "\':" + str(relation[x][y]) + ','
            print '},'
        print '}'
        return 0

#................................................
if __name__=='__main__':
    import sys
    import time
    import random
    import copy
    main()
    
