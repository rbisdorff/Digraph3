#!/usr/bin/python
#   Computing standard Electre IS outranking index
#   R. Bisdorff   January 2008
#-------------------------------------------------------------------------

#  ------------- data input model -------------------------
#Example Python Data File
#criteria = ['g1', 'g2', 'g3', 'g4', 'g5']
#
#threshold = {
#    'g1': { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(2.0,0.0)},
#    'g2': { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(2.0,0.0)},
#    'g3': { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(2.0,0.0)},
#    'g4': { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(2.0,0.0)},
#    'g5': { 'ind':(0.0, 0.0),'pref':(1.0,0.0), 'veto':(2.0,0.0)},
#}
#
#actionset = [ 'a1', 'a2', 'a3', 'a4', 'a5', 'a6']
#
#weightorder = [[ 'g1', 'g2', 'g3', 'g4', 'g5']]
#
#weightset = {'g1':1.0, 'g2':1.0, 'g3':1.0, 'g4':1.0, 'g5':1.0}
#
#evaluation = {
#'g1': 
#{'a1': 3, 'a2': 2, 'a3': 1, 'a4': 3, 'a5': 1, 'a6': 1}, 
#'g2': 
#{'a1': 1, 'a2': 3, 'a3': 2, 'a4': 1, 'a5': 3, 'a6': 1}, 
#'g3': 
#{'a1': 2, 'a2': 1, 'a3': 3, 'a4': 1, 'a5': 1, 'a6': 3}, 
#'g3': 
#{'a1': -2, 'a2': -3, 'a3': -1, 'a4': -3, 'a5': -3, 'a6': -1}, 
#'g4': 
#{'a1': 2, 'a2': 2, 'a3': 2, 'a4': 2, 'a5': 2, 'a6': 2}, 
#'g5': 
#{'a1': 1, 'a2': 1, 'a3': 1, 'a4': 1, 'a5': 1, 'a6': 1}, 
#
#}
#

# ---------  procedures -----------------------------

# ---- debugger print function 
def dbgprint(dgbflag, y):
	#global dbgflag
	if dbgflag != 0:
		print y
# ---- local dominance test
def localdominance(d, h, q):
	if d < -q:
		return 0
	else:
		if d < -h:
			return (q + d)/(q - h)
		else:
			return 1
# ---- local veto detection d <= -v
def localveto(d, v):
	if  d > -v:
		return 0.0
	else:
		return 1.0

# -------------------------------
def main():
	global dbgflag
	print '##########################################'
	print '# generating outranking graphs from a    #'
	print '# a given performance tableau            #'
	print '# standard concordance and non veto      #'
	print '# R. Bisdorff January 2006               #'
	print '##########################################'
	narg = len(sys.argv)
	if narg < 2:
		print 'Usage: python normConcordance.py <datafile> [<dbflag=1>]'
		return 1
	
	modname = __import__(sys.argv[1])

	dbgflag = 0
	if narg > 2:
		dbgflag = sys.argv[2] 

	if dbgflag != 0:
		print 'Executing in debugging mode!!!'

	# start output of the Python outranking graph
	print '# standard outranking graph from ', modname
	print 'actionset = ['
	for x in modname.actionset:
		print '\'' + str(x) + '\',' 
	print ']'

	# relations are evaluated in percents: L = {0-100}
	print 'valuationdomain = {\'min\':0.0, \'med\':50.0, \'max\':100.0}' 

	# total of criteria weights
	totalweight = 0
	for c in modname.criteria:
		totalweight = totalweight + modname.weightset[c]
		
	dbgprint(dbgflag, 'totalweight ' + str(totalweight))

	# output all outranking relation predicates
	print 'relation = {'

	for a in modname.actionset:
		print "\'" + str(a) + "\': {"	
		for b in modname.actionset:
			nc = len(modname.criteria)
			dbgprint(dbgflag, 'nc ' + str(nc))
			counter = 0.0
			veto = 0
			for c in modname.criteria:
				dbgprint(dbgflag, 'criteria: ' + str(c))
				if modname.evaluation[c][a] != 999 and modname.evaluation[c][b] != 999:		
					ax = modname.threshold[c]['ind'][0]
					ay = modname.threshold[c]['ind'][1]
					bx = modname.threshold[c]['pref'][0]
					by = modname.threshold[c]['pref'][1]
					vx = modname.threshold[c]['veto'][0]
					vy = modname.threshold[c]['veto'][1]
					h = ax +ay * modname.evaluation[c][a]
					q = bx + by * modname.evaluation[c][a]
					v = vx + vy * modname.evaluation[c][a]
					dbgprint(dbgflag, 'indifference threshold: ' + str(h))
					dbgprint(dbgflag, 'preference threshold: ' + str(q))
					dbgprint(dbgflag, 'veto threshold: ' + str(v))
					d = modname.evaluation[c][a] - modname.evaluation[c][b]
					dbgprint(dbgflag, 'diff: ' + str(d))
					lc0 = localdominance(d,h,q)
					dbgprint(dbgflag, 'localdominance: ' + str(lc0))
					counter = counter + (lc0 * modname.weightset[c])
					dbgprint(dbgflag, 'counter: ' + str(counter))
					veto = veto + localveto(d,v)
					dbgprint(dbgflag, 'veto: ' + str(veto))				
				else:
					counter = counter + 0.5 * modname.weightset[c]
			dbgprint(dbgflag, 'concord: ' + str(counter))
			concordindex = int(round((counter / totalweight) * 100))
			dbgprint(dbgflag, concordindex)
			discordindex = 0
			if veto == 0:
				print "\'" + str(b) + "\':" + str(concordindex) + ','
			else:
				print "\'" + str(b) + "\':" + str(discordindex) + ','
		

		print '},'
	print '}'
	return 0			
#................................................
if __name__=='__main__':
    import sys
    main()

