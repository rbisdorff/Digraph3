#!/usr/bin/python2.4
# MaxIrredDomChoices
# R.B. June 2005
#######################

import sys
import time

def dbgprint(dbgflag, y):
	if dbgflag != 0:
		print y

# powerset generator
def powerset(U):
      """Generates all subsets of a set or sequence U."""
      U = iter(U)
      try:
          x = frozenset([U.next()])
          for S in powerset(U):
              yield S
              yield S | x
      except StopIteration:
          yield frozenset()


# successors Gama(node)
def dneighbors(node, nodeset,relation,valuationdomain):
    nb = set()
    for a in nodeset:
	    if relation[node][a] > valuationdomain['med']:
		    nb.add(a)
    return nb
# not successors Gama(node)
def notdneighbors(node, nodeset,relation,valuationdomain):
    nb = set()
    for a in nodeset:
	    if relation[node][a] < valuationdomain['med']:
		    nb.add(a)
    return nb

# predecessors Gamma(node)^-1 
def aneighbors(node, nodeset, relation,valuationdomain):
    nb = set()
    for a in nodeset:
	    if relation[a][node] > valuationdomain['med']:
		    nb.add(a)
    return nb

# not predecessors Gamma(node)^-1 
def notaneighbors(node, nodeset, relation,valuationdomain):
    nb = set()
    for a in nodeset:
	    if relation[a][node] < valuationdomain['med']:
		    nb.add(a)
    return nb

# initialize singletons
def singletons(actionset,relation,valuationdomain):
	global gamma
	s = []       # list of singletons and neighborhood
	for x in actionset:
		indep = notgamma[x][0] & notgamma[x][1]
		s = s + [(frozenset([x]),gamma[x][0],gamma[x][1],indep)]
	return s

# initialize neighborhoods
def gammasets(actionset,relation,valuationdomain):
	gamma = {}    # dictionary of neighborhoods {node: (dx,ax)}
	for x in actionset:
		dx = dneighbors(x,actionset,relation,valuationdomain)
		ax = aneighbors(x,actionset,relation,valuationdomain)
		#dx.add(x)
		#ax.add(x)
		gamma[x] = (dx,ax)
	return gamma
# initialize notneighborhoods
def notgammasets(actionset,relation,valuationdomain):
	notgamma = {}    # dictionary of neighborhoods {node: (dx,ax)}
	for x in actionset:
		dx = notdneighbors(x,actionset,relation,valuationdomain)
		ax = notaneighbors(x,actionset,relation,valuationdomain)
		#dx.add(x)
		#ax.add(x)
		notgamma[x] = (dx,ax)
	return notgamma

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
	#global gamma
	#global notgamma
	global domKernels    # results
	global absKernels
	global kuplets       # historical record for cutting search space

	med = valuationdomain['med']
	
	print '--------------------------------------'
	print
	print 'connected component : ' + str(actions)
	print
	# initialize kernels extraction history
	domKernels = set()
	absKernels = set()
	nbsol = 0
	#kuplets = set()
	t0 = time.time()
	print '------------------------'
	print '   Kernel extraction    '
	kisets = singletons(actions,relation,valuationdomain)
	for choice in independentChoices1(kisets,actions,relation,valuationdomain):
		restactions = actions - choice[0][0]
	       	if restactions <= choice[0][1]:
			domKernels.add(choice[0][0])
			print 'dominant -->>', choice[0][0]
				
	       	if restactions <= choice[0][2]:
	       		absKernels.add(choice[0][0])
	       		print 'absorbent -->>', choice[0][0]
	       	nbsol += 1
	t1 = time.time() -t0
	print '    Statistics    '
	t1 = time.time() - t0
	sys.stderr.write('Time     : '+str(t1)+'\n')
	sys.stderr.write('History  : '+str(nbsol)+'\n')
	r1 = len(domKernels) + len(absKernels)
	sys.stderr.write('Solutions: '+str(r1)+'\n')
	# ---- statistics
	#fileout = open('runtimesallkernels.txt','a')
	#fileout.write(str(t1) + ' ' + str(k1) + ' ' + str(r1) + '\n')
	#fileout.close

        domChoices = domKernels | absKernels
	print '------------------'
	print '  Global results  '
	maxalphaGraph = 0
	minalphaGraph = len(actions)
	for choice in domChoices:
		alphaChoice = len(choice)
		if alphaChoice < minalphaGraph:
			minalphaGraph = alphaChoice
		if alphaChoice > maxalphaGraph:
			maxalphaGraph = alphaChoice
		degi = intstab(choice,relation,valuationdomain)
		if degi > med:
			dega = absorb(choice,actions,relation,valuationdomain)
			degd = domin(choice,actions,relation,valuationdomain)
			print '== >> ', choice
			print 'independance: ' + str(degi),
			print '; dominance: ' + str(degd),
			print '; absorbancy: ' + str(dega)
			if degd > dega:
				print 'dominant kernel  : ' + str(min(degi,degd)),
			if dega > degd:
				print 'absorbent kernel : ' + str(min(degi,dega)),
			print
	print
	print 'Time needed: ' + str(t1), 
	print '; History length      : ', nbsol,
	print '; Solutions           : '+str(r1)
	print '; Max independence number : '+str(maxalphaGraph)
	print '; Min independence number : '+str(minalphaGraph)
	print '---- end component ----'
	print

# k-kernel extraction   --------------------- 

def kd_Choices(choice,actions,relation,valuationdomain):
	global domKernels
	global absKernels
	global kuplets
	global gamma
	global notgamma
        #print 'choice', choice
        restactions = actions - choice[0]
	#print 'restactions', restactions
	uncoverdom = restactions - choice[1]
	uncoverabs = restactions - choice[2]
	if uncoverdom == set():
		print 'Minimal dominant choice: ', choice[0]
		domKernels.add(choice[0])
	if uncoverabs == set():
		print 'Minimal absorbent choice: ', choice[0]
		absKernels.add(choice[0])
	#print 'uncover', indep
	for x in choice[3]:
		choice1set = choice[0] | set([x])
		#print 'choice1set', choice1set
		if choice1set not in kuplets:
			ch1gamdom = choice[1] | gamma[x][0]
			ch1gamabs = choice[2] | gamma[x][1]
			ch1indep = choice[3] & notgamma[x][0] & notgamma[x][1]
			choice1 = (choice1set,ch1gamdom,ch1gamabs,ch1indep)
			#print 'choice1', choice1
			kuplets.add(choice1set)
			kd_Choices(choice1,actions,relation,valuationdomain)


def privatedomneighborhood(x,choice):
	# it is suppoesed verified that x is in choice
	nbhchoicewithoutx = set()
	choicewithoutx = choice - set([x])
	for y in choicewithoutx:
		nbhchoicewithoutx = nbhchoicewithoutx | gamma[y][0]
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
	global notgamma
	global domKernels
	global absKernels
	global kuplets
	
	#------------------
	print 'Extraction of minimal dominant choices'
	print 'by reduction of X to minimal dominating sets'
	print 'R. Bisdorff, April 2005               '
	print '--------------------------------------'
	actions = set(modname.actionset)
	relation = modname.relation
	valuationdomain = modname.valuationdomain
	# prepare neighborhoods
	gamma = gammasets(actions,relation,valuationdomain)
	notgamma = notgammasets(actions,relation,valuationdomain)
	print 'direct neighbors : ', gamma
	print 'not direct neighbors : ', notgamma
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
	print 'Connected Components:'
	k=1
	for Comp in ConComp:
		print str(k) + ': ' + str(Comp)
		k = k + 1
	print
#-------------------
	#n0 = len(actions)
	for Comp in ConComp:
		n = len(Comp)
		#if n == n0:
		compChoices(Comp,relation,valuationdomain)
	print
	print ' Global statistics '
	print '-------------------'
	print
	print ' Components    : ',len(ConComp)
	StrBc = domKernels - absKernels
	print ' Strict best choices  : ' + str(len(StrBc))
	print ' Best choices  : ' + str(len(domKernels))
	StrWc = absKernels - domKernels
	print ' Strict worst choices  : ' + str(len(StrWc))
	print ' Worst choices : ' + str(len(absKernels))
	StrNc = domKernels & absKernels
	print ' Null choices : ' + str(len(StrNc))
	print '--- end of components ----'
	print '******************'
	print '* allkernels.py  *'
	print '* R.B. June 2005 *'
	print '******************'

#-----------------------
def testmain():
	
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
	global notgamma
	global domKernels
	global absKernels
	global kuplets
	
	#------------------
	print 'Extraction of minimal dominant choices'
	print 'by reduction of X to minimal dominating sets'
	print 'R. Bisdorff, April 2005               '
	print '--------------------------------------'
	actions = set(modname.actionset)
	relation = modname.relation
	valuationdomain = modname.valuationdomain
	# prepare neighborhoods
	gamma = gammasets(actions,relation,valuationdomain)
	notgamma = notgammasets(actions,relation,valuationdomain)
	print 'direct neighbors : ', gamma
	print 'not direct neighbors : ', notgamma
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
	print 'Connected Components:'
	k=1
	for Comp in ConComp:
		print str(k) + ': ' + str(Comp)
		k = k + 1
	print
#-------------------
	#n0 = len(actions)
	for Comp in ConComp:
		n = len(Comp)
		#if n == n0:
		#compChoices(Comp,relation,valuationdomain)
		t0 = time.time()
		i = 0
		for choice in indpowerset(Comp,relation,valuationdomain):
			degd = domin(choice,actions,relation,valuationdomain)
			if degd > valuationdomain['med']:
				print choice
			i += 1
		t1 = time.time() - t0
		print i, t1
	print
	print '--- end of components ----'
	print '******************'
	print '* allkernels.py  *'
	print '* R.B. June 2005 *'
	print '******************'
# ---------------------------
def testmain1():
	
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
	global notgamma
	global domKernels
	global absKernels
	global kuplets
	
	#------------------
	print 'Extraction of minimal dominant choices'
	print 'by reduction of X to minimal dominating sets'
	print 'R. Bisdorff, April 2005               '
	print '--------------------------------------'
	actions = set(modname.actionset)
	relation = modname.relation
	valuationdomain = modname.valuationdomain
	# prepare neighborhoods
	gamma = gammasets(actions,relation,valuationdomain)
	notgamma = notgammasets(actions,relation,valuationdomain)
	print 'direct neighbors : ', gamma
	print 'not direct neighbors : ', notgamma
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
	print 'Connected Components:'
	k=1
	for Comp in ConComp:
		print str(k) + ': ' + str(Comp)
		k = k + 1
	print
#-------------------
	#n0 = len(actions)
	for Comp in ConComp:
		n = len(Comp)
		#if n == n0:
		#compChoices(Comp,relation,valuationdomain)
		t0 = time.time()
		i = 0
		kisets = singletons(Comp,relation,valuationdomain)
		for choice in independentChoices1(kisets,Comp,relation,valuationdomain):
			#degd = domin(choice[0],actions,relation,valuationdomain)
			#if degd > valuationdomain['med']:
			
			#print 'independent -->>', choice
			restactions = Comp - choice[0][0]
			if restactions <= choice[0][1]:
				print 'dominant -->>', choice[0][0]
			if restactions <= choice[0][2]:
				print 'absorbent -->>', choice[0][0]
			i += 1
		t1 = time.time() - t0
		print i, t1
	print
	print '--- end of components ----'
	print '******************'
	print '* allkernels.py  *'
	print '* R.B. June 2005 *'
	print '******************'
# ---------------------------
# independent powerset generator
def indpowerset(U,relation,valuationdomain):
      """Generates all independent subsets of a bipolar valued digraph."""
      U = iter(U)
      try:
          x = frozenset([U.next()])
	  #print x
          for S in indpowerset(U,relation,valuationdomain):
		  #degiS = intstab(S,relation,valuationdomain)
		  #if degiS > valuationdomain['med']:
		  yield S
		  print 'S', S
		  Sx = S | x
		  degiSx = intstab(Sx,relation,valuationdomain)
		  if degiSx > valuationdomain['med']:		  
			  yield Sx
			  print 'Sx', Sx
      except StopIteration:
          yield frozenset()
#-------------------------------
# independent powerset generator
def independentChoices(U,actions,relation,valuationdomain):
      """Generates all independent subsets of a bipolar valued digraph."""
      U = iter(U)
      #print U
      try:
          x = list([U.next()])
	  print 'x', x
          for S in independentChoices(U,actions,relation,valuationdomain):
		  #degiS = intstab(S,relation,valuationdomain)
		  #if degiS > valuationdomain['med']:
		  yield S
		  #print 'S', S
		  #print 'x', x
		  #Sindep = S[0][3] & S[0][4]
		  #print 'test', x[0][0], Sindep		  
		  #print 'Sxchoice', Sxchoice
		  #if len(Sxchoice) == 1 or x[0][0] <=  Sindep:
		  if x[0][0] <=  S[0][3]:
			  Sxgamdom = S[0][1] | x[0][1]
		          #print 'Sxgamdom',Sxgamdom
			  Sxgamabs = S[0][2] | x[0][2]
		          #print 'Sxgamabs',Sxgamabs
			  Sxindep = S[0][3] &  x[0][3]
			  #print 'Sxindep ',Sxindep
			  Sxchoice = S[0][0] | x[0][0]
			  Sx = [(Sxchoice,Sxgamdom,Sxgamabs,Sxindep)]
			  #print 'Sx', Sx
			  yield Sx
      except StopIteration:
          yield [(frozenset(),set(),set(),actions)]
#--------------------------------------------------
# independent powerset generator
def independentChoices1(U,actions,relation,valuationdomain):
      """Generates all independent subsets of a bipolar valued digraph."""
      if U == []:
	      yield [(frozenset(),set(),set(),actions)]
      else:
          x = list(U.pop())
	  #print 'x', x[0]
          for S in independentChoices1(U,actions,relation,valuationdomain):
		  #degiS = intstab(S,relation,valuationdomain)
		  #if degiS > valuationdomain['med']:
		  yield S
		  #print 'S', S
		  #print 'x', x
		  #Sindep = S[0][3] & S[0][4]
		  #print 'test', x[0][0], Sindep		  
		  #print 'Sxchoice', Sxchoice
		  #if len(Sxchoice) == 1 or x[0] <=  Sindep:
		  if x[0] <=  S[0][3]:
			  Sxgamdom = S[0][1] | x[1]
		          #print 'Sxgamdom',Sxgamdom
			  Sxgamabs = S[0][2] | x[2]
		          #print 'Sxgamabs',Sxgamabs
			  Sxindep = S[0][3] &  x[3]
			  #print 'Sxindep ',Sxindep
			  Sxchoice = S[0][0] | x[0]
			  Sx = [(Sxchoice,Sxgamdom,Sxgamabs,Sxindep)]
			  #print 'Sx', Sx
			  yield Sx
#-----------------------
main()
