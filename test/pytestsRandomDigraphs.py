#######################
# R. Bisdorff
# randomDigraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsDigraph.py
# # Current $Revision: 1.53 $
########################

from randomDigraphs import *

def testRandomDigraph():

    print('==>> Testing generating random digraphs')
    h = RandomDigraph(order=5)
    h.showStatistics()
    h.showAll()

def testRandomRegularDigraph():
    print("==>> Testing random regular graph generation")
    g = RandomRegularDigraph(order=12,degree=4)
    g.showAll()
    g.showStatistics()

def testRandomFixedSizeDigraph():
    print("==>> Testing random fixed size digraph generation")
    g = RandomFixedSizeDigraph(order=12,size=40)
    g.showAll()
    g.showStatistics()

def testRandomFixedDegreeSequenceDigraph():
    print("==>> Testing random fixed degree sequence graph generation")
    g = RandomFixedDegreeSequenceDigraph(order=10,degreeSequence=[3,3,3,2,2,2,1,1,1,0])
    g.showAll()
    g.showStatistics()

def testRandomValuationDigraph():
    print('*==>> testing RandomValuationDigraph ----*')
    g = RandomValuationDigraph(ndigits=3)
    h = PolarisedDigraph(g,0.70)
    h.showRelationTable()
    h.save('testPol')
    hp = Digraph('testPol')
    g.showRelationTable()
    g.save('testVal')
    gs = Digraph('testVal')

def testWeakTournaments():
    print('*==>> weak tournaments ----*')
    t = RandomWeakTournament(order=5,ndigits=3)
    t.showRelationTable(ndigits=3)
    t = RandomWeakTournament(order=5,weaknessDegree=0.5)
    t.showRelationTable()
    t = RandomWeakTournament(order=5,IntegerValuation=True)
    t.showRelationTable()

def testRandomTournament():
    print('*----- test RandomTournament -----*')
    t = RandomTournament(order=5,ndigits=3,Crisp=False)
    t.showRelationTable()
    t = RandomTournament(order=5,Crisp=True)
    t.showRelationTable()
    t = RandomTournament(order=5,valuationDomain=(-10,10))
    t.showRelationTable()

def testIntegerRandomDigraph():
    print('==>> Testing Integer RandomDigraph() class instantiation ')
    g = RandomDigraph(order=10,IntegerValuation=True)
    g.save()
    g.computeChordlessCircuits(Comments=True,Debug=True)
