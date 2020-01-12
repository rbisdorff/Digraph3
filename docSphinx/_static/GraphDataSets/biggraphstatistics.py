#!/home/bisi/Python-2.4/python
# graphstatistics.py
# R.B. June 2005
#######################

import sys
import time
sys.setrecursionlimit(10000)

def dbgprint(dbgflag, y):
	if dbgflag != 0:
		print y

# successors Gama(node)
def dneighbors(node, nodeset,relation,valuationdomain):
    nb = set()
    for a in nodeset:
	    if relation[node][a] > valuationdomain['med']:
		    nb.add(a)
    return nb

# predecessors Gamma(node)^-1 
def aneighbors(node, nodeset, relation,valuationdomain):
    nb = set()
    for a in nodeset:
	    if relation[a][node] > valuationdomain['med']:
		    nb.add(a)
    return nb
# initialize singletons
def singletons(actionset,relation,valuationdomain):
	s = []          # list of singletons and neighborhood
	for x in actionset:
		s = s + [(frozenset([x]),gamma[x][0],gamma[x][1])]
	return s

# initialize neighborhoods
def gammasets(actionset,relation,valuationdomain):
	gamma = {}    # dictionary of neighborhoods {node: (dx,ax)}
	for x in actionset:
		dx = dneighbors(x,actionset,relation,valuationdomain)
		ax = aneighbors(x,actionset,relation,valuationdomain)
		dx.add(x)
		ax.add(x)
		gamma[x] = (dx,ax)
	return gamma
#collect compenents
def collectcomps(x, A, actions, relation, valuationdomain, ncomp):
	Comp = set()
	Nx = gamma[x][0] | gamma[x][1]
	for y in Nx:
		if A[y] == 0:
			A[y] = ncomp
			Comp.add(y)
			Comp = Comp | collectcomps(y, A, actions, relation, valuationdomain, ncomp)
	return Comp
# compute independance degree 
def intstab(ker,relation,valuationdomain):
	deg = valuationdomain['min']
	for a in ker:
		for b in ker:
			x = relation[a][b]
			if x > deg and a != b:
				deg = x
	res = valuationdomain['max'] - deg
	return res

#compute absorbancy degree
def absorb(ker,actions,relation,valuationdomain):
	deg = valuationdomain['max']
	restactions = actions - ker
	for a in restactions:
		dega = 0
		for b in ker:
			x = relation[a][b]
			if x > dega:
				dega = x
		if dega < deg:
			deg = dega
	return deg

#compute dominance degree
def domin(ker,actions,relation,valuationdomain):
	deg = valuationdomain['max']
	restactions = actions - ker
	for a in restactions:
		dega = 0
		for b in ker:
			x = relation[b][a]
			if x > dega:
				dega = x
		if dega < deg:
			deg = dega
	return deg


 # component kernels extraction
def compChoices(actions, relation, valuationdomain):
	# globals and constants
	global domChoices    # results
	global domKernels
	global kuplets       # historical record for cutting search space

	med = valuationdomain['med']
	
	print '--------------------------------------'
	print
	print 'connected component : ' + str(actions)
	print
	# initialize kernels extraction history
	domChoices = set()
	domKernels = set()
	kuplets = set()         
	#kisets = singletons(actions,relation,valuationdomain)
	kiset = frozenset()
	kiset = kiset | actions
	t0 = time.clock()
	# recursive minimal dominant choice extraction
	kd_Choices(kiset,actions,relation,valuationdomain)
	# output results
	#print
	#print 'Results'
	#print '-------'
	t1 = time.clock() - t0
	print t1
       	k1 = len(kuplets)
	print k1
	r1 = len(domChoices)
	print r1
	#print domChoices
	fileout = open('runtimesmindom.txt','a')
	fileout.write(str(t1) + ' ' + str(k1) + ' ' + str(r1) + '\n')
	fileout.close

	#for choice in domChoices:
		#print 'minimal dominant choice : ', choice
		#degi = intstab(choice,relation,valuationdomain)
		#dega = absorb(choice,actions,relation,valuationdomain)
		#degd = domin(choice,actions,relation,valuationdomain)
		#print 'independance: ' + str(degi),
		#print '; dominance: ' + str(degd),
		#print '; absorbancy: ' + str(dega),
		#if degi > med:
			#domKernels.add(choice)
			#print '; dominant kernel: ' + str(min(degi,degd)),
		#if dega > med and  degd > med:
			#print '; ambiguous choice !',
		#print
		#print
	#print 'Time needed: ' + str(t1), 
	#print '; History length: ', len(kuplets)
	#print '---- end component ----'
	#print

# k-kernel extraction   --------------------- 

def kd_Choices(choice,actions,relation,valuationdomain):
	global domChoices
	global kuplets
	global gamma
	#print '--->>', choice
	Irred = True
	for x in choice:
		#print 'x', x
		nbhchoicewithoutx = set()
		choicewithoutx = choice - set([x])
		for y in choicewithoutx:
			nbhchoicewithoutx = nbhchoicewithoutx | gamma[y][0]
	                #print 'x', x, 'gamma', gamma[x][0]
	                #print 'nbhchoicewithoutx', nbhchoicewithoutx 
	        pdnbhx = gamma[x][0] - nbhchoicewithoutx
		#pdnbhx = privatedomneighborhood(x,choice)
		#print 'pdnbhx', pdnbhx
		if pdnbhx == set():
			Irred = False
			choice1 = choice - set([x])
			if choice1 not in kuplets:				
				#kuplets.add(choice1)
				kd_Choices(choice1,actions,relation,valuationdomain)
				kuplets.add(choice1)

	if Irred:
		print 'Minimal dominant choice: ', choice
		domChoices.add(choice)

def privatedomneighborhood(x,choice):
	global gamma
	# it is suppoesed verified that x is in choice
	nbhchoicewithoutx = set()
	choicewithoutx = choice - set([x])
	for y in choicewithoutx:
		nbhchoicewithoutx = nbhchoicewithoutx | gamma[y][0]
	#print 'x', x, 'gamma', gamma[x][0]
	#print 'nbhchoicewithoutx', nbhchoicewithoutx 
	pdnbhx = gamma[x][0] - nbhchoicewithoutx
	return pdnbhx


##################################################################
def main():
	
	#-------------------------
	narg = len(sys.argv)
	if narg < 2:
		print 'Usage: mindom.py relation [<dbflag=1>]'
	
	modname = __import__(sys.argv[1])

	dbgflag = 0
	if narg > 2:
		dbgflag = sys.argv[2] 

	if dbgflag != 0:
		print 'Executing in debugging mode!!!'
	#------------------
	global gamma
	global domChoices
	global domKernels
	global kuplets
	
	#------------------
	#print 'Extraction of minimal dominant choices'
	#print 'by reduction of X to minimal dominating sets'
	#print 'R. Bisdorff, April 2005               '
	#print '--------------------------------------'
	actions = set(modname.actionset)
	relation = modname.relation
	valuationdomain = modname.valuationdomain
	# prepare neighborhoods
	gamma = gammasets(actions,relation,valuationdomain)
	#print 'direct neighbors : ', gamma
	# connected components
	A = {}
	for x in actions:
		A[x] = 0
	ncomp = 1
	ConComp = [] 
	for x in A:
		Comp = set()
		if A[x] == 0:
			A[x] = ncomp
			Comp = Comp | set([x])
			Comp = Comp | collectcomps(x, A, actions, relation, valuationdomain, ncomp)
		if len(Comp) > 0:
			ncomp = ncomp + 1
			ConComp = ConComp + [Comp]
#	print 'Connected Components:', len(ConComp)
#	k=1
#	for Comp in ConComp:
#		print str(k) + ': ' + str(Comp)
#		k = k + 1
#	print
#----------------------
        order = len(actions)
	nbrcomp = len(ConComp)
	size = 0
	undeterm = 0
	degoutseq = {}
	deginseq = {}
	for x in actions:
		degoutseq[x] = 0
		deginseq[x] = 0
		for y in actions:
			if x != y:
				if relation[x][y] > valuationdomain['med']:
					size += 1
					degoutseq[x] += 1
				if relation[x][y] == valuationdomain['med']:
					undeterm += 1
				if relation[y][x] > valuationdomain['med']:
					deginseq[x] += 1
	deg = 0
	degseq = []
	for x in actions:
		degx = max(deginseq[x],degoutseq[x])
		degseq.append((degx,x))
		if degx > deg:
			deg = degx
	degseq.sort()
	fillrate = (size * 100.0)/ (order * (order - 1 ))
	undetermrate = (undeterm * 100.0)/ (order * (order - 1 ))
	print '--------------------------------------------------------------'
	print 'Bipolar digraphs'
	print 'General statistics'
	print
	print 'order                 : ', order
	print 'size                  : ', size
	print 'arc density (%)       : ', fillrate
	print 'degree                : ', deg
	print 'degree sequence       : ', degseq
	print 'undetermined          : ', undeterm
	print 'undetermined (%)      : ', undetermrate
	print 'Components            : ', nbrcomp
	print 'Valuation domain      : ', valuationdomain
	print
	print '--------------------------------------------------------------'
	print 'RB August 2005'

#-------------------
	#t0 = time.clock()
	#n0 = len(actions)
	#for Comp in ConComp:
		#n = len(Comp)
		#if n == n0:
			#compChoices(Comp,relation,valuationdomain)
	#t1 = time.clock() - t0
	#print 'Global time needed: ' + str(t1)
# ---------------------------
main()
