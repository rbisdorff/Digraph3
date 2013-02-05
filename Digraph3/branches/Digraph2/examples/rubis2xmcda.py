#!/usr/bin/env python
# Python implementation of digraphs
# Current revision $Revision: 1.1 $
# Copyright (C) 2006-2008  Raymond Bisdorff
import sys
import digraphs
print '****************************************************'
print '* Python digraphs module                           *'
print '* $Revision: 1.1 $                               *'                   
print '* Copyright (C) 2006-2007 University of Luxembourg *'
print '* The module comes with ABSOLUTELY NO WARRANTY     *'
print '* to the extent permitted by the applicable law.   *'
print '* This is free software, and you are welcome to    *'
print '* redistribute it if it remains free software.     *'
print '****************************************************'
narg = len(sys.argv)
print narg, sys.argv
if narg < 2:
    print 'usage: rubis2xmcda.py inRubisXMLFile [outXMCDAFile] (!! file names without extensions !!)'
    sys.exit(1)
else:
    print 'Converting %s from Rubis XML format' % (sys.argv[1])
    t = digraphs.XMLRubisPerformanceTableau(sys.argv[1])
    if narg == 3:
        print 'to XMCDA 1.0 format in %s' % (sys.argv[2])
        t.saveXMCDA(fileName=sys.argv[2])
    else:
        print 'to XMCDA 1.0 format in %s' % (sys.argv[1])
        t.saveXMCDA(fileName=sys.argv[1])
    sys.exit(0)

    
