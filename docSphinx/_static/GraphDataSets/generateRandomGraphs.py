#!/usr/bin/python
#   generating random graphs
#   R. Bisdorff   December 2004
#-------------------------------------------------------------------------
import sys
import random
#---------------------debugger print function ------------------
def dbgprint(dgbflag, y):
	if dbgflag != 0:
		print y
#---------------------------------------------------
narg = len(sys.argv)
if narg < 3:
	print 'Usage: {python | [./]}circulargraph.py <Order> [<dbflag=1>]'
	print '       <Order> ::= n , number of vertices'
	print '       <Fill rate> := f, integer percentage'
	

dbgflag = 0
if narg > 3:
	dbgflag = sys.argv[3] 

if dbgflag != 0:
	print 'Executing in debugging mode!!!'

# ---------  procedures -----------------------------
dbgprint (dbgflag, 'order =' + sys.argv[1])
n = eval(sys.argv[1])
f = eval(sys.argv[2])
# start output of the GNU-Prolog source
print '# automatically generated with generateRandomGraphs.py -------'


# generate actionset
actionset = range(n+1)
actionset.remove(0)
print 'actionset = ['
for x in actionset:
	print '\'' + str(x) + '\',' 
print ']'

# relations are evaluated in L100: {0,50,100}

print 'valuationdomain = {\'min\':0, \'med\':50, \'max\':100}' 

# output all outranking relation predicates
random.seed()
print 'relation = {'
for x in actionset:
	print "\'" + str(x) + "\': {"	
	for y in actionset:
		if x == y:
			print "\'" + str(y) + "\':" + str(0) + ','
		else:
			maxv = (round(50.0 / (1 - (f/100.0))))
			v = min(random.randint(0,maxv),100)
			print "\'" + str(y) + "\':" + str(v) + ','
	print '},'
print '}'
