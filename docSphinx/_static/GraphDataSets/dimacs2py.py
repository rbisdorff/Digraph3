#!/usr/bin/python2.4
#
# Graph format converter from DIMACS to RB python format
# RB December 2005
# ------------------------------------

def main():
	
	#-------------------------
	narg = len(sys.argv)
	if narg < 2:
		print 'Usage: dimacs2py.py dimacsFile'

        File = sys.argv[1]
        print '###################################'
        print '# dimacs2py graph format converter#'
        print '# RB december 2005                #'
        print '###################################'
        print '# Converting input file: ' + File
        try:
            f1 = open(File,'r')
        except:
            print 'The input file: ', File,' could not be found!'
            return 1
        nl = 0
        while 1:
            t = f1.readline()
            nl += 1
            if t == '':
                break
            if t[:1] == 'c':
                print '# ', t,
            if t[:1] == 'p':
                order = eval(t.split(' ')[2])
                print '# order = ', order
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
                        f2.write("\'" + str(y) + "\':" + str(2.0) + ',\n')
                    f2.write('},\n')
                f2.write('}')
                f2.close()
                modname = __import__('tmp')
            if t[:1] == 'e':
                edge = t.split(' ')
                xa = edge[1]
                xb = edge[2].strip()
                modname.relation[xa][xb] = 0.0         
                modname.relation[xb][xa] = 0.0         
        f1.close()
        print modname.relation
        print ' # number of lines read: ' + str(nl)
        print 'actionset = ['
        for x in modname.actionset:
            print '\'' + str(x) + '\',' 
        print ']'
        print 'valuationdomain = {\'min\':0.0, \'med\':1.0, \'max\':2.0}' 
        print 'relation = {'
        for x in modname.actionset:
            print "\'" + str(x) + "\': {"	
            for y in modname.actionset:
		print "\'" + str(y) + "\':" + str(modname.relation[x][y]) + ','
            print '},'
        print '}'
        return 0

#................................................
if __name__=='__main__':
    import sys
    import time
    main()
    
