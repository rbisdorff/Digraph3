#######################
# R. Bisdorff 
# sortingDigraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsSortingDigraph.py
# # Current $Revision$
########################

from digraphs import *

############# test sortingDigraphs ####################
from sortingDigraphs import *

def testDefaultSortingDigraph():
    print('*---- testing default instantiation of the SortingDigraph Class ---*')
    s = SortingDigraph(isRobust=False)
    s.showCriteriaCategoryLimits()
    actions = list(s.getActionsKeys())
    sorting = s.computeSortingCharacteristics(Comments=True)
    actions.sort()
    for x in actions:
        for c in s.orderedCategoryKeys():
            if sorting[x][c] >= s.valuationdomain['med']:
                print('%s in %s = %.2f' % (x,c,sorting[x][c]['categoryMembership']))
    sorts = s.computePessimisticSorting(Comments=False)
    for c in s.orderedCategoryKeys():
        print(c, sorts[c])

def testRobustSortingDigraphClass():
    print('*---- testing SortingDigraph class instantiation ---*')
    t = RandomPerformanceTableau(numberOfCriteria=5)
    s = SortingDigraph(t)
    srb = SortingDigraph(t,isRobust=True)
    s.showCriteriaCategoryLimits()
    sorts = s.computePessimisticSorting(Comments=True)
    for c in s.orderedCategoryKeys():
        print(c, sorts[c])
    sorting = s.computeSortingCharacteristics(Comments=True)
    robustSorting = srb.computeSortingCharacteristics(Comments=True)
    actions = list(s.getActionsKeys())
    actions.sort()
    for x in actions:
        for c in s.orderedCategoryKeys():
            if sorting[x][c] >= s.valuationdomain['med']:
                print('%s in %s = %.2f (%d)' % (x,c,sorting[x][c]['categoryMembership'],robustSorting[x][c]['categoryMembership']))

def testShowSortingMethod():
    print('*---- testing showSorting method ----*')
    t = RandomPerformanceTableau(numberOfActions=10,numberOfCriteria=5)
    s = SortingDigraph(t,scaleSteps=5)
    html = s.showSorting(isReturningHTML=True)
    html += s.showSorting(Reverse=False,isReturningHTML=True)
    s.saveProfilesXMCDA2()
    fo = open('test.html','w')
    fo.write(html)
    fo.close()

def testSaveProfilesXMCDA2():
    print('*---- testing saveProfilesXMCDA2  method ----*')
    t = RandomPerformanceTableau(numberOfActions=10,numberOfCriteria=5)
    s = SortingDigraph(t,scaleSteps=5)
    s.showSorting()
    s.saveProfilesXMCDA2()

def testIConstructorLowerOpenCategories():
    print('*-------- Testing lowerOpen Categories -------')
    s = SortingDigraph(scaleSteps=5)
    s.criteriaCategoryLimits['lowerClosed']= False
    s.relation = s.constructRelation(s.criteria,s.evaluation,terminal=s.actionsOrig,initial=s.profileLimits,hasNoVeto=False, hasBipolarVeto=True)
    s.sorting = s.computeSortingCharacteristics()
    s.showSorting(Reverse=True)
    s.showCriteriaCategoryLimits()

def testLowerOpenClosedCategories():
    print('*-------- Testing lowerClosedOpen Categories -------')

    t = RandomCBPerformanceTableau()
    t.save('test')
    s = SortingDigraph(t,lowerClosed=True)
    s.showSorting(Reverse=True)
    s1 = SortingDigraph(t,lowerClosed=False)
    s1.showSorting(Reverse=True)

