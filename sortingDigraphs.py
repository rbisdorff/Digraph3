#!/usr/bin/env python3
"""
Digraph3 collection of python3 modules for
Algorithmic Decision Theory applications.

Module for sorting and rating applications.

Copyright (C) 2016-2020  Raymond Bisdorff.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR ANY PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################
from digraphsTools import *
from digraphs import *
from outrankingDigraphs import *
from sortingDigraphs import *

class SortingDigraph(BipolarOutrankingDigraph):
    """
    Specialisation of the digraphs.BipolarOutrankingDigraph Class
    for Condorcet based multicriteria sorting of alternatives.

    Besides a valid PerformanceTableau instance we require a sorting profile,
    i.e.:

         * a dictionary <categories> of categories with 'name', 'order' and 'comment'
         * a dictionary <criteriaCategoryLimits> with double entry:

               [criteriakey][categoryKey] containing a ['minimum'] and
               a  ['maximum'] value in the scale of the criterion
               respecting the order of the categories.

    Template of required data for a 4-sorting::
        
        categories = {
                      'c1': { 'name': 'week','order': 1,
                              'lowLimit': 0,'highLimit': 25,
                              'comment': 'lowest category',},
                      'c2': { 'name': 'ok','order': 2,
                              'lowLimit': 25,'highLimit': 50,
                              'comment': 'medium category',},
                      'c3': { 'name': 'good','order': 3,
                              'lowLimit': 50,'highLimit': 75,
                              'comment': 'highest category',},
                      'c4': { 'name': 'excellent','order': 4,
                              'lowLimit': 75,'highLimit': 100,
                              'comment': 'highest category',},
         }
        criteriaCategoryLimits['LowerClosed'] = True # default
        criteriaCategoryLimits[g] = {
                'c1': {'minimum':0, 'maximum':25},
                'c2': {'minimum':25, 'maximum':50},
                'c3': {'minimum':50, 'maximum':75},
                'c4': {'minimum':75, 'maximum':200},
         }

    A template named tempProfile.py is providied in the digraphs module distribution.
        
    .. note::

        We generally require a performanceTableau instance and a filename
        where categories and a profile my be read from. If no such filename is given,
        then a default profile with five, equally spaced, categories is used
        on each criteria. By default lower-closed limts of categories are
        supposed to be used in the sorting.

    Example Python3 session:

    >>> from sortingDigraphs import SortingDigraph
    >>> from randomPerfTabs import RandomPerformanceTableau
    >>> t = RandomPerformanceTableau(seed=1)
    >>> [x for x in t.actions]
    ['a01', 'a02', 'a03', 'a04', 'a05', 'a06', 'a07', 'a08',
    'a09', 'a10', 'a11', 'a12', 'a13']
    >>> so = SortingDigraph(t,scaleSteps=5)
    # so gives a sorting result into five lower closed ordered
    # categories enumerated from 0 to 5.
    >>> so.showSorting()
    *--- Sorting results in descending order ---*
    ]> - 4]: 	 ['a02', 'a03', 'a11']
    ]4 - 3]: 	 ['a04', 'a07', 'a08', 'a09', 'a10', 'a11', 'a12', 'a13']
    ]3 - 2]: 	 ['a04', 'a05', 'a06', 'a09', 'a12']
    ]2 - 1]: 	 ['a01']
    ]1 - 0]: 	 []
    # Notice that some alternatives, like a04, a09, a11 and a12 are sorted
    # into more than one adjacent category. Weak ordering the sorting result
    # into ordered adjacent categories gives following result:
    >>> so.showWeakOrder(strategy='average',Descending=True)
    Weak ordering by average normalized 5-sorting limits
    ]  >  -80.0] : ['a02', 'a03']
    ]100.0-60.0] : ['a11']
    ] 80.0-60.0] : ['a07', 'a08', 'a10', 'a13']
    ] 80.0-40.0] : ['a04', 'a09', 'a12']
    ] 60.0-40.0] : ['a05', 'a06']
    ] 40.0-20.0] : ['a01']

    """
    def __init__(self,argPerfTab=None,\
                 argProfile=None,\
                 scaleSteps=5,\
                 minValuation=-100.0,\
                 maxValuation=100.0,\
                 isRobust=False,\
                 hasNoVeto=False,\
                 LowerClosed=True,\
                 StoreSorting=True,\
                 Threading=False,\
                 tempDir=None,\
                 nbrCores=None,\
                 Debug=False):
        """
        Constructor for SortingDigraph instances.

        """

        from copy import copy, deepcopy
        from decimal import Decimal
        from collections import OrderedDict
        from time import time

        # import or generate a performance tableau
        tt = time()
        if argPerfTab == None:
            print('!!! No valid performance tableau given!!')
            print('!!! Random standard performance tableau generated!!')
            from randomPerfTabs import RandomPerformanceTableau
            perfTab = RandomPerformanceTableau(numberOfActions=10,
                                               numberOfCriteria=13)
        elif isinstance(argPerfTab,str):
            try:
                perfTab = XMCDA2PerformanceTableau(argPerfTab)
            except:
                print('Performance Tableau not in XMCDA2 format!')
                perfTab = None
        else:
            perfTab = argPerfTab

        # normalize the actions as a dictionary construct
        if isinstance(perfTab.actions,list):
            actions = OrderedDict()
            for x in perfTab.actions:
                actions[x] = {'name': str(x)}
            self.actions = actions
        else:
            self.actions = deepcopy(perfTab.actions)
        self.criteria = deepcopy(perfTab.criteria)
        self.convertWeight2Decimal()
        self.evaluation = deepcopy(perfTab.evaluation)
        self.convertEvaluation2Decimal()

        # keep a copy of the original actions set before adding the profiles
        actionsOrig = deepcopy(perfTab.actions)
        self.actionsOrig = actionsOrig
        
        #  input the profiles
        if argProfile != None:
            defaultProfiles = False
            # normalize the actions as a dictionary construct
            if isinstance(perfTab.actions,list):
                actions = OrderedDict()
                for x in perfTab.actions:
                    actions[x] = {'name': str(x)}
                self.actions = actions
            else:
                self.actions = deepcopy(perfTab.actions)
            self.criteria = deepcopy(perfTab.criteria)
            self.convertWeight2Decimal()
            self.evaluation = deepcopy(perfTab.evaluation)
            self.convertEvaluation2Decimal()
            if isinstance(argProfile,str): # input from stored instantiation
                fileName = argProfile
                fileNameExt = fileName + '.py'
                profile = OrderedDict()
                exec(compile(open(fileNameExt).read(), fileNameExt, 'exec'),profile)
                #print(profile)
                self.name = fileName
                self.categories = profile['categories']
                self.criteriaCategoryLimits = profile['criteriaCategoryLimits']
#                self.profiles = profile['profiles']
#                self.profileLimits = set(self.profiles['min']) | \
#                                     set(self.profiles['max'])
            else: # input from a profiles dictionary
                self.name = 'sorting_with_given_profile'
                self.categories = argProfile['categories'].copy()
                self.criteriaCategoryLimits = argProfile['criteriaCategoryLimits'].copy()
#                self.profiles = {}

        else:
            defaultProfiles = True
            self.name = 'sorting_with_default_profiles'
            normPerfTab = NormalizedPerformanceTableau(perfTab)
            self.actions = normPerfTab.actions
            self.criteria = normPerfTab.criteria
            self.convertWeight2Decimal()
            self.evaluation = normPerfTab.evaluation
            self.convertEvaluation2Decimal()
            # supposing all criteria scales between 0.0 and 100.0
            lowValue = Decimal('0.0')
            highValue = Decimal('100.0')
            # with preference direction = max
            categories = OrderedDict()
            k = highValue / Decimal(str(scaleSteps))
            nd = len(str(scaleSteps))
            for i in range(scaleSteps):
                categories[str(i)] = {'name':('c%%0%dd' % (nd)) % (i+1),\
                                     'order':i,\
                                     'lowLimit': Decimal('%.1f' % (i*k)),\
                                     'highLimit': Decimal('%.1f' % ((i+1)*k))}            
            self.categories = categories
            criteriaCategoryLimits = OrderedDict()
            criteriaCategoryLimits['LowerClosed'] = LowerClosed
            for g in self.criteria:
                criteriaCategoryLimits[g] = {}
                k = (self.criteria[g]['scale'][1] - \
                     self.criteria[g]['scale'][0]) / scaleSteps
                i = 0
                for c in categories:
                    if i < (scaleSteps-1):
                        gHighLimit = Decimal('%.1f' %\
                                    (self.criteria[g]['scale'][0] + (i+1)*k))
                    else:
                        gHighLimit = Decimal('%.1f' % (2*self.criteria[g]['scale'][1]))
                    if i > 0:
                        gLowLimit = Decimal('%.1f' %\
                                    (self.criteria[g]['scale'][0] + (i)*k))
                    else:
                        gLowLimit = Decimal('%.1f' % (-self.criteria[g]['scale'][1]))
                    criteriaCategoryLimits[g][c]={
                        'minimum': Decimal('%.1f' % gLowLimit),
                        'maximum': Decimal('%.1f' % gHighLimit)
                        }
                    i += 1
            self.criteriaCategoryLimits = criteriaCategoryLimits
            
            # set the category limits type (LowerClosed = True)
            self.criteriaCategoryLimits['LowerClosed'] = LowerClosed
            
        self.runTimes={'dataInput': time()-tt}
        

        # add the catogory limits to the actions set
        actions = self.actions
        criteria = self.criteria
        evaluation = self.evaluation
        categories = self.categories
        criteriaCategoryLimits = self.criteriaCategoryLimits
        t0 = time()
        profiles = {'min':{},'max':{}}
        profileLimits = set()
        for c in categories.keys():
            cMinKey = c+'-m'
            cMaxKey = c+'-M'
            profileLimits.add(cMinKey)
            profileLimits.add(cMaxKey)
            actions[cMinKey] = {'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
            actions[cMaxKey] = {'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
            profiles['min'][cMinKey] = {'category': c, 'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
            profiles['max'][cMaxKey] = {'category': c, 'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
            for g in criteria.keys():
                try:
                    if criteria[g]['preferenceDirection'] == 'max':
                        evaluation[g][cMinKey] = Decimal(str(criteriaCategoryLimits[g][c]['minimum']))
                        evaluation[g][cMaxKey] = Decimal(str(criteriaCategoryLimits[g][c]['maximum']))
                    elif criteria[g]['preferenceDirection'] == 'min':
                        if not defaultProfiles:
                            highValueg = Decimal(str(criteria[g]['scale'][1]))
                        else:
                            highValueg = Decimal('%.1f' % highValue)
                        #print 'highValue = ', highValue
                        evaluation[g][cMinKey] = -(highValueg - Decimal(str(criteriaCategoryLimits[g][c]['minimum'])))
                        evaluation[g][cMaxKey] = -(highValueg - Decimal(str(criteriaCategoryLimits[g][c]['maximum'])))
                    else:
                        print('===>>>>> Error')
                except:

                    evaluation[g][cMinKey] = Decimal(str(criteriaCategoryLimits[g][c]['minimum']))
                    evaluation[g][cMaxKey] = Decimal(str(criteriaCategoryLimits[g][c]['maximum']))
                #print 'LowerClosed', LowerClosed
        self.profiles = profiles
        self.profileLimits = profileLimits
        self.evaluation = evaluation
        self.convertEvaluation2Decimal()
        self.LowerClosed = LowerClosed

        self.runTimes['computeProfiles'] =  time()-t0

        
        # construct outranking relation
        t0 = time()
        if isRobust:
            g = RobustOutrankingDigraph(self)
            self.valuationdomain = g.valuationdomain
            self.relation = g.relation
        else:
            Min = Decimal('%.4f' % minValuation)
            Max = Decimal('%.4f' % maxValuation)
            Med = (Max + Min)/Decimal('2.0')
            self.valuationdomain = {'min': Min, 'med':Med ,'max':Max }
            if LowerClosed:
                relation = BipolarOutrankingDigraph._constructRelationWithThreading(self,criteria,
                                                       self.evaluation,
                                                       initial=actionsOrig,
                                                       terminal=profileLimits,
                                                       hasNoVeto=hasNoVeto,
                                                       hasBipolarVeto=True,
                                                        Threading=Threading,
                                                        tempDir=tempDir,
                                                        WithConcordanceRelation=False,
                                                        WithVetoCounts=False,
                                                        Debug=Debug)
            else:
                relation = BipolarOutrankingDigraph._constructRelationWithThreading(self,criteria,
                                                       self.evaluation,
                                                       terminal=actionsOrig,
                                                       initial=profileLimits,
                                                       hasNoVeto=hasNoVeto,
                                                        hasBipolarVeto=True,
                                                        Threading=Threading,
                                                        tempDir=tempDir,
                                                        WithConcordanceRelation=False,
                                                        WithVetoCounts=False,
                                                        Debug=Debug)
            if LowerClosed:
                for x in actionsOrig.keys():
                    rx = relation[x]
                    for y in actionsOrig.keys():
                        rx[y] = Med
                for x in profileLimits:
                    relation[x] = {}
                    rx = relation[x]
                    for y in actions.keys():
                        rx[y] = Med
            else:
                for x in actionsOrig.keys():
                    relation[x] = {}
                    rx = relation[x]
                    for y in actionsOrig.keys():
                        rx[y] = Med
                for y in profileLimits:
                    for x in actions.keys():
                        relation[x][y] = Med
            self.relation = relation
        self.runTimes['computeRelation'] = time()-t0
        
        # compute weak ordering
        t0 = time()
        sortingRelation = self.computeSortingRelation(Debug=Debug,)
        relation = self.relation
        for x in actionsOrig.keys():
            rx = relation[x]
            srx = sortingRelation[x]
            for y in actionsOrig.keys():
                rx[y] = srx[y]

        # reset original action set
        self.actions = actionsOrig

        # compute weak ordering by choosing
        # self.computeRankingByChoosing() !!! not scalable !!!
        # obsolete: replaced by self.computeWeakOrder()

        # init general digraph Data
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['weakOrdering'] = time()-t0
        self.runTimes['totalTime'] = time()-tt

#########
    def __repr__(self):
        """
        Default presentation method for BipolarOutrankingDigraph instance.
        """
        String =  '*-----  Object instance description -----------*\n'
        String += 'Instance class      : %s\n' % self.__class__.__name__
        String += 'Instance name       : %s\n' % self.name
        String += '# # Actions         : %d\n' % self.order
        String += '# Criteria          : %d\n' % len(self.criteria)
        String += '# Categories        : %d\n' % len(self.categories)
        String += 'Lowerclosed         : %s\n' % str(self.criteriaCategoryLimits['LowerClosed'])
        String += 'Size                : %d\n' % self.computeSize()
        String += 'Determinateness     : %.3f\n' % self.computeDeterminateness()
        String += '*------  Constructor run times (in sec.) ------*\n'
        try:
            String += '# Threads        : %d\n' % self.nbrThreads
        except:
            self.nbrThreads = 1
            String += '# Threads        : %d\n' % self.nbrThreads
        String += 'Total time       : %.5f\n' % self.runTimes['totalTime']
        String += 'Data input       : %.5f\n' % self.runTimes['dataInput']
        String += 'Compute profiles : %.5f\n' % self.runTimes['computeProfiles']
        String += 'Compute relation : %.5f\n' % self.runTimes['computeRelation']
        String += 'Weak Ordering    : %.5f\n' % self.runTimes['weakOrdering']
        return String 

    def saveCategories(self,fileName='tempCategories'):

        fileName += '.py'
        print('*--- Saving sorting categories in file: <%s> ---*' % fileName)
        with open(fileName,'w') as fo:
            fo.write('# categories save method from the SortingDigraph class\n')
            fo.write('from collections import OrderedDict\n')
            fo.write('from decimal import Decimal\n')
           # save categories
            fo.write('categories = OrderedDict([\n')
            for c in self.categories:
                fo.write('(\'%s\',%s),\n' % (c,str(self.categories[c])))
            fo.write('])\n')
            # save criteria category limits
            fo.write('criteriaCategoryLimits = OrderedDict([\n')
            fo.write('(\'LowerClosed\',%s),\n' %\
                     (str(self.criteriaCategoryLimits['LowerClosed'])) )
            for g in self.criteria:
                fo.write('(\'%s\',{\n' % (g))
                for c in self.categories:
                    fo.write('\'%s\' :%s,\n' %\
                             (c,str(self.criteriaCategoryLimits[g][c])) )
                fo.write('}),\n')
            fo.write('])\n')
        # close
        
        
    def htmlCriteriaCategoryLimits(self,tableTitle='Category limits'):
        """
        Renders category minimum and maximum limits for each criterion
        as a html table.
        """
        s = ''
        s += '<h1>%s</h1>' % tableTitle
        s += '<table border="1">'

        criterionKeys = [x for x in self.criteria]
        categoryKeys = [x for x in self.categories]
        s += '<tr><th>Criteria</th>'
        for g in criterionKeys:
            s += '<th>%s</th>' % g
        s += '</tr>'

        for g in criterionKeys:
            s += '<tr><th>%s</th></tr>' % (g)
            s += '<tr><th>Lower limit</th>'
            for c in categoryKeys:
                #print '\t', c, (self.criteriaCategoryLimits[g][c]['minimum'],self.criteriaCategoryLimits[g][c]['maximum'])
                s += '<td>%2.f</td>' % (self.criteriaCategoryLimits[g][c]['minimum'])
            s += '</tr>'
            s += '<tr><th>Upper limit</th>'
            for c in categoryKeys:
                #print '\t', c, (self.criteriaCategoryLimits[g][c]['minimum'],self.criteriaCategoryLimits[g][c]['maximum'])
                s += '<td>%2.f</td>' % (self.criteriaCategoryLimits[g][c]['maximum'])
        s += '</tr>'

        s += '</table>'
        return s

    def computeWeakOrder(self,Descending=False,strategy='average',\
                         Comments=False,Debug=False):
        """
        specialisation of the showWeakOrder method.
        The weak ordering strategy may be:

           "optimistic" (ranked by highest category limits),
           "pessimistic" (ranked by lowest category limits) or
           "average" (ranked by average category limits)
        """
        actions = self.actions
        categories = self.categories
        actionsCategories = {}
        actionsCategoryLimits = {}
        for x in actions.keys():
            a,lowCateg,highCateg,credibility = self.showActionCategories(x,Comments=Debug)
            if Debug:
                print(actions[x],a,lowCateg,highCateg,credibility)
                print(strategy)
            if strategy == 'average': # average by default
                lc = categories[lowCateg]['lowLimit']
                hc = categories[highCateg]['highLimit']
                ac = (lc+hc)/Decimal('2.0')
                try:
                    actionsCategories[(ac,categories[highCateg]['highLimit'],\
                        categories[lowCateg]['lowLimit'])]['categoryContent'].append(a)
                except:
                    actionsCategories[(ac,categories[highCateg]['highLimit'],\
                                       categories[lowCateg]['lowLimit'])] =\
                                        {'categoryContent': [a], 'categoryInterval': (lowCateg,highCateg)}
            else: # strategy == "optimistic" or "pessimistic":
                try:
                    actionsCategories[(categories[highCateg]['highLimit'],\
                                       categories[lowCateg]['lowLimit'])]['categoryContent'].append(a)
                except:
                    actionsCategories[(categories[highCateg]['highLimit'],\
                                       categories[lowCateg]['lowLimit'])] =\
                                        {'categoryContent': [a], 'categoryInterval': (lowCateg,highCateg)}                                                            
        #print(actionsCategories)    
        actionsCategIntervals = []
        for interval in actionsCategories:
            #print(interval)
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        actionsCategIntervals.sort(reverse=Descending)
        weakOrdering = []
        catKeys = [x for x in self.categories]
        #print(catKeys)
        if Comments:
            k = len(self.categories)
            print('Weak ordering with %s normalized %d-sorting limits' % (strategy,k) )
        
        for ci,item in enumerate(actionsCategIntervals):
            #print(item[1])
            interval = item[1]['categoryInterval']
            content = item[1]['categoryContent']
            if Comments:
##                if strategy == "average":
                if Descending:
                    if interval[1] == interval[0]:
                        catName0 = self.categories[interval[0]]['name']
                        print('[%s]   : %s' % (catName0,content) )
                    else:
                        catName0 = self.categories[interval[0]]['name']
                        catName1 = self.categories[interval[1]]['name']
                        print('[%s-%s] : %s' % (catName1,\
                                            catName0,\
                                            content ) )
                else:
                    if interval[0] == interval[1]:
                        catName1 = self.categories[interval[1]]['name']
                        print('[%s]   : %s' % (catName1,\
                                            content ) )
                    else:
                        catName0 = self.categories[interval[0]]['name']
                        catName1 = self.categories[interval[1]]['name']
                        print('[%s-%s] : %s' % (catName0,\
                                            catName1,\
                                            content ) )                           
                            

            weakOrdering.append(content)
        return weakOrdering

    def showWeakOrder(self,Descending=False,strategy='average'):
        """ dummy for computeWeakOrder with Comments=True """
        self.computeWeakOrder(Descending=Descending,strategy=strategy,Comments=True)
        

    def computeSortingRelation(self,categoryContents=None,StoreSorting=True,Debug=False):
        """
        constructs a bipolar sorting relation using the category contents.
        """
        if categoryContents == None:
            categoryContents = self.computeCategoryContents(StoreSorting=True,)
        categoryKeys = self.orderedCategoryKeys()

        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        actions = [x for x in self.actionsOrig]
        currActions = set(actions)
        #sortedActions = set()
        sortingRelation = {}
        for x in actions:
            sortingRelation[x] = {}
            srx = sortingRelation[x]
            for y in actions:
                srx[y] = Med
                
        if Debug:
            print('categoryContents',categoryContents)
        for i in categoryKeys:
            ibch = set(categoryContents[i])
            ribch = set(currActions) - ibch
            if Debug:
                print('ibch,ribch',ibch,ribch)
            for x in ibch:
                for y in ibch:
                    sortingRelation[x][y] = Med
                    sortingRelation[y][x] = Med
                for y in ribch:
                    sortingRelation[x][y] = Min
                    sortingRelation[y][x] = Max
            currActions = currActions - ibch
        return sortingRelation


    def showCriteriaCategoryLimits(self):
        """
        Shows category minimum and maximum limits for each criterion.
        """
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True
        criteria = self.criteria
        categories = self.categories
        for g in criteria:
            print(g)
            for c in categories:
                if LowerClosed:
                    print('\t%s [%s; %s[' % (c, self.criteriaCategoryLimits[g][c]['minimum'],self.criteriaCategoryLimits[g][c]['maximum']))
                else:
                    print('\t%s ]%s; %s]' % (c, self.criteriaCategoryLimits[g][c]['minimum'],self.criteriaCategoryLimits[g][c]['maximum']))

    def getActionsKeys(self,action=None,withoutProfiles=True):
        """
        extract normal actions keys()
        """
        profiles_m = set(self.profiles['min'])
        profiles_M = set(self.profiles['max'])
        if action == None:
            actionsExt = set(self.actions)
            if withoutProfiles:
                return actionsExt - profiles_m - profiles_M
            else:
                return actionsExt | profiles_m | profiles_M
        else:
            return set([action])           

    def orderedCategoryKeys(self,Reverse=False):
        """
        Renders the ordered list of category keys
        based on self.categories['order'] numeric values.
        """
        orderedCategoryKeys = list(self.categories.keys())
        if Reverse:
            orderedCategoryKeys.reverse()
        return orderedCategoryKeys

    def _computeWeakOrder(self,Descending=True,strategy=None,Comments=None,Debug=False):
        """
        Specialisation for QuantilesSortingDigraphs.
        """
        from decimal import Decimal
        cC = self.computeCategoryContents()
        
        if Descending:
            cCKeys = self.orderedCategoryKeys(Reverse = True)
        else:
            cCKeys = self.orderedCategoryKeys(Reverse = False)
        if Debug:
            print(cCKeys)
        n = len(cC)
        n2 = n//2
        ordering = []
        
        for i in range(n2):
            if i == 0:
                x = cC[cCKeys[i]]
                y = cC[cCKeys[n-i-1]]
                setx = set(x)
                sety = set(y) - setx
            else:
                x = list(set(cC[cCKeys[i]]) - (setx | sety))
                setx = setx | set(x)
                y = list(set(cC[cCKeys[n-i-1]]) - (setx | sety))
                sety = sety | set(y)
            if x != [] or y != []:
                ordering.append( ( (Decimal(str(i+1)),x),(Decimal(str(n-i)),y) ) )
        if 2*n2 < n:
            if n2 == 0:
                x = cC[cCKeys[n2]]
            else:
                x = list(set(cC[cCKeys[n2]]) - (setx | sety))
            ordering.append( ( (Decimal(str(n2+1)),x),(Decimal(str(n2+1)),[]) ) )

        if Debug:
            print(ordering)
        
        orderingList = []
        n = len(ordering)
        for i in range(n):
            x = ordering[i][0][1]
            if x != []:
                orderingList.append(x)
        for i in range(n):
            y = ordering[n-i-1][1][1]
            if y != []:
                orderingList.append(y)
                
        return orderingList

    def showOrderedRelationTable(self,direction="decreasing"):
        """
        Showing the relation table in decreasing (default) or increasing order.
        """
        if direction == "decreasing":
            Descending = True
        else:
            Descending = False

        weakOrdering = self.computeWeakOrder(Descending)
        
        actionsList = []
        for eq in weakOrdering:
            #print(eq)
            eq.sort()
            for x in eq:
                actionsList.append(x)
        if len(actionsList) != len(self.actions):
            print('Error !: missing action(s) %s in ordered table.')
            
        Digraph.showRelationTable(self,actionsSubset=actionsList,\
                                relation=self.relation,\
                                Sorted=False,\
                                ReflexiveTerms=False)

    def exportDigraphGraphViz(self,fileName=None, bestChoice=set(),worstChoice=set(),Comments=True,graphType='png',graphSize='7,7'):
        """
        export GraphViz dot file for digraph drawing filtering.
        """
        Digraph.exportGraphViz(self, fileName=fileName,\
                               bestChoice=bestChoice,\
                               worstChoice=worstChoice,\
                               Comments=Comments,\
                               graphType=graphType,\
                               graphSize=graphSize)


    def exportGraphViz(self,fileName=None,direction='decreasing',\
                       Comments=True,graphType='png',\
                       graphSize='7,7',\
                       fontSize=10,
                       relation=None,
                       Debug=False):
        """
        export GraphViz dot file for weak order (Hasse diagram) drawing
        filtering from SortingDigraph instances.
        """
        import os
        from copy import copy, deepcopy

        def _safeName(t0):
            try:
                t = t0.split(sep="-")
                t1 = t[0]
                n = len(t)
                if n > 1:
                    for i in range(1,n):
                        t1 += '%s%s' % ('_',t[i])
                return t1
            except:
                print('Error in nodeName: %s !!' % t0, type(t0))
                return t0
                
        if direction == 'decreasing':
            ordering = self.computeWeakOrder(Descending=True)
        else:
            ordering = self.computeWeakOrder(Descending=False)
        if Debug:
            print(ordering)
                    
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')
        actionKeys = [x for x in self.actions]
        n = len(actionKeys)
        if relation == None:
            relation = self.relation
        Med = self.valuationdomain['med']
        i = 0
        if fileName == None:
            name = self.name
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)

        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        fo.write('graph [ bgcolor = cornsilk, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        fo.write('\\transitiveDigraphs module (graphviz)\\n R. Bisdorff, 2014", size="')
        fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
        # nodes
        for x in actionKeys:
            try:
                nodeName = self.actions[x]['shortName']
            except:
                nodeName = str(x)
            node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                   % (str(_safeName(x)),_safeName(nodeName),fontSize)
            fo.write(node)
        # same ranks for Hasses equivalence classes
        k = len(ordering)
        for i in range(k):
            sameRank = '{ rank = same; '
            ich = ordering[i]
            for x in ich:
                sameRank += str(_safeName(x))+'; '
            sameRank += '}\n'
            print(i,sameRank)
            fo.write(sameRank)
        # save original relation
        originalRelation = copy(self.relation)
        self.relation = relation
        self.closeTransitive(Reverse=True)
        for i in range(k-1):
            ich = ordering[i]
            for x in ich:
                for j in range(i+1,k):
                    jch = ordering[j]
                    for y in jch:
                        #edge = 'n'+str(i+1)+'-> n'+str(i+2)+' [dir=forward,style="setlinewidth(1)",color=black, arrowhead=normal] ;\n'
                        if self.relation[x][y] > self.valuationdomain['med']:
                            arcColor = 'black'
                            edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' % (_safeName(x),_safeName(y),1,arcColor)
                            fo.write(edge)
                        elif self.relation[y][x] > self.valuationdomain['med']:
                            arcColor = 'black'
                            edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' % (_safeName(y),_safeName(x),1,arcColor)
                            fo.write(edge)
                                                  
        fo.write('}\n \n')
        fo.close()
        # restore original relation
        self.relation = copy(originalRelation)

        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')

    def computeSortingCharacteristics(self, action=None, StoreSorting=True,\
                                      Comments=False, Debug=False,\
                                        Threading=False, nbrOfCPUs=None):
        """
        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "action x in A belongs to category c in C",
        ie x outranks low category limit and does not outrank
        the high category limit.
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        actions = list(self.getActionsKeys(action))
        na = len(actions)
            
        #categories = list(self.orderedCategoryKeys())
        categories = self.categories

        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True
        if Threading:
            from multiprocessing import Process, active_children
            from pickle import dumps, loads, load
            from os import cpu_count
            class myThread(Process):
                def __init__(self, threadID, tempDirName, actions, catKeys,LowerClosed,Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.workingDirectory = tempDirName
                    self.actions = actions
                    self.catKeys = catKeys
                    self.LowerClosed = LowerClosed
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    chdir(self.workingDirectory)
                    if self.Debug:
                        print("Starting working in %s on %s" % (self.workingDirectory, self.name))
                        print('actions,catKeys',self.actions,self.catKeys)
                    fi = open('dumpSelfRelation.py','rb')
                    #context = loads(fi.read())
                    relation = loads(fi.read())
                    fi.close()
                    Min = context.valuationdomain['min']
                    Max = context.valuationdomain['max']
                    actions = self.actions
                    catKeys = self.catKeys
                    LowerClosed = self.LowerClosed
                    #relation = context.relation
                    sorting = {}
                    for x in actions:
                        sorting[x] = {}
                        for c in catKeys:
                            sorting[x][c] = {}
                            cMinKey= c+'-m'
                            cMaxKey= c+'-M'
                            if LowerClosed:
                                lowLimit = relation[x][cMinKey]
                                notHighLimit = Max - relation[x][cMaxKey] + Min
                            else:
                                lowLimit = Max - relation[cMinKey][x] + Min
                                notHighLimit = relation[cMaxKey][x]
                            if self.Debug:
                                print('%s in %s: low = %.2f, high = %.2f' % \
                                      (x, c,lowLimit,notHighLimit), end=' ')
                            categoryMembership = min(lowLimit,notHighLimit)
                            sorting[x][c]['lowLimit'] = lowLimit
                            sorting[x][c]['notHighLimit'] = notHighLimit
                            sorting[x][c]['categoryMembership'] = categoryMembership
                            if self.Debug:
                                print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'],\
                                   sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
                        if self.Debug:
                            print(sorting[x])
                    foName = 'sorting-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(sorting,-1))
                    fo.close()
            print('Threaded computing of sorting characteristics ...')        
            from tempfile import TemporaryDirectory,mkdtemp
            tempDirName = mkdtemp()
            td = time()
            selfFileName = tempDirName +'/dumpSelfRelation.py'
            if Debug:
                print('temDirName, selfFileName', tempDirName,selfFileName)
            fo = open(selfFileName,'wb')
            pd = dumps(self.relation,-1)
            fo.write(pd)
            fo.close()
            if Comments:
                print('Relation dump: %.5f' % (time()-td))
           
            if nbrOfCPUs == None:
                nbrOfCPUs = cpu_count()-1
            print('Nbr of actions',na)
            
            nbrOfJobs = na//nbrOfCPUs
            if nbrOfJobs*nbrOfCPUs < na:
                nbrOfJobs += 1
            print('Nbr of threads = ',nbrOfCPUs)
            print('Nbr of jobs/thread',nbrOfJobs)
            nbrOfThreads = 0
            for j in range(nbrOfCPUs):
                print('thread = %d/%d' % (j+1,nbrOfCPUs),end="...")
                start= j*nbrOfJobs
                if (j+1)*nbrOfJobs < na:
                    stop = (j+1)*nbrOfJobs
                else:
                    stop = na
                thActions = actions[start:stop]
                if Debug:
                    print(thActions)
                if thActions != []:
                    process = myThread(j,tempDirName,thActions,categories,LowerClosed,Debug)
                    process.start()
                    nbrOfThreads += 1
            while active_children() != []:
                pass
                #sleep(1)
            print('Exit %d threads' % nbrOfThreads)
            sorting = {}
            for th in range(nbrOfThreads):
                if Debug:
                    print('job',th)
                fiName = tempDirName+'/sorting-'+str(th)+'.py'
                fi = open(fiName,'rb')
                sortingThread = loads(fi.read())
                if Debug:
                    print('sortingThread',sortingThread)
                sorting.update(sortingThread)
        # end of Threading
        else: # with out Threading 
            sorting = {}
            for x in actions:
                sorting[x] = {}
                for c in categories:
                    sorting[x][c] = {}
                    cMinKey= c+'-m'
                    cMaxKey= c+'-M'
                    if LowerClosed:
                        lowLimit = self.relation[x][cMinKey]
                        notHighLimit = Max - self.relation[x][cMaxKey] + Min
                    else:
                        lowLimit = Max - self.relation[cMinKey][x] + Min
                        notHighLimit = self.relation[cMaxKey][x]
                    if Debug:
                        print('%s in %s: low = %.2f, high = %.2f' % \
                              (x, c,lowLimit,notHighLimit), end=' ')
                    categoryMembership = min(lowLimit,notHighLimit)
                    sorting[x][c]['lowLimit'] = lowLimit
                    sorting[x][c]['notHighLimit'] = notHighLimit
                    sorting[x][c]['categoryMembership'] = categoryMembership

                    if Debug:
                        print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
        if StoreSorting:
            self.sorting = sorting
        return sorting
    
    def showSortingCharacteristics(self, action=None):
        """
        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "action x in A belongs to category c in C",
        ie x outranks low category limit and does not outrank
        the high category limit.
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        actions = self.getActionsKeys(action)
            
        categoryKeys = self.orderedCategoryKeys()

        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True

        sorting = {}
        if LowerClosed:
            print('x  in  K_k\t r(x >= m_k)\t r(x < M_k)\t r(x in K_k)')
        else:
            print('x  in  K_k\t r(m_k < x)\t r(M_k >= x)\t r(x in K_k)')
        for x in actions:
            sorting[x] = {}
            for i in range(len(categoryKeys)):
                sorting[x][categoryKeys[i]] = {}
                cMinKey= categoryKeys[i]+'-m'
                cMaxKey= categoryKeys[i]+'-M'
                if LowerClosed:
                    lowLimit = self.relation[x][cMinKey]
                    notHighLimit = Max - self.relation[x][cMaxKey] + Min
                else:
                    lowLimit = Max - self.relation[cMinKey][x] + Min
                    notHighLimit = self.relation[cMaxKey][x]
                if LowerClosed:
                    if i < (len(categoryKeys)-1):
                        print('%s in [%s - %s[\t' % (x, categoryKeys[i],categoryKeys[i+1]), end=' ')
                    else:
                        print('%s in [%s - %s[\t' % (x, categoryKeys[i],' '), end=' ')
                        
                else:
                    if i == 0:
                        print('%s in ]%s - %s]\t' % (x, ' ',categoryKeys[i]), end=' ')
                    else:
                        print('%s in ]%s - %s]\t' % (x, categoryKeys[i-1],categoryKeys[i]), end=' ')
                        
                categoryMembership = min(lowLimit,notHighLimit)
                sorting[x][categoryKeys[i]]['lowLimit'] = lowLimit
                sorting[x][categoryKeys[i]]['notHighLimit'] = notHighLimit
                sorting[x][categoryKeys[i]]['categoryMembership'] = categoryMembership
                print('%.2f\t\t %.2f\t\t %.2f' % (sorting[x][categoryKeys[i]]['lowLimit'],\
                                                  sorting[x][categoryKeys[i]]['notHighLimit'],\
                                                  sorting[x][categoryKeys[i]]['categoryMembership']))

    def _computePessimisticSorting(self, Comments=False):
        """
        Returns a dictionary with category keys gathering the actions per ordered category on
        the basis of a bipolar valued outranking relation Stilde with low and high category limt profiles.

        An action x is added to cotegory c if (a Stilde c_min) > Med and a Stilde C_Max <= Med.
        """
        actions = self.getActionsKeys()
        categories = self.orderedCategoryKeys()
        Med = self.valuationdomain['med']

        sorts = {}
        for c in categories:
            sorts[c] = set()
        for x in actions:
            if Comments:
                print(x)
            for c in categories:
                overMin=True
                overMax = True
                cMinKey= c+'-m'
                cMaxKey= c+'-M'
                if Comments:
                    print('\t %s: low = %.2f, high = %.2f' % (c,self.relation[x][cMinKey],self.relation[x][cMaxKey]))
                if self.relation[x][cMinKey] > Med:
                    overMin = True
                else:
                    break
                if self.relation[x][cMaxKey] <= Med:
                    overMax = False
                    #print '\t %s: low = %.2f, high = %.2f' % (c,self.relation[x][cMinKey],self.relation[x][cMaxKey])
                    sorts[c].add(x)
                    break
            if overMin and overMax:
                #print '\t %s: low = %.2f, high = %.2f' % (c,self.relation[x][cMinKey],self.relation[x][cMaxKey])
                sorts[c].add(x)
        if Comments:
            print('Sorting results')
            for c in self.orderedCategoryKeys():
                print('%s: %s' % (c, str(sorts[c])))
        return sorts

    def computeCategoryContents(self,Reverse=False,StoreSorting=True,Comments=False):
        """
        Computes the sorting results per category.
        """
        Med = self.valuationdomain['med']
        actions = list(self.getActionsKeys())
        actions.sort()
        try:
            sorting=self.sorting
        except:
            sorting = self.computeSortingCharacteristics(StoreSorting=StoreSorting,Comments=Comments)

        categoryContent = {}
        for c in self.orderedCategoryKeys(Reverse=Reverse):
            categoryContent[c] = []
            for x in actions:
                if sorting[x][c]['categoryMembership'] >= Med:
                    categoryContent[c].append(x)
        if StoreSorting:
            self.categoryContent = categoryContent
        return categoryContent
                                                     
    def showSorting(self,Reverse=True,isReturningHTML=False):
        """
        Shows sorting results in decreasing or increasing (Reverse=False)
        order of the categories. If isReturningHTML is True (default = False)
        the method returns a htlm table with the sorting result.
        """
        #from string import replace
        try:
            categoryContent = self.categoryContent
        except:
            categoryContent = self.computeCategoryContents(StoreSorting=True)
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = true
        if Reverse:
            print('\n*--- Quantiles Sorting results in descending order ---*\n')
            prev_c = '>'
            if isReturningHTML:
                prev_c = '&gt;'
                html = '<h2>Sorting results in descending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'
            for c in self.orderedCategoryKeys(Reverse=Reverse):
                cName = self.categories[c]['name']
                if LowerClosed:
                    print(']%s - %s]:' % (prev_c,cName), end=' ')
                    print('\t',categoryContent[c])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">]%s - %s]</td>' % (prev_c,c)
                        catString = str(categoryContent[c])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')
                else:
                    print('[%s - %s[:' % (prev_c,cName), end=' ')
                    print('\t',categoryContent[c])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">[%s - %s[</td>' % (prev_c,c)
                        catString = str(categoryContent[c])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')
                prev_c = cName
        else:
            print('\n*--- Sorting results in ascending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in ascending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'
            cat = [x for x in self.orderedCategoryKeys(Reverse=Reverse)]
            cat.append('<')
            catNames =  [self.categories[x]['name'] for x in self.orderedCategoryKeys(Reverse=Reverse)]                              
            if isReturningHTML:
                catNames.append('&lt;')
            else:
                catNames.append('<')

            for i in range(len(cat)-1):
                if LowerClosed:
                    print('[%s - %s[:' % (catNames[i],catNames[i+1]), end=' ')
                    print('\t',categoryContent[cat[i]])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">]%s - %s]</td>' % (cat[i],cat[i+1])
                        catString = str(categoryContent[cat[i]])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')
                else:
                    print(']%s - %s]:' % (catNames[i],catNames[i+1]), end=' ')
                    print('\t',categoryContent[cat[i]])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">[%s - %s[</td>' % (cat[i],cat[i+1])
                        catString = str(categoryContent[cat[i]])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')

        if isReturningHTML:
            html += '</table>'
            return html

    def showActionCategories(self,action,Debug=False,Comments=True,\
                             Threading=False,nbrOfCPUs=None):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        Med = self.valuationdomain['med']
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,\
                                                     Comments=Debug,\
                                                     Threading=Threading,
                                                     StoreSorting=False,
                                                     nbrOfCPUs=nbrOfCPUs)
        if Debug:
            print(sorting)
        #keys = []
        catKeys = self.orderedCategoryKeys()
        lowLimit = sorting[action][catKeys[0]]['lowLimit']
        notHighLimit = sorting[action][catKeys[-1]]['notHighLimit']
        keys = [catKeys[0],catKeys[-1]]  # action is sorted by default in all categories 
        for c in self.orderedCategoryKeys():
            if sorting[action][c]['categoryMembership'] >= Med:
                if sorting[action][c]['lowLimit'] > Med:
                    lowLimit = sorting[action][c]['lowLimit']
                    keys[0] = c  # the highest lowLimit is remembered
                if sorting[action][c]['notHighLimit'] > Med:
                    notHighLimit = sorting[action][c]['notHighLimit']
                    keys[1] = c  # the highest notHighLimit (lowest HigLimit) is remembered
                if Debug:
                    print(action, c, sorting[action][c],keys)
        credibility = min(lowLimit,notHighLimit)
        if Comments:
            print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                 self.categories[keys[0]]['name'],\
                                 self.categories[keys[1]]['name'],\
                                 action,\
                                 credibility,lowLimit,notHighLimit) )
        return action,\
                keys[0],\
                keys[1],\
                credibility            

    def showActionsSortingResult(self,actionSubset=None,Debug=False):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        if actionSubset == None:
            actions = [x for x in self.actions]
            actions.sort()
        else:
            actions = [x for x in flatten(actionSubset)]
        print('Quantiles sorting result per decision action')
        for x in actions:
            self.showActionCategories(x,Debug=Debug)

    def saveProfilesXMCDA2(self,fileName='temp',category='XMCDA 2.0 format',user='sortinDigraphs Module (RB)',version='saved from Python session',title='Sorting categories in XMCDA-2.0 format.',variant='Rubis',valuationType='bipolar',isStringIO=False,stringNA='NA',comment='produced by saveProfilesXMCDA2()'):
        """
        Save profiles object self in XMCDA 2.0 format.
        """
        import codecs
        if not isStringIO:
            print('*----- saving sorting profiles in XMCDA 2.0 format  -------------*')
        nameExt = fileName+'.xml'
        if isStringIO:
            comment='produced by stringIO()'
            import io
            fo = io.StringIO()
        else:
            #nameExt = fileName+'.xmcda2'
            fo = codecs.open(nameExt,'w',encoding='utf-8')
        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<?xml-stylesheet type="text/xsl" href="xmcda2Rubis.xsl"?>\n')
        fo.write(str('<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2010/XMCDA-2.1.0-Rubis http://leopold-loewenheim.uni.lu/XMCDA2/XMCDA-2.1.0-Rubis.xsd" xmlns:xmcda="http://www.decision-deck.org/2010/XMCDA-2.1.0-Rubis" instanceID="void">\n'))

        # write description
        fo.write('<projectReference id="%s" name="%s">\n' % (fileName,nameExt))
        fo.write('<title>%s</title>\n' % (str(title)) )
        fo.write('<author>%s</author>\n' % (user) )
        fo.write('<version>%s</version>\n' % (version) )
        fo.write('<comment>%s</comment>\n' % (str(comment)) )
        fo.write('</projectReference>\n')


        #  save categories
        categoriesList = [x for x in self.categories]
        categoriesList.sort()
        na = len(categoriesList)
        categories = self.categories
        fo.write('<categories mcdaConcept="%s">\n' % ('categories'))
        fo.write('<description>\n')
        fo.write('<subTitle>Sorting categories.</subTitle>\n')
        fo.write('</description>\n')
        for i in range(na):
            try:
                categoryName = str(categories[categoriesList[i]]['name'])
            except:
                categoryName = categoriesList[i]
            fo.write('<category id="%s" name="%s" mcdaConcept="%s">\n' % (categoriesList[i],categoryName,'sortingCategory'))
            fo.write('<description>\n')
            fo.write('<comment>')
            try:
                fo.write(str(categories[categoriesList[i]]['comment']))
            except:
                fo.write('None')
            fo.write('</comment>\n')
            fo.write('</description>\n')
            fo.write('<type>real</type>\n')
            fo.write('<active>true</active>\n')
            fo.write('</category>\n')
        fo.write('</categories>\n')

        # save criteriaCategoryLimits
        criteriaList = [x for x in self.criteria]
        criteriaList.sort()
        categoriesList = [x for x in self.categories]
        categoriesList.sort()
        criteria = self.criteria
        fo.write('<criteriaCategoryLimits mcdaConcept="categoryProfiles">\n')
        fo.write('<description>\n')
        fo.write('<subTitle>Sorting profiles.</subTitle>\n')
        fo.write('</description>\n')
        for g in criteriaList:
            for c in categoriesList:
                try:
                    criterionName = str(criteria[g]['id'])
                except:
                    criterionName = g
                try:
                    categoryName = str(category[c]['id'])
                except:
                    categoryName = c

                fo.write('<criterionCategoryLimits id="lim_%s_%s" mcdaConcept="%s">\n' % (criterionName,categoryName,'criterionCategoryLimits' ) )
                fo.write('<description>\n')
                fo.write('<comment>%s</comment>\n' % ('No comment') )
                fo.write('<version>%s</version>\n' % ('Rubis k-sorting') )
                fo.write('</description>\n')
                fo.write('<criterionID>%s</criterionID>\n' % (criterionName) )
                fo.write('<categoryID>%s</categoryID>\n' % (categoryName) )
                fo.write('<lowLimit><real>%.2f</real></lowLimit>\n' % (self.criteriaCategoryLimits[g][c]['minimum']) )
                fo.write('<highLimit><real>%.2f</real></highLimit>\n' % (self.criteriaCategoryLimits[g][c]['maximum']) )

                fo.write('</criterionCategoryLimits>\n')
        fo.write('</criteriaCategoryLimits>\n')
        #########################
        fo.write('</xmcda:XMCDA>\n')
        if isStringIO:
            problemText = fo.getvalue()
            fo.close
            return problemText
        else:
            fo.close()
            print('File: ' + nameExt + ' saved !')

    def recodeValuation(self,newMin=-1.0,newMax=1.0,Debug=False):
        """
        Recodes the characteristic valuation domain according
        to the parameters given.

        .. note::

            Default values gives a normalized valuation domain

        """
        from copy import copy, deepcopy
        oldMax = self.valuationdomain['max']
        oldMin = self.valuationdomain['min']
        oldMed = self.valuationdomain['med']

        oldAmplitude = oldMax - oldMin
        if Debug:
            print(oldMin, oldMed, oldMax, oldAmplitude)

        newMin = Decimal(str(newMin))
        newMax = Decimal(str(newMax))
        newMed = Decimal('%.3f' % ((newMax + newMin)/Decimal('2.0')))

        newAmplitude = newMax - newMin
        if Debug:
            print(newMin, newMed, newMax, newAmplitude)

        actions = self.getActionsKeys(withoutProfiles=False)
        oldrelation = copy(self.relation)
        newrelation = {}
        for x in actions:
            newrelation[x] = {}
            for y in actions:
                if oldrelation[x][y] == oldMax:
                    newrelation[x][y] = newMax
                elif oldrelation[x][y] == oldMin:
                    newrelation[x][y] = newMin
                elif oldrelation[x][y] == oldMed:
                    newrelation[x][y] = newMed
                else:
                    newrelation[x][y] = newMin + ((self.relation[x][y] - oldMin)/oldAmplitude)*newAmplitude
                    if Debug:
                        print(x,y,self.relation[x][y],newrelation[x][y])
        # install new values in self
        self.valuationdomain['max'] = newMax
        self.valuationdomain['min'] = newMin
        self.valuationdomain['med'] = newMed
        self.valuationdomain['hasIntegerValuation'] = False

        self.relation = copy(newrelation)

#-------------
        
class QuantilesSortingDigraph(SortingDigraph):
    """
    Specialisation of the root :py:class:`sortingDigraphs.SortingDigraph` class
    for sorting of a large set of alternatives into
    quantiles delimited ordered classes.
      
    .. note::

        The constructor requires a valid PerformanceTableau instance.
        If no number of limiting quantiles is given, then a default profile with the limiting quartiles Q0,Q1,Q2, Q3 and Q4 is used on each criteria.
        By default upper closed limits of categories are supposed to be used in the sorting.

    Example Python3 session:

    >>> from sortingDigraphs import QuantilesSortingDigraph
    >>> from randomPerfTabs import RandomCBPerformanceTableau
    >>> t = RandomCBPerformanceTableau(numberOfActions=7,numberOfCriteria=5,
    ...                                weightDistribution='equiobjectives')
    >>> qs = QuantilesSortingDigraph(t,limitingQuantiles=7)
    >>> qs.showSorting()
    *--- Sorting results in descending order ---*
    ]0.86 - 1.00]: 	 []
    ]0.71 - 0.86]: 	 ['a03']
    ]0.57 - 0.71]: 	 ['a04']
    ]0.43 - 0.57]: 	 ['a04', 'a05', 'a06']
    ]0.29 - 0.43]: 	 ['a01', 'a02', 'a06', 'a07']
    ]0.14 - 0.29]: 	 []
    ]< - 0.14]: 	 []
    >>> qs.showQuantileOrdering()
    ]0.71-0.86] : ['a03']
    ]0.43-0.71] : ['a04']
    ]0.43-0.57] : ['a05']
    ]0.29-0.57] : ['a06']
    ]0.29-0.43] : ['a07', 'a02', 'a01']
    >>> qs.exportGraphViz('quantilesSorting')
    
    .. image:: quantilesSorting.png
       :alt: Example of quantiles sorting digraph
       :width: 400 px
       :align: center
    """
    def __init__(self,argPerfTab=None,\
                 limitingQuantiles=None,\
                 LowerClosed=False,\
                 PrefThresholds=True,\
                 hasNoVeto=False,\
                 outrankingType = "bipolar",\
                 WithSortingRelation=True,\
                 CompleteOutranking = False,\
                 StoreSorting=False,\
                 CopyPerfTab=False,\
                 Threading=False,\
                 tempDir=None,\
                 nbrCores=None,\
                 nbrOfProcesses=None,\
                 Comments=False,
                 Debug=False):
        """
        Constructor for QuantilesSortingBigDigraph instances.

        """
        from time import time
        from copy import copy, deepcopy
        if CopyPerfTab:
            copy2self = deepcopy
        else:
            copy2self = copy
        from decimal import Decimal

        # import the performance tableau
        tt = time()
        if argPerfTab == None:
            print('Error: a valid performance tableau is required!')
##            perfTab = RandomPerformanceTableau(numberOfActions=10,
##                                               numberOfCriteria=13)
        else:
            perfTab = argPerfTab
        # normalize the actions as a dictionary construct
        if isinstance(perfTab.actions,list):
            actions = OrderedDict()
            for x in perfTab.actions:
                actions[x] = {'name': str(x)}
        else:
            actions = copy2self(perfTab.actions)
        actions = actions
        self.actions = actions

        # keep a copy of the original actions set before adding the profiles
        actionsOrig = OrderedDict(actions)
        self.actionsOrig = actionsOrig

        #  normalizing the performance tableau
        normPerfTab = NormalizedPerformanceTableau(perfTab)

        # instantiating the performance tableau part
        criteria = normPerfTab.criteria
        self.criteria = criteria
        self.convertWeight2Decimal()
        evaluation = normPerfTab.evaluation
        self.evaluation = evaluation
        self.convertEvaluation2Decimal()
        self.runTimes = {'dataInput': time()-tt}

        #  compute the limiting quantiles
        t0 = time()
        if isinstance(limitingQuantiles,list):
            self.name = 'sorting_with_given_quantiles'
            newLimitingQuantiles = []
            for x in limitingQuantiles:
                newLimitingQuantiles.append(Decimal(str(x)))
            limitingQuantiles = newLimitingQuantiles
            if Debug:
                print('convert to decimal!',limitingQuantiles)
        else:
            limitingQuantiles = self._computeQuantiles(limitingQuantiles,Debug=Debug)
        self.limitingQuantiles = limitingQuantiles

        if Debug:
            print('limitingQuantiles',self.limitingQuantiles)

        # supposing all criteria scales between 0.0 and 100.0
        # with preference direction = max
        self.LowerClosed = LowerClosed
        lowValue = 0.0
        highValue = 100.00
        categories = OrderedDict()
        k = len(limitingQuantiles)-1
        if LowerClosed:
            for i in range(0,k-1):
                categories[str(i+1)] = {'name':'[%.2f - %.2f['\
                %(limitingQuantiles[i],limitingQuantiles[i+1]),\
                                'order':i+1,\
                                'lowLimit': '[%.2f' % (limitingQuantiles[i]),
                                'highLimit': '%.2f[' % (limitingQuantiles[i+1]),
                                        'quantile': limitingQuantiles[i]}
            categories[str(k)] = {'name':'[%.2f - <['\
                %(limitingQuantiles[k-1]), 'order':k,\
                                  'lowLimit': '[%.2f' % (limitingQuantiles[k-1]),\
                                  'highLimit': '<[',
                                'quantile': limitingQuantiles[k-1] }                 
        else:
            categories[str(1)] = {'name':']< - %.2f]'\
                %(limitingQuantiles[1]), 'order':1,
                    'highLimit': '%.2f]' % (limitingQuantiles[1]),\
                    'lowLimit': ']<',
                    'quantile': limitingQuantiles[1]}                                  
            for i in range(1,k):
                categories[str(i+1)] = {'name':']%.2f - %.2f]'\
                %(limitingQuantiles[i],limitingQuantiles[i+1]), 'order':i+1,
                        'lowLimit': ']%.2f' % (limitingQuantiles[i]),
                        'highLimit': '%.2f]' % (limitingQuantiles[i+1]),
                                        'quantile': limitingQuantiles[i+1]}
        self.categories = categories
        if Debug:
            print('categories',self.categories)
            print('list',list(dict.keys(categories)))

        criteriaCategoryLimits = {}
        criteriaCategoryLimits['LowerClosed'] = LowerClosed
        self.criteriaCategoryLimits = criteriaCategoryLimits
        for g in dict.keys(criteria):
            gQuantiles = self._computeLimitingQuantiles(g,\
                            PrefThresholds=PrefThresholds,Debug=Debug)
##            if Debug:
##                print(g,gQuantiles)
            criteriaCategoryLimits[g] = gQuantiles
        self.criteriaCategoryLimits = criteriaCategoryLimits
        if Debug:
            print('CriteriaCategoryLimits',criteriaCategoryLimits)

        # add the catogory limits to the actions set
        profiles = OrderedDict()
        #profileLimits = set()
        for c in categories:
            if LowerClosed:
                cKey = c+'-m'
            else:
                cKey = c+'-M'
            #profileLimits.add(cKey)
            if LowerClosed:
                actions[cKey] = {'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
                profiles[cKey] = {'category': c, 'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
            else:
                actions[cKey] = {'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
                profiles[cKey] = {'category': c, 'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
            for g in dict.keys(criteria):
                if LowerClosed:
                    evaluation[g][cKey] = Decimal(str(criteriaCategoryLimits[g][int(c)-1]))
                else:
                    evaluation[g][cKey] = Decimal(str(criteriaCategoryLimits[g][int(c)]))

        self.profiles = profiles
        profileLimits = list(profiles.keys())
        #profileLimits.sort()
        self.profileLimits = profileLimits
        
        if Debug:
            print('self.profiles',profiles)
            print('self.profileLimits',profileLimits)
            
        self.runTimes['computeProfiles'] = time() - t0
        
        # construct outranking relation
        t0 = time()
        self.hasNoVeto = hasNoVeto
        minValuation = -100.0
        maxValuation = 100.0
        if CompleteOutranking:
            g = BipolarOutrankingDigraph(normPerfTab,hasNoVeto=hasNoVeto,
                                         Threading=Threading,nbrCores=nbrCores)
            g.recodeValuation(minValuation,maxValuation)
            self.relationOrig = g.relation
            Min = g.valuationdomain['min']
            Max = g.valuationdomain['max']
            self.valuationdomain = g.valuationdomain
        else:
            Min = Decimal(str(minValuation))
            Max = Decimal(str(maxValuation))
        Med = (Max + Min)/Decimal('2.0')
        self.valuationdomain = {'min': Min, 'med':Med ,'max':Max }
        if LowerClosed:
            initial=actionsOrig
            terminal=profiles
        else:
            initial=profiles
            terminal=actionsOrig
        relation = self._constructRelationWithThreading(criteria,
                                                   evaluation,
                                                   initial=initial,
                                                   terminal=terminal,
                                                   hasNoVeto=hasNoVeto,
                                                   hasBipolarVeto=True,
                                                   WithConcordanceRelation=False,
                                                   WithVetoCounts=False,       
                                                    Threading=Threading,
                                                        tempDir=tempDir,
                                                    nbrCores=nbrCores,
                                                    Comments=Comments,
                                                    WithSortingRelation=WithSortingRelation,
                                                    StoreSorting=StoreSorting)

        if WithSortingRelation:
            if LowerClosed:
                for x in dict.keys(actionsOrig):
                    rx = relation[x]
                    for y in dict.keys(actionsOrig):
                        rx[y] = Med
                for x in dict.keys(profiles):
                    relation[x] = {}
                    rx = relation[x]
                    for y in dict.keys(actions):
                        rx[y] = Med
            else:
                for x in dict.keys(actionsOrig):
                    relation[x] = {}
                    rx = relation[x]
                    for y in dict.keys(actionsOrig):
                        rx[y] = Med
                for y in dict.keys(profiles):
                    for x in dict.keys(actions):
                        relation[x][y] = Med
            self.relation = relation
        self.runTimes['computeRelation'] = time() - t0

        # compute weak ordering
        t0 = time()
        if WithSortingRelation:
            if nbrOfProcesses == None:
                nbrOfProcesses = nbrCores

            sortingRelation = self.computeSortingRelation(StoreSorting=StoreSorting,\
                                                          Debug=Debug,Comments=Comments,\
                                                          Threading=Threading,\
                                                          nbrOfCPUs=nbrOfProcesses)
            for x in dict.keys(actionsOrig):
                rx = self.relation[x]
                srx = sortingRelation[x]
                for y in dict.keys(actionsOrig):
                    rx[y] = srx[y]
                    
        self.runTimes['weakOrdering'] = time() - t0
        # reset original action set
        if WithSortingRelation:
            self.actions = actionsOrig
            self.order = len(self.actions)
            self.gamma = self.gammaSets()
            self.notGamma = self.notGammaSets()

        self.runTimes['totalTime'] = time() - tt

    def _constructRelationWithThreading(self,criteria,\
                           evaluation,\
                           initial=None,\
                           terminal=None,\
                           hasNoVeto=False,\
                           hasBipolarVeto=True,\
                           Debug=False,\
                           hasSymmetricThresholds=True,\
                           Threading=False,\
                           tempDir=None,\
                           WithConcordanceRelation=True,\
                           WithVetoCounts=True,\
                            WithSortingRelation=True,\
                            StoreSorting=True,\
                           nbrCores=None,Comments=False):
        """
        Specialization of the corresponding BipolarOutrankingDigraph method
        """
        from multiprocessing import cpu_count
        
        LowerClosed = self.criteriaCategoryLimits['LowerClosed']        

        if not Threading or cpu_count() < 2:
            # set parameters for non threading
            self.nbrThreads = 1
            Min = self.valuationdomain['min']
            Med = self.valuationdomain['med']
            Max = self.valuationdomain['max']
            

            # compute sorting relation
            # !! concordance relation and veto counts need a complex constructor
            if (not hasBipolarVeto) or WithConcordanceRelation or WithVetoCounts:
                constructRelation = self._constructRelation
            else:
                constructRelation = self._constructRelationSimple

            relation = constructRelation(criteria,\
                                    evaluation,\
                                    initial=initial,\
                                    terminal=terminal,\
                                    hasNoVeto=hasNoVeto,\
                                    hasBipolarVeto=hasBipolarVeto,\
                                    WithConcordanceRelation=WithConcordanceRelation,\
                                    WithVetoCounts=WithVetoCounts,\
                                    Debug=Debug,\
                                    hasSymmetricThresholds=hasSymmetricThresholds)
            if WithSortingRelation:
                self.relation = relation

            # compute quantiles sorting result
            if LowerClosed:
                actions = initial
            else:
                actions = terminal
            categories = self.categories.keys()
            sorting = {}
            nq = len(self.limitingQuantiles) - 1
            for x in actions:
                sorting[x] = {}
                for c in categories:
                    sorting[x][c] = {}
                    if LowerClosed:
                        cKey= c+'-m'
                    else:
                        cKey= c+'-M'
                    if LowerClosed:
                        lowLimit = relation[x][cKey]
                        if int(c) < nq:
                            cMaxKey = str(int(c)+1)+'-m'
                            notHighLimit = Max - relation[x][cMaxKey] + Min
                        else:
                            notHighLimit = Max
                    else:
                        if int(c) > 1:
                            cMinKey = str(int(c)-1)+'-M'
                            lowLimit = Max - relation[cMinKey][x] + Min
                        else:
                            lowLimit = Max
                        notHighLimit = relation[cKey][x]
                    categoryMembership = min(lowLimit,notHighLimit)
                    sorting[x][c]['lowLimit'] = lowLimit
                    sorting[x][c]['notHighLimit'] = notHighLimit
                    sorting[x][c]['categoryMembership'] = categoryMembership

            if StoreSorting:
                self.sorting = sorting

            # compute category contents
            categoryContent = {}
            for c in self.orderedCategoryKeys():
                categoryContent[c] = []
                for x in actions:
                    if sorting[x][c]['categoryMembership'] >= self.valuationdomain['med']:
                        categoryContent[c].append(x)
            self.categoryContent = categoryContent

            return relation
            
        ##
        else:  # parallel computation
            from copy import copy, deepcopy
            from io import BytesIO
            from pickle import Pickler, dumps, loads, load
            from multiprocessing import Process, Lock,\
                                        active_children, cpu_count
            #Debug=True
            class myThread(Process):
                def __init__(self, threadID,\
                             InitialSplit, tempDirName,\
                             splitActions,\
                             hasNoVeto, hasBipolarVeto,\
                             hasSymmetricThresholds, Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.InitialSplit = InitialSplit
                    self.workingDirectory = tempDirName
                    self.splitActions = splitActions
                    self.hasNoVeto = hasNoVeto
                    self.hasBipolarVeto = hasBipolarVeto,
                    hasSymmetricThresholds = hasSymmetricThresholds,
                    self.Debug = Debug
                def run(self):
                    from io import BytesIO
                    from pickle import Pickler, dumps, loads
                    from os import chdir
                    from outrankingDigraphs import BipolarOutrankingDigraph
                    chdir(self.workingDirectory)
##                    if Debug:
##                        print("Starting working in %s on thread %s" % (self.workingDirectory, str(self.threadId)))
                    fi = open('dumpSelf.py','rb')
                    digraph = loads(fi.read())
                    fi.close()
                    Min = digraph.valuationdomain['min']
                    Med = digraph.valuationdomain['med']
                    Max = digraph.valuationdomain['max']
                    splitActions = self.splitActions
                    constructRelation = BipolarOutrankingDigraph._constructRelation
                    if self.InitialSplit:
                        initialIn = splitActions
                        terminalIn = digraph.profiles
                    else:
                        initialIn = digraph.profiles
                        terminalIn = splitActions
                    splitRelation = constructRelation(
                                            digraph,digraph.criteria,\
                                            digraph.evaluation,\
                                            initial=initialIn,\
                                            terminal=terminalIn,\
                                            hasNoVeto=hasNoVeto,\
                                            hasBipolarVeto=hasBipolarVeto,\
                                            WithConcordanceRelation=False,\
                                            WithVetoCounts=False,\
                                            #WithSortingRelation=True,\
                                            #StoreSorting=True,\
                                            Debug=False,\
                                            hasSymmetricThresholds=hasSymmetricThresholds)
                    foName = 'splitRelation-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(splitRelation,-1))
                    fo.close()
                    # compute quantiles sorting result
                    LowerClosed = digraph.criteriaCategoryLimits['LowerClosed']
                    nq = len(digraph.limitingQuantiles) - 1
                    categories = digraph.categories.keys()
                    sorting = {}
                    nq = len(digraph.limitingQuantiles) - 1
                    for x in splitActions:
                        sorting[x] = {}
                        for c in categories:
                            sorting[x][c] = {}
                            if LowerClosed:
                                cKey= c+'-m'
                            else:
                                cKey= c+'-M'
                            if LowerClosed:
                                lowLimit = splitRelation[x][cKey]
                                if int(c) < nq:
                                    cMaxKey = str(int(c)+1)+'-m'
                                    notHighLimit = Max - splitRelation[x][cMaxKey] + Min
                                else:
                                    notHighLimit = Max
                            else:
                                if int(c) > 1:
                                    cMinKey = str(int(c)-1)+'-M'
                                    lowLimit = Max - splitRelation[cMinKey][x] + Min
                                else:
                                    lowLimit = Max
                                notHighLimit = splitRelation[cKey][x]
                            categoryMembership = min(lowLimit,notHighLimit)
                            sorting[x][c]['lowLimit'] = lowLimit
                            sorting[x][c]['notHighLimit'] = notHighLimit
                            sorting[x][c]['categoryMembership'] = categoryMembership

                    if StoreSorting:
                        #self.sorting = sorting
                        foName = 'splitSorting-'+str(self.threadID)+'.py'
                        fo = open(foName,'wb')
                        fo.write(dumps(sorting,-1))
                        fo.close()

                    # compute category contents
                    categoryContent = {}
                    for c in digraph.orderedCategoryKeys():
                        categoryContent[c] = []
                        for x in splitActions:
                            if sorting[x][c]['categoryMembership'] >= digraph.valuationdomain['med']:
                                categoryContent[c].append(x)

                    #self.categoryContent = categoryContent
                    foName = 'splitCategoryContent-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(categoryContent,-1))
                    fo.close()
                    
                # .......
             
            if Comments:
                print('Threading ...')
            from tempfile import TemporaryDirectory
            with TemporaryDirectory(dir=tempDir) as tempDirName:
                from copy import copy, deepcopy

                #selfDp = copy(self)
                selfFileName = tempDirName +'/dumpSelf.py'
                if Debug:
                    print('temDirName, selfFileName', tempDirName,selfFileName)
                fo = open(selfFileName,'wb')
                fo.write(dumps(self,-1))
                fo.close()

                if nbrCores == None:
                    nbrCores = cpu_count()
                if Comments:
                    print('Nbr of cpus = ',nbrCores)
                # set number of threads
                self.nbrThreads = nbrCores

                ni = len(initial)
                nt = len(terminal)
                if LowerClosed:
                    n = ni
                    actions2Split = list(initial)
                    InitialSplit = True
                else:
                    n = nt
                    actions2Split = list(terminal)
                    InitialSplit = False
##                if Debug:
##                    print('InitialSplit, actions2Split', InitialSplit, actions2Split)
            
                nit = n//nbrCores
                nbrOfJobs = nbrCores
                if nit*nbrCores < n:
                    nit += 1
                while nit*(nbrOfJobs-1) >= n:
                    nbrOfJobs -= 1
                if Comments:
                    print('nbr of actions to split',n)
                    print('nbr of jobs = ',nbrOfJobs)    
                    print('nbr of splitActions = ',nit)

                relation = {}
                Med = self.valuationdomain['med']
                for x in initial:
                    relation[x] = {}
                    rx = relation[x]
                    for y in terminal:
                        rx[y] = Med
                i = 0
                actionsRemain = set(actions2Split)
                splitActionsList = []
                for j in range(nbrOfJobs):
                    if Comments:
                        print('Thread = %d/%d' % (j+1,nbrOfJobs),end=" ")
                    splitActions=[]
                    for k in range(nit):
                        if j < (nbrOfJobs -1) and i < n:
                            splitActions.append(actions2Split[i])
                        else:
                            splitActions = list(actionsRemain)
                        i += 1
                    if Comments:
                        print('%d' % (len(splitActions)) )
##                    if Debug:
##                        print(splitActions)
                    actionsRemain = actionsRemain - set(splitActions)
##                    if Debug:
##                        print(actionsRemain)
                    splitActionsList.append(splitActions)

                    splitThread = myThread(j,InitialSplit,
                                           tempDirName,splitActions,
                                           hasNoVeto,hasBipolarVeto,
                                           hasSymmetricThresholds,Debug)
                    splitThread.start()
                    
                while active_children() != []:
                    pass

                if Comments:    
                    print('Exiting computing threads')
                sorting = {}
                categoryContent = {}
                relation = {}
                for j in range(len(splitActionsList)):
                    # update category contents
                    fiName = tempDirName+'/splitCategoryContent-'+str(j)+'.py'
                    fi = open(fiName,'rb')
                    splitCategoryContent = loads(fi.read())
                    categoryContent.update(splitCategoryContent)
                    # update sorting result
                    if StoreSorting:
                        fiName = tempDirName+'/splitSorting-'+str(j)+'.py'
                        fi = open(fiName,'rb')
                        splitSorting = loads(fi.read())
                        sorting.update(splitSorting)
                    # update complete sorting relation
                    if WithSortingRelation:
                        splitActions = splitActionsList[j]
    ##                    if Debug:
    ##                        print('splitActions',splitActions)
                        fiName = tempDirName+'/splitRelation-'+str(j)+'.py'
                        fi = open(fiName,'rb')
                        splitRelation = loads(fi.read())
    ##                    if Debug:
    ##                        print('splitRelation',splitRelation)
                        fi.close()
                        #relation update with splitRelation)                    
                        if LowerClosed:
                            #for x,y in product(splitActions,terminal):
                            for x in splitActions:
                                try:
                                    rx = relation[x]
                                except:
                                    relation[x] = {}
                                    rx = relation[x]
                                sprx = splitRelation[x]
                                for y in self.profiles:
                                    rx[y] = sprx[y]
                        else:
                            #for x,y in product(initial,splitActions):
                            for x in self.profiles:
                                try:
                                    rx = relation[x]
                                except KeyError:
                                    relation[x] = {}
                                    rx = relation[x]
                                sprx = splitRelation[x]
                                for y in splitActions:
                                    rx[y] = sprx[y]
                self.categoryContent = categoryContent
                if StoreSorting:
                    self.sorting = sorting
                if WithSortingRelation:
                    return relation

    def showActionCategories(self,action,Debug=False,Comments=True,\
                             Threading=False,nbrOfCPUs=None):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        Med = self.valuationdomain['med']
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,\
                                                     Comments=Debug,\
                                                     Threading=Threading,
                                                     StoreSorting=False,
                                                     nbrOfCPUs=nbrOfCPUs)
        catKeys = self.orderedCategoryKeys()
        keys = [catKeys[0],[catKeys[-1]]]
        lowLimit = sorting[action][catKeys[0]]['lowLimit']
        notHighLimit = sorting[action][catKeys[-1]]['lowLimit']
        for c in self.orderedCategoryKeys():
            if sorting[action][c]['categoryMembership'] >= Med:
                if sorting[action][c]['lowLimit'] > Med:
                    lowLimit = sorting[action][c]['lowLimit']
                    keys[0] = c
                if sorting[action][c]['notHighLimit'] > Med:
                    notHighLimit = sorting[action][c]['notHighLimit']
                    keys[1] = c
                #keys.append(c)
                if Debug:
                    print(action, c, sorting[action][c], keys)
        credibility = min(lowLimit,notHighLimit)
        if Comments:
            print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                 self.categories[keys[0]]['lowLimit'],\
                                 self.categories[keys[-1]]['highLimit'],\
                                 action,\
                                 credibility,lowLimit,notHighLimit) )
        return action,\
                keys[0],\
                keys[1],\
                credibility            

    def showActionsSortingResult(self,actionSubset=None,Debug=False):
        """
        shows the quantiles sorting result all (default) of a subset of the decision actions.
        """
        if actionSubset == None:
            actions = [x for x in self.actions]
            actions.sort()
        else:
            actions = [x for x in flatten(actionSubset)]
        print('Quantiles sorting result per decision action')
        for x in actions:
            self.showActionCategories(x,Debug=Debug)
 

    def showWeakOrder(self,Descending=True):
        """
        Specialisation for QuantilesSortingDigraphs.
        """
        from decimal import Decimal
        from transitiveDigraphs import TransitiveDigraph
        try:
            cC = self.categoryContent
        except:
            cC = self.computeCategoryContents(StoreSorting=True)
        
        if Descending:
            cCKeys = self.orderedCategoryKeys(Reverse = True)
        else:
            cCKeys = self.orderedCategoryKeys(Reverse = False)
        n = len(cC)
        n2 = n//2
        ordering = []
        
        for i in range(n2):
            if i == 0:
                x = cC[cCKeys[i]]
                y = cC[cCKeys[n-i-1]]
                setx = set(x)
                sety = set(y) - setx
            else:
                x = list(set(cC[cCKeys[i]]) - (setx | sety))
                setx = setx | set(x)
                y = list(set(cC[cCKeys[n-i-1]]) - (setx | sety))
                sety = sety | set(y)
            if x != [] or y != []:
                ordering.append( ( (Decimal(str(i+1)),x),(Decimal(str(n-i)),y) ) )
        if 2*n2 < n:
            if n2 == 0:
                x = cC[cCKeys[n2]]
            else:
                x = list(set(cC[cCKeys[n2]]) - (setx | sety))
            ordering.append( ( (Decimal(str(n2+1)),x),(Decimal(str(n2+1)),x) ) )
        
        weakOrdering = {'result':ordering}

        TransitiveDigraph.showTransitiveDigraph(self,weakOrdering)

##        return orderingList

    def _computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                Debug=False):
        """
        Renders the 
        *Parameters*:
            * Descending: listing in *decreasing* (default) or *increasing* quantile order.
            * strategy: ordering in an {'optimistic' | 'pessimistic' | 'average' (default)}
              in the uppest, the lowest or the average potential quantile.
        
        """
        if strategy == None:
            try:
                strategy = self.sortingParameters['strategy']
            except:
                strategy = 'average'
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug)
            if strategy == "optimistic":
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]
            elif strategy == "pessimistic":
                try:
                    actionsCategories[(int(lowCateg),int(highCateg))].append(a)
                except:
                    actionsCategories[(int(lowCateg),int(highCateg))] = [a]
            elif strategy == "average":
                lc = float(lowCateg)
                hc = float(highCateg)
                ac = (lc+hc)/2.0
                try:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))] = [a]
            else:  # optimistic by default
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]      
                
        actionsCategIntervals = []
        for interval in actionsCategories:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        actionsCategIntervals.sort(reverse=Descending)

        return actionsCategIntervals


    def computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                HTML=False,
                                title='Quantiles Preordering',
                                Comments=False,
                                Debug=False):
        """
        *Parameters*:
            * Descending: listing in *decreasing* (default) or *increasing* quantile order.
            * strategy: ordering in an {'optimistic' (default) | 'pessimistic' | 'average'}
              in the uppest, the lowest or the average potential quantile.
        
        """
        from operator import itemgetter
        if strategy == None:
            strategy = 'optimistic'
        if HTML:
            html = '<h1>%s</h1>\n' % title
            html += '<table style="background-color:White;" border="1">\n'
            html += '<tr bgcolor="#9acd32"><th>quantile limits</th>\n'
            html += '<th>%s sorting</th>\n' % strategy
            html += '</tr>\n'
        actionsCategories = {}
        for x in self.actions:
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug)
            #print(a,lowCateg,highCateg,credibility)
            if strategy == "optimistic":
                try:
                    actionsCategories[(highCateg,lowCateg,lowCateg)].append(a)
                except:
                    actionsCategories[(highCateg,lowCateg,lowCateg)] = [a]
            elif strategy == "pessimistic":
                try:
                    actionsCategories[(lowCateg,highCateg,lowCateg)].append(a)
                except:
                    actionsCategories[(lowCateg,highCateg,lowCateg)] = [a]
            elif strategy == "average":
                lc = float(lowCateg)
                hc = float(highCateg)
                ac = (lc+hc)/2.0
                try:
                    actionsCategories[(ac,highCateg,lowCateg)].append(a)
                except:
                    actionsCategories[(ac,highCateg,lowCateg)] = [a]
            else:  # optimistic by default
                try:
                    actionsCategories[(highCateg,lowCateg,lowCateg)].append(a)
                except:
                    actionsCategories[(highCateg,lowCateg,lowCateg)] = [a]      
                
        #actionsCategIntervals.sort(reverse=Descending)
        actionsCategoriesKeys = [key for key in actionsCategories]
        actionsCategoriesKeys = sorted(actionsCategoriesKeys,key=itemgetter(0,1,2), reverse=True)

        actionsCategIntervals = []
        for interval in actionsCategoriesKeys:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        
        weakOrdering = []
        for item in actionsCategIntervals:
            #print(item)
            if Comments:
                if strategy == "optimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><tdbgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])                            
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                elif strategy == "pessimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])

                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )                   
                elif strategy == "average":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
            weakOrdering.append(item[1])
        if HTML:
            html += '</table>'
            return html
        else:
            return weakOrdering

    def showQuantileOrdering(self,strategy=None):
        """
        Dummy show method for the commenting computeQuantileOrdering() method.
        """
        self.computeQuantileOrdering(strategy=strategy,Comments=True)


    def computeWeakOrder(self,Descending=True,Debug=False):
        """
        Specialisation for QuantilesSortingDigraphs.
        """
        from decimal import Decimal
        try:
            cC = self.categoryContent
        except:
            cC = self.computeCategoryContents(StoreSorting=True)
        if Debug:
            print(cC)
        if Descending:
            cCKeys = self.orderedCategoryKeys(Reverse = True)
        else:
            cCKeys = self.orderedCategoryKeys(Reverse = False)
        if Debug:
            print('cCKeys',cCKeys)
        n = len(cC)
        n2 = n//2
        if Debug:
            print('n,n2',n,n2)
        ordering = []
        
        for i in range(n2):
            if i == 0:
                x = cC[cCKeys[i]]
                y = cC[cCKeys[n-i-1]]
                setx = set(x)
                sety = set(y) - setx
            else:
                x = list(set(cC[cCKeys[i]]) - (setx | sety))
                setx = setx | set(x)
                y = list(set(cC[cCKeys[n-i-1]]) - (setx | sety))
                sety = sety | set(y)
            if Debug:
                print('i,x,y,setx,sety',i,x,y,setx,sety)
            if x != [] or y != []:
                ordering.append( ( (Decimal(str(i+1)),x),(Decimal(str(n-i)),y) ))
            if Debug:
                print(i, ( (Decimal(str(i+1)),x),(Decimal(str(n-i)),y) ) )
        if 2*n2 < n:
            if n2 == 0:
                x = cC[cCKeys[n2]]
            else:
                x = list(set(cC[cCKeys[n2]]) - (setx | sety))
            ordering.append( ( (Decimal(str(n2+1)),x),(Decimal(str(n2+1)),[]) ) )
            if Debug:
                print('median term',( (Decimal(str(n2+1)),x),(Decimal(str(n2+1)),[]) ))
        if Debug:
            print(ordering)
        
        orderingList = []
        n = len(ordering)
        for i in range(n):
            x = ordering[i][0][1]
            if x != []:
                orderingList.append(x)
        for i in range(n):
            y = ordering[n-i-1][1][1]
            if y != []:
                orderingList.append(y)
        return orderingList

    def showOrderedRelationTable(self,direction="decreasing"):
        """
        Showing the relation table in decreasing (default) or increasing order.
        """
        if direction == "decreasing":
            Descending = True
        else:
            Descending = False

        weakOrdering = self.computeWeakOrder(Descending)
        
        actionsList = []
        for eq in weakOrdering:
            #print(eq)
            eq.sort()
            for x in eq:
                actionsList.append(x)
        if len(actionsList) != len(self.actions):
            print('Error !: missing action(s) %s in ordered table.')
            
        Digraph.showRelationTable(self,actionsSubset=actionsList,\
                                relation=self.relation,\
                                Sorted=False,\
                                ReflexiveTerms=False)
        

    def _computeQuantiles(self,x,Debug=False):
        """
        renders the limiting quantiles
        """
        from math import floor
        if isinstance(x,int):
            n = x
        elif x == None:
            n = 4
        elif x == 'bitiles':
            n = 2
        elif x == 'tritiles':
            n = 3
        elif x == 'quartiles':
            n = 4
        elif x == 'quintiles':
            n = 5
        elif x == 'sextiles':
            n = 6
        elif x == 'septiles':
            n = 7
        elif x == 'octiles':
            n = 8
        elif x == 'deciles':
            n = 10
        elif x == 'dodeciles':
            n = 20
        elif x == 'centiles':
            n = 100
        elif x == 'automatic':
            pth = [5]
            for g in self.criteria:
                try:
                    pref = self.criteria[g]['thresholds']['ind'][0] + \
                           (self.criteria[g]['thresholds']['ind'][1]*Decimal('100'))
                    pth.append(pref)
                except:
                    pass
            amp = max(Decimal('1'),min(pth))
            n = int(floor(Decimal('100')/amp))
            if Debug:
                print('Detected preference thresholds = ',pth)
                print('amplitude, n',amp,n)

        limitingQuantiles = []
        for i in range(n+1):
            limitingQuantiles.append( Decimal(str(i)) / Decimal(str(n)) )
        self.name = 'sorting_with_%d-tile_limits' % n
        return limitingQuantiles
                                         
    def _computeLimitingQuantiles(self,g,Debug=False,PrefThresholds=True):
        """
        Renders the list of limiting quantiles on criteria g
        """
        from math import floor
        from copy import copy, deepcopy
        LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        gValues = []
        for x in self.actionsOrig:
            if Debug:
                print('g,x,evaluation[g][x]',g,x,self.evaluation[g][x])
            if self.evaluation[g][x] != Decimal('-999'):
                gValues.append(self.evaluation[g][x])
        gValues.sort()
        if PrefThresholds:
            try:
                gPrefThrCst = self.criteria[g]['thresholds']['pref'][0]
                gPrefThrSlope = self.criteria[g]['thresholds']['pref'][1]
            except:
                gPrefThrCst = Decimal('0')
                gPrefThrSlope = Decimal('0')            
        n = len(gValues)
        if Debug:
            print('g,n,gValues',g,n,gValues)
##        if n > 0:
##        nf = Decimal(str(n+1))
        nf = Decimal(str(n))
        limitingQuantiles = copy(self.limitingQuantiles)
        limitingQuantiles.sort()
        if Debug:
            print(limitingQuantiles)
        if LowerClosed:
            limitingQuantiles = limitingQuantiles[:-1]
        else:
            limitingQuantiles = limitingQuantiles[1:]
        if Debug:
            print(limitingQuantiles)
        # computing the quantiles on criterion g
        gQuantiles = []
        if LowerClosed:
            # we ignore the 1.00 quantile and replace it with +infty
            for q in self.limitingQuantiles:
                r = (Decimal(str(nf)) * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq < (n-1):
                    quantile = gValues[rq]\
                        + ((r-Decimal(str(rq)))*(gValues[rq+1]-gValues[rq]))
                    if rq > 0 and PrefThresholds:
                        quantile += gPrefThrCst + quantile*gPrefThrSlope
                else :
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        quantile = Decimal('100.0')
                    else:
                        quantile = Decimal('200.0')
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)               

        else:  # upper closed categories
            # we ignore the quantile 0.0 and replace it with -\infty            
            for q in self.limitingQuantiles:
                r = (Decimal(str(nf)) * q)
                rq = int(floor(r))
                if Debug:
                    print('r,rq',r,rq, end=' ')
                if rq == 0:
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        quantile = Decimal('-200.0')
                    else:
                        quantile = Decimal('-100.0')
                elif rq < (n-1):
                    quantile = gValues[rq]\
                        + ((r-Decimal(str(rq)))*(gValues[rq+1]-gValues[rq]))
                    if PrefThresholds:
                        quantile -= gPrefThrCst - quantile*gPrefThrSlope
                else:
                    if n > 0:
                        quantile = gValues[n-1]
                    else:
                        if self.criteria[g]['preferenceDirection'] == 'min':
                            quantile = Decimal('-200.0')
                        else:
                            quantile = Decimal('-100.0')     
                if Debug:
                    print('quantile',quantile)
                gQuantiles.append(quantile)
##        else:
##            gQuantiles = []
        if Debug:
            print(g,LowerClosed,self.criteria[g]['preferenceDirection'],gQuantiles)
        return gQuantiles

    def getActionsKeys(self,action=None,withoutProfiles=True):
        """
        extract normal actions keys()
        """
        profiles = set([x for x in list(self.profiles.keys())])
        if action == None:
            actionsExt = set([x for x in list(self.actions.keys())])
            if withoutProfiles:
                return actionsExt - profiles
            else:
                return actionsExt | profiles
        else:
            return set([action])           

    def computeCategoryContents(self,Reverse=False,Comments=False,StoreSorting=True,\
                                Threading=False,nbrOfCPUs=None):
        """
        Computes the sorting results per category.
        """
        actions = list(self.getActionsKeys())
        actions.sort()
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(Comments=Comments,\
                                                     StoreSorting=StoreSorting,\
                                                     Threading=Threading,\
                                                     nbrOfCPUs=nbrOfCPUs)

        categoryContent = {}
        for c in self.orderedCategoryKeys(Reverse=Reverse):
            categoryContent[c] = []
            for x in actions:
                if sorting[x][c]['categoryMembership'] >= self.valuationdomain['med']:
                    categoryContent[c].append(x)
        
        return categoryContent

    def computeSortingCharacteristics(self, action=None,Comments=False,\
                                      StoreSorting=False,Debug=False,\
                                        Threading=False, nbrOfCPUs=None):
        """
        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "action x in A belongs to category c in C",
        ie x outranks low category limit and does not outrank
        the high category limit.
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        try:
            return self.sorting
        except:
            pass
        if action != None:
            storeSorting = False
        actions = list(self.getActionsKeys(action))
        na = len(actions)
##        if Debug:
##            print(actions)
            
        #categories = list(self.orderedCategoryKeys())
        categories = list(self.categories.keys())
        selfRelation = self.relation
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True
        if Threading and action==None:
            from multiprocessing import Process, active_children
            from pickle import dumps, loads, load
            from os import cpu_count
            from time import time
##            if Comments:
##                self.Debug = True
            class myThread(Process):
                def __init__(self, threadID, tempDirName,
                             nq, Min, Max, LowerClosed, Debug):
                    Process.__init__(self)
                    self.threadID = threadID
                    self.workingDirectory = tempDirName
                    #self.actions = actions
                    self.nq = nq
                    self.Min = Min
                    self.Max = Max
                    self.LowerClosed = LowerClosed
                    self.Debug = Debug
                def run(self):
                    from pickle import dumps, loads
                    from os import chdir
                    chdir(self.workingDirectory)
##                    if self.Debug:
##                        print("Starting working in %s on %s" % (self.workingDirectory, str(self.threadID)))
##                        print('actions,catKeys',self.actions,self.catKeys)
                    fi = open('dumpSelfRelation.py','rb')
                    #context = loads(fi.read())
                    relation = loads(fi.read())
                    fi.close()
                    fi = open('dumpCategories.py','rb')
                    #context = loads(fi.read())
                    catKeys = loads(fi.read())
                    fi.close()
                    fi = open('dumpActions%d.py' % self.threadID,'rb')
                    #context = loads(fi.read())
                    actions = loads(fi.read())
                    fi.close()
##                    Min = context.valuationdomain['min']
##                    Max = context.valuationdomain['max']
                    Min = self.Min
                    Max = self.Max
                    LowerClosed = self.LowerClosed
                    sorting = {}
                    nq = self.nq
                    #nq = len(context.limitingQuantiles) - 1
                    #actions = self.actions
                    #catKeys = self.catKeys
                    #relation = context.relation
                    for x in actions:
                        sorting[x] = {}
                        sorx = sorting[x]
                        for c in catKeys:
                            sorx[c] = {}
                            if LowerClosed:
                                cKey= c+'-m'
                            else:
                                cKey= c+'-M'
                            if LowerClosed:
                                lowLimit = relation[x][cKey]
                                if int(c) < nq:
                                    cMaxKey = str(int(c)+1)+'-m'
                                    notHighLimit = Max - relation[x][cMaxKey] + Min
                                else:
                                    notHighLimit = Max
                            else:
                                if int(c) > 1:
                                    cMinKey = str(int(c)-1)+'-M'
                                    lowLimit = Max - relation[cMinKey][x] + Min
                                else:
                                    lowLimit = Max
                                notHighLimit = relation[cKey][x]
                            if Debug:
                                print('%s in %s: low = %.2f, high = %.2f' % \
                                      (x, c,lowLimit,notHighLimit), end=' ')
                            categoryMembership = min(lowLimit,notHighLimit)
                            sorx[c]['lowLimit'] = lowLimit
                            sorx[c]['notHighLimit'] = notHighLimit
                            sorx[c]['categoryMembership'] = categoryMembership
##                            if self.Debug:
##                                print('\t %.2f \t %.2f \t %.2f\n' % (sorting[x][c]['lowLimit'],\
##                                   sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
##                        if self.Debug:
##                            print(sorting[x])
                    foName = 'sorting-'+str(self.threadID)+'.py'
                    fo = open(foName,'wb')
                    fo.write(dumps(sorting,-1))
                    fo.close()
            if Comments:
                print('Threaded computing of sorting characteristics ...')        
            from tempfile import TemporaryDirectory,mkdtemp
            tempDirName = mkdtemp()
            td = time()
            selfFileName = tempDirName +'/dumpSelfRelation.py'
##            if Debug:
##                print('temDirName, selfFileName', tempDirName,selfFileName)
            fo = open(selfFileName,'wb')
            pd = dumps(selfRelation,-1)
            fo.write(pd)
            fo.close()
            selfFileName = tempDirName +'/dumpCategories.py'
##            if Debug:
##                print('temDirName, selfFileName', tempDirName,selfFileName)
            fo = open(selfFileName,'wb')
            pd = dumps(categories,-1)
            fo.write(pd)
            fo.close()            
            if nbrOfCPUs == None:
                nbrOfCPUs = cpu_count()-1
            if Comments:
                print('Dump relation: %.5f' % (time()-td))
                print('Nbr of actions',na)
                
            
            nbrOfJobs = na//nbrOfCPUs
            if nbrOfJobs*nbrOfCPUs < na:
                nbrOfJobs += 1
            if Comments:
                print('Nbr of threads = ',nbrOfCPUs)
                print('Nbr of jobs/thread',nbrOfJobs)
            nbrOfThreads = 0
            nq = len(self.limitingQuantiles) -1
            Max = self.valuationdomain['max']
            Min = self.valuationdomain['min']
            for j in range(nbrOfCPUs):
                if Comments:
                    print('thread = %d/%d' % (j+1,nbrOfCPUs),end="...")
                start= j*nbrOfJobs
                if (j+1)*nbrOfJobs < na:
                    stop = (j+1)*nbrOfJobs
                else:
                    stop = na
                thActions = actions[start:stop]
##                if Debug:
##                    print(thActions)
                if thActions != []:
                    selfFileName = tempDirName +'/dumpActions%d.py' % j
                    fo = open(selfFileName,'wb')
                    pd = dumps(thActions,-1)
                    fo.write(pd)
                    fo.close()            
                    process = myThread(j,tempDirName,nq,Min,Max,
                                       LowerClosed,Debug)
                    process.start()
                    nbrOfThreads += 1
            while active_children() != []:
                pass
                #sleep(1)
            if Comments:
                print('Exit %d threads' % nbrOfThreads)
            sorting = {}
            for th in range(nbrOfThreads):
##                if Debug:
##                    print('job',th)
                fiName = tempDirName+'/sorting-'+str(th)+'.py'
                fi = open(fiName,'rb')
                sortingThread = loads(fi.read())
##                if Debug:
##                    print('sortingThread',sortingThread)
                sorting.update(sortingThread)
        # end of Threading
        else: # with out Threading 
            sorting = {}
            nq = len(self.limitingQuantiles) - 1
            for x in actions:
                sorting[x] = {}
                for c in categories:
                    sorting[x][c] = {}
                    if LowerClosed:
                        cKey= c+'-m'
                    else:
                        cKey= c+'-M'
                    if LowerClosed:
                        lowLimit = selfRelation[x][cKey]
                        if int(c) < nq:
                            cMaxKey = str(int(c)+1)+'-m'
                            notHighLimit = Max - selfRelation[x][cMaxKey] + Min
                        else:
                            notHighLimit = Max
                    else:
                        if int(c) > 1:
                            cMinKey = str(int(c)-1)+'-M'
                            lowLimit = Max - selfRelation[cMinKey][x] + Min
                        else:
                            lowLimit = Max
                        notHighLimit = selfRelation[cKey][x]
                    categoryMembership = min(lowLimit,notHighLimit)
                    sorting[x][c]['lowLimit'] = lowLimit
                    sorting[x][c]['notHighLimit'] = notHighLimit
                    sorting[x][c]['categoryMembership'] = categoryMembership

##                    if Debug:
##                        print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
        if StoreSorting:
            self.sorting = sorting
        return sorting

    def _computeSortingCharacteristicsOld(self, action=None, Comments=False):
        """
        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "action x in A belongs to category c in C",
        ie x outranks low category limit and does not outrank
        the high category limit.
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        actions = self.getActionsKeys(action)
            
        categories = self.orderedCategoryKeys()

        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True

        if Comments:
            if LowerClosed:
                print('x  in  K_k\t r(x >= m_k)\t r(x < M_k)\t r(x in K_k)')
            else:
                print('x  in  K_k\t r(m_k < x)\t r(M_k >= x)\t r(x in K_k)')

        sorting = {}
        nq = len(self.limitingQuantiles) - 1
        for x in actions:
            sorting[x] = {}
            for c in categories:
                sorting[x][c] = {}
                if LowerClosed:
                    cKey= c+'-m'
                else:
                    cKey= c+'-M'
                if LowerClosed:
                    lowLimit = self.relation[x][cKey]
                    if int(c) < nq:
                        cMaxKey = str(int(c)+1)+'-m'
                        notHighLimit = Max - self.relation[x][cMaxKey] + Min
                    else:
                        notHighLimit = Max
                else:
                    if int(c) > 1:
                        cMinKey = str(int(c)-1)+'-M'
                        lowLimit = Max - self.relation[cMinKey][x] + Min
                    else:
                        lowLimit = Max
                    notHighLimit = self.relation[cKey][x]
                #if Comments:
                #    print('%s in %s: low = %.2f, high = %.2f' % \
                #          (x, c,lowLimit,notHighLimit), end=' ')
                if Comments:
                    print('%s in %s - %s\t' % (x, self.categories[c]['lowLimit'],self.categories[c]['highLimit'],), end=' ')
                categoryMembership = min(lowLimit,notHighLimit)
                sorting[x][c]['lowLimit'] = lowLimit
                sorting[x][c]['notHighLimit'] = notHighLimit
                sorting[x][c]['categoryMembership'] = categoryMembership

                if Comments:
                    #print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
                    print('%.2f\t\t %.2f\t\t %.2f\n' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))

        return sorting

    def showSortingCharacteristics(self, action=None):
        """
        Renders a bipolar-valued bi-dictionary relation
        representing the degree of credibility of the
        assertion that "action x in A belongs to category c in C",
        ie x outranks low category limit and does not outrank
        the high category limit.
        """
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,StoreSorting=False)

        actions = self.getActionsKeys(action)
            
        categories = self.orderedCategoryKeys()

        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True
        if LowerClosed:
            print('x  in  K_k\t r(x >= m_k)\t r(x < M_k)\t r(x in K_k)')
        else:
            print('x  in  K_k\t r(m_k < x)\t r(M_k >= x)\t r(x in K_k)')

        for x in actions:
            for c in categories:
                print('%s in %s - %s\t' % (x, self.categories[c]['lowLimit'],\
                        self.categories[c]['highLimit'],), end=' ')
                print('%.2f\t\t %.2f\t\t %.2f' %\
                      (sorting[x][c]['lowLimit'],\
                       sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
            print()


    def showHTMLQuantileOrdering(self,title='Quantiles Preordering',Descending=True,strategy='average'):
        """
        Shows the html version of the quantile preordering in a browser window.

        The ordring strategy is either:
            * **average** (default), following the averag of the upper and lower quantile limits,
            * **optimistic**, following the upper quantile limits (default),
            * **pessimistic**, following the lower quantile limits.
            
        """
        import webbrowser
        fileName = '/tmp/preOrdering.html'
        fo = open(fileName,'w')
        fo.write(self.computeQuantileOrdering(Descending=Descending,
                                              strategy=strategy,
                                              HTML=True,
                                              title=title,
                                              Comments=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)


    def showHTMLSorting(self,Reverse=True):
        """
        shows the html version of the sorting result in a browser window.
        """
        import webbrowser
        fileName = '/tmp/sorting.html'
        fo = open(fileName,'w')
        fo.write(self.showSorting(Reverse=Reverse,isReturningHTML=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)


    def showSorting(self,Reverse=True,isReturningHTML=False,Debug=False):
        """
        Shows sorting results in decreasing or increasing (Reverse=False)
        order of the categories. If isReturningHTML is True (default = False)
        the method returns a htlm table with the sorting result.
        
        """
        #from string import replace
        from copy import copy, deepcopy

        try:
            categoryContent = self.categoryContent
        except:
            categoryContent = self.computeCategoryContents(StoreSorting=True)

        categoryKeys = self.orderedCategoryKeys(Reverse=Reverse)
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True

        if Reverse:
            print('\n*--- Sorting results in descending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in descending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'
        else:
            print('\n*--- Sorting results in ascending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in ascending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'

        for c in categoryKeys:
            print('%s:' % (self.categories[c]['name']), end=' ')
            print('\t',categoryContent[c])
            if isReturningHTML:
                #html += '<tr><td bgcolor="#FFF79B">[%s - %s[</td>' % (limprevc,limc)
                html += '<tr><td bgcolor="#FFF79B">%s</td>' % (self.categories[c]['name'])
                catString = str(categoryContent[c])
                html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')

        if isReturningHTML:
            html += '</table>'
            return html

    def computeSortingRelation(self,categoryContents=None,Debug=False,StoreSorting=True,
                               Threading=False,nbrOfCPUs=None,Comments=False):
        """
        constructs a bipolar sorting relation using the category contents.
        """
        try:
            categoryContents = self.categoryContent
        except:
            pass
        if categoryContents == None:
            categoryContents = self.computeCategoryContents(StoreSorting=StoreSorting,\
                                Threading=Threading,nbrOfCPUs=nbrOfCPUs,Comments=Comments)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        actions = [x for x in self.actionsOrig]
        currActions = set(actions)
        sortingRelation = {}
        for x in actions:
            sortingRelation[x] = {}
            for y in actions:
                sortingRelation[x][y] = Med
                
        if Debug:
            print('categoryContents',categoryContents)
        #for i in categoryKeys:
        for c in self.categories.keys():
            ibch = set(categoryContents[c])
            ribch = set(currActions) - ibch
            if Debug:
                print('ibch,ribch',ibch,ribch)
            for x in ibch:
                for y in ibch:
                    sortingRelation[x][y] = Med
                    sortingRelation[y][x] = Med
                for y in ribch:
                    sortingRelation[x][y] = Min
                    sortingRelation[y][x] = Max
            currActions = currActions - ibch
        return sortingRelation

##############################################################333333
#-------------
from performanceQuantiles import PerformanceQuantiles  
class NormedQuantilesRatingDigraph(QuantilesSortingDigraph,PerformanceQuantiles):
    """
    Specialisation of the root :py:class:`sortingDigraphs.SortingDigraph` class
    for absolute rating of a new set of decision actions with
    normed performance quantiles gathered from historical data.
      
    .. note::

        The constructor requires a valid
        :py:class:`performanceQuantiles.PerformanceQuantiles` instance.

    Example Python session:
        >>> from sortingDigraphs import *
        >>> # historical data
        >>> from randomPerfTabs import RandomCBPerformanceTableau
        >>> nbrActions=1000
        >>> nbrCrit = 13
        >>> seed = 100
        >>> tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,numberOfCriteria=nbrCrit,seed=seed)
        >>> pq = PerformanceQuantiles(tp,numberOfBins='deciles',LowerClosed=True,Debug=False)
        >>> # new incoming decision actions of the same kind
        >>> from randomPerfTabs import RandomCBPerformanceGenerator as PerfTabGenerator
        >>> tpg = PerfTabGenerator(tp,instanceCounter=0,seed=seed)
        >>> newActions = tpg.randomActions(10)
        >>> # rating the new set of decision actions after
        >>> # updating the historical performance quantiles
        >>> pq.updateQuantiles(newActions,historySize=None)
        >>> nqr = NormedQuantilesRatingDigraph(pq,newActions)
        >>> # inspecting the rating result
        >>> nqr.showQuantilesRating()
        *-------- Normed quantiles rating result ---------
        [0.60 - 0.70[ ['a01']
        [0.50 - 0.60[ ['a07', 'a10', 'a02', 'a08', 'a09']
        [0.40 - 0.50[ ['a03', 'a06', 'a05']
        [0.30 - 0.40[ ['a04']
        >>> nqr.showHTMLRatingHeatmap(pageTitle='Heatmap of Quantiles Rating')

    .. image:: heatMap3.png
        :alt: usage example of Normed Quantiles Rating Digraph
        :width: 500 px
        :align: center

    """

    def __init__(self,argPerfQuantiles=None,newData=None,\
                 quantiles=None,\
                 hasNoVeto=False,\
                 #PrefThresholds=False,\
                 valuationScale=(-1,1),\
                 rankingRule='best',\
                 WithSorting=False,\
                 Threading=False,\
                 tempDir=None,\
                 nbrOfCPUs=None,\
                 Comments=False,
                 Debug=False):
        
        # constructor for incremental rating agents
        from copy import copy,deepcopy        
        from time import time
        from decimal import Decimal

        # set Debug status
##        if Debug:
##            self.Debug = Debug
        # import the performance quantiles
        self.runTimes = {}
        tt = time()
        if argPerfQuantiles == None:
            print('Error: valid performance quantiles are required!')

        else:
            perfQuantiles = argPerfQuantiles

        # instantiating the performance quantiles part
        try:
            self.objectives = deepcopy(perfQuantiles.objectives)
        except:
            pass
        self.criteria = deepcopy(perfQuantiles.criteria)
        self.LowerClosed = perfQuantiles.LowerClosed
        self.quantilesFrequencies = deepcopy(perfQuantiles.quantilesFrequencies)
        self.limitingQuantiles = deepcopy(perfQuantiles.limitingQuantiles)
        self.historySizes = deepcopy(perfQuantiles.historySizes)
        self.cdf = deepcopy(perfQuantiles.cdf)
        self.name = 'normedRatingDigraph'
        # import the actions to rate
        if newData != None:
            try:  # randomActions format {'actions': .., 'evaluation':..}
                self.newActions = newData['actions']
                self.evaluation = newData['evaluation']
            except:
                try:  #  randomPerformanceTableau format
                    self.newActions = deepcopy(newData.actions)
                    self.evaluation = deepcopy(newData.evaluation)
                except:
                    print('Error !!!: valid new Actions or valid new PerformanceTableau required')
        else:
            print('Error !!!: newly observed decision actions with performance evaluations are required !!')
            return
        
        self.runTimes['dataInput'] = time()-tt
        
        if Debug:
            print('new actions',self.newActions)
            print('new evaluations',self.evaluation)
            print('Quantiles frequencies: ', self.quantilesFrequencies)
            print('limitingQuantiles',self.limitingQuantiles)
            print()

        # instantiate rating categories
        t0 = time()

        # convertWeights to positive
##        from perfTabs import PerformanceTableau
##        PerformanceTableau.convertWeights2Positive(self)        

        # check if new quantile limits should be interpolated
        if quantiles != None:
            oldFreq = self.quantilesFrequencies
            newFreq = self._computeQuantilesFrequencies(quantiles)
            newLimitingQuantiles = {}
            for g in self.criteria:
                newLimitingQuantiles[g] = []
            for p in newFreq:
                newQuantiles = self.computeQuantileProfile(p,oldFreq)
                for g in self.criteria:
                    newLimitingQuantiles[g].append(newQuantiles[g])
            self.limitingQuantiles = newLimitingQuantiles
            self.quantilesFrequencies = newFreq
            
        quantFreq = self.quantilesFrequencies
        limitingQuantiles = self.limitingQuantiles

        if Debug:
            print(quantFreq)
            print(limitingQuantiles)
            
        LowerClosed = self.LowerClosed
        categories = OrderedDict()
        k = len(quantFreq)-1
        if LowerClosed:
            for i in range(0,k-1):
                categories[str(i+1)] = {'name':'[%.2f - %.2f['\
                %(quantFreq[i],quantFreq[i+1]),\
                                'order':i+1,\
                                'lowLimit': '[%.2f' % (quantFreq[i]),
                                'highLimit': '%.2f[' % (quantFreq[i+1]),
                                        'quantile': quantFreq[i]}
            categories[str(k)] = {'name':'[%.2f - <['\
                %(quantFreq[k-1]), 'order':k,\
                                  'lowLimit': '[%.2f' % (quantFreq[k-1]),\
                                  'highLimit': '<[',
                                'quantile': quantFreq[k-1] }                 
        else:
            categories[str(1)] = {'name':']< - %.2f]'\
                %(quantFreq[1]), 'order':1,
                    'highLimit': '%.2f]' % (quantFreq[1]),\
                    'lowLimit': ']<',
                    'quantile': quantFreq[1]}                                  
            for i in range(1,k):
                categories[str(i+1)] = {'name':']%.2f - %.2f]'\
                %(quantFreq[i],quantFreq[i+1]), 'order':i+1,
                        'lowLimit': ']%.2f' % (quantFreq[i]),
                        'highLimit': '%.2f]' % (quantFreq[i+1]),
                                        'quantile': quantFreq[i+1]}
        self.categories = categories
        self.runTimes['categories'] = time()-t0
##
        if Debug:
            print('categories',self.categories)
            print('list',list(dict.keys(categories)))

        # instantiate criteria category limits
        t0 = time()
        criteria = self.criteria
        self.criteriaCategoryLimits = {}
        self.criteriaCategoryLimits['LowerClosed'] = LowerClosed
        #self.criteriaCategoryLimits = criteriaCategoryLimits
        for g in criteria:
            self.criteriaCategoryLimits[g] = limitingQuantiles[g]
            gQuantiles = self._computeLimitingQuantiles(g,\
                            #PrefThresholds=PrefThresholds,\
                            Debug=Debug)
            self.criteriaCategoryLimits[g] = gQuantiles
        if Debug:
            print('CriteriaCategoryLimits',self.criteriaCategoryLimits)

        # set the category limits type (LowerClosed = True is default)
        self.criteriaCategoryLimits['LowerClosed'] = self.LowerClosed
        criteriaCategoryLimits = self.criteriaCategoryLimits

        # add the profiles, ie catogory limits, to the actions set
        profiles = OrderedDict()
        for c in categories:
            if LowerClosed:
                cKey = 'm'+c
            else:
                cKey = 'M'+c
            if LowerClosed:
                profiles[cKey] = {'category': c, 'name': categories[c]['lowLimit'] + ' -',\
                                  'comment': 'Inferior or equal limits for category membership assessment'}
            else:
                profiles[cKey] = {'category': c, 'name': '- ' + categories[c]['highLimit'],\
                                  'comment': 'Lower or equal limits for category membership assessment'}
            for g in criteria:
                if LowerClosed:
                    self.evaluation[g][cKey] = Decimal(str(self.criteriaCategoryLimits[g][int(c)-1]))
                else:
                    self.evaluation[g][cKey] = Decimal(str(self.criteriaCategoryLimits[g][int(c)]))

        self.profiles = profiles
        profileLimits = list(profiles.keys())
        self.profileLimits = profileLimits
        
        if Debug:
            print('self.profiles',profiles)
            print('self.profileLimits',profileLimits)
            
        self.runTimes['profiles'] = time() - t0
        
        # construct outranking relation
        t0 = time()
        if Threading:
            self.nbrThreads = nbrOfCPUs
        self.hasNoVeto = hasNoVeto
        minValuation = valuationScale[0]
        maxValuation = valuationScale[1]
        # construct the corresponding perfTab
        perfTab = PerformanceTableau(isEmpty=True)
        perfTab.actions = deepcopy(self.newActions)
        perfTab.actions.update(self.profiles)
        perfTab.criteria = self.criteria
        perfTab.evaluation = deepcopy(self.evaluation)
        
        if Debug:
            perfTab.showActions()
            perfTab.showCriteria()
            perfTab.showPerformanceTableau()
        
        g = BipolarOutrankingDigraph(perfTab,hasNoVeto=hasNoVeto,Normalized=True,
                                     Threading=Threading,nbrCores=nbrOfCPUs)
        g.recodeValuation(minValuation,maxValuation)
        self.actions = g.actions
        self.completeRelation = g.relation
        self.relation = g.relation
        try:
            self.concordanceRelation = g.concordanceRelation
            self.largeDifferencesCount = g.largeDifferencesCount
        except:
            pass
##        Min = g.valuationdomain['min']
##        Max = g.valuationdomain['max']
##        Med = g.valuationdomain['med']
        self.valuationdomain = g.valuationdomain
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['computeRelation'] = time() - t0

        # compute rating categories
        t0 = time()
        if rankingRule == 'best':
            from linearOrders import NetFlowsOrder,CopelandOrder
            nf = NetFlowsOrder(g)           
            cop = CopelandOrder(g)
            corrnf = g.computeOrderCorrelation(nf.netFlowsOrder)
            #print('nf:', corrnf)
            corrcop = g.computeOrderCorrelation(cop.copelandOrder)
            #print('cop', corrcop)
            if corrnf['correlation'] >= corrcop['correlation']:
                actionsList = nf.netFlowsRanking
                self.rankingRule = 'NetFlows'
                self.rankingCorrelation = corrnf
                self.rankingScores = nf.netFlows
            else:
                actionsList = cop.copelandRanking
                self.rankingRule = 'Copeland'
                self.rankingCorrelation = corrcop
                self.rankingScores = cop.decCopelandScores
        elif rankingRule == 'Copeland':
            from linearOrders import CopelandOrder
            cop = CopelandOrder(g)
            actionsList = cop.copelandRanking
            self.rankingRule = 'Copeland'
            self.rankingScores = cop.decCopelandScores
        else: # net flows by default
            from linearOrders import NetFlowsOrder
            nf = NetFlowsOrder(g)
            actionsList = nf.netFlowsRanking
            self.rankingRule = 'NetFlows'
            self.rankingScores = nf.netFlows
        if rankingRule != 'best':
            actionsOrdering = list(actionsList)
            actionsOrdering.reverse()
            self.rankingCorrelation = g.computeOrderCorrelation(actionsOrdering)
        self.actionsRanking = actionsList
        if Debug:
            print('*',self.actionsRanking)
        self.ratingCategories = self.computeQuantilesRating(Debug=Debug)
        if Debug:
            print('Ranking rule        :', self.rankingRule)
            print('Actions ranking     :', self.actionsRanking)
            print('Ranking correlation :', self.rankingCorrelation)
            print('Rating categories:', self.ratingCategories)
        self.runTimes['rating'] = time() - t0
               
        # compute quantiles sorting
        t0 = time()
        if WithSorting:
            self.sorting = self.computeSortingCharacteristics()
            self.categoryContent = self.computeCategoryContents()
            if Debug:
                self.showSorting()
                self.showActionsSortingResult()
                self.showQuantileOrdering()
        self.runTimes['sorting'] = time() - t0

        # end of the construction
        self.runTimes['totalTime'] = time() - tt

    def __repr__(self):
        """
        Default presentation method for BipolarOutrankingDigraph instance.
        """
        String =  '*-----  Object instance description -----------*\n'
        String += 'Instance class      : %s\n' % self.__class__.__name__
        String += 'Instance name       : %s\n' % self.name
        String += '# Criteria          : %d\n' % len(self.criteria)
        String += '# Quantile profiles : %d\n' % len(self.profiles)
        String += '# New actions       : %d\n' % len(self.newActions)
        String += 'Size                : %d\n' % self.computeSize()
        String += 'Determinateness     : %.3f\n' % self.computeDeterminateness()
        String += 'Attributes: %s\n' % list(self.__dict__.keys())
        String += '*------  Constructor run times (in sec.) ------*\n'
        try:
            String += '# Threads        : %d\n' % self.nbrThreads
        except:
            self.nbrThreads = 1
            String += '# Threads        : %d\n' % self.nbrThreads
        String += 'Total time       : %.5f\n' % self.runTimes['totalTime']
        String += 'Data input       : %.5f\n' % self.runTimes['dataInput']
        String += 'Quantile classes : %.5f\n' % self.runTimes['categories']
        String += 'Compute profiles : %.5f\n' % self.runTimes['profiles']
        String += 'Compute relation : %.5f\n' % self.runTimes['computeRelation']
        String += 'Compute rating   : %.5f\n' % self.runTimes['rating']
        String += 'Compute sorting  : %.5f\n' % self.runTimes['sorting']
        return String 

# ------------ private methods ------------------

    def _computeLimitingQuantiles(self,g,_PrefThresholds=False,Debug=True):
        """
        Renders the list of limiting quantiles on criteria g
        """
        if _PrefThresholds:
            try:
                gPrefThrCst = self.criteria[g]['thresholds']['pref'][0]
                gPrefThrSlope = self.criteria[g]['thresholds']['pref'][1]
            except:
                gPrefThrCst = Decimal('0')
                gPrefThrSlope = Decimal('0')            
        gQuantiles = self.criteriaCategoryLimits[g]
        if Debug:
            print(g,gQuantiles)
        nq = len(gQuantiles)
        if self.LowerClosed:
            if _PrefThresholds:
                for i in range(nq-1): # quantile limits raised by the preference thershold
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        gQuantiles[i] += gPrefThrCst - gQuantiles[i]*gPrefThrSlope
                    else:
                        gQuantiles[i] += gPrefThrCst + gQuantiles[i]*gPrefThrSlope
            # we ignore the 1.00 quantile and replace it with +infty        
            if self.criteria[g]['preferenceDirection'] == 'min':
                gQuantiles[-1] = Decimal(str(self.criteria[g]['scale'][1]))
            else:
                gQuantiles[-1] = Decimal(str(self.criteria[g]['scale'][1])) * Decimal('2')       

        else:  # upper closed categories
            # we ignore the quantile 0.0 and replace it with -\infty            
            if self.criteria[g]['preferenceDirection'] == 'min':
                gQuantiles[0] = -Decimal(str(self.criteria[g]['scale'][1])) * Decimal('2')
            else:
                gQuantiles[0] = -Decimal(str(self.criteria[g]['scale'][1]))
            if _PrefThresholds:
                for i in range(1,nq): # quantile limits raised by the preference thershold
                    if self.criteria[g]['preferenceDirection'] == 'min':
                        gQuantiles[i] += gPrefThrCst - gQuantiles[i]*gPrefThrSlope
                    else:
                        gQuantiles[i] += gPrefThrCst + gQuantiles[i]*gPrefThrSlope
        if Debug:
            print(g,self.LowerClosed,self.criteria[g]['preferenceDirection'],gQuantiles)
        return gQuantiles

# ------------ public methods ------------------

    def computeCategoryContents(self,Debug=False):
        """
        Computes the quantiles sorting results per quantile category.
        """
        if self.LowerClosed:
            Reverse=False
        else:
            Reverse=True
        Med = self.valuationdomain['med']
        actions = self.newActions
        sorting = self.computeSortingCharacteristics(Debug=Debug)
        categoryContent = {}
        for c in self.orderedCategoryKeys(Reverse=Reverse):
            categoryContent[c] = []
            for x in actions:
                if sorting[x][c]['categoryMembership'] >= Med:
                    categoryContent[c].append(x)
        return categoryContent

    def computeQuantileOrdering(self,strategy=None,
                                Descending=True,
                                HTML=False,
                                Comments=False,
                                Debug=False):
        """
        Orders the quantiles sorting result of self.newActions.

        *Parameters*:
            * Descending: listing in *decreasing* (default) or *increasing* quantile order.
            * strategy: ordering in an {'optimistic' (default) | 'pessimistic' | 'average'}
              in the uppest, the lowest or the average potential quantile.
        
        """
        if strategy == None:
            strategy = 'average'
        if HTML:
            html = '<h1>Quantiles preordering</h1>'
            html += '<table style="background-color:White;" border="1">'
            html += '<tr bgcolor="#9acd32"><th>quantile limits</th>'
            html += '<th>Ordering by %s quantile class limits</th>' % strategy
            html += '</tr>'
        actionsCategories = {}
        for x in self.newActions:
            a,lowCateg,highCateg,credibility =\
                     self.showActionCategories(x,Comments=Debug)
            if strategy == "optimistic":
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]
            elif strategy == "pessimistic":
                try:
                    actionsCategories[(int(lowCateg),int(highCateg))].append(a)
                except:
                    actionsCategories[(int(lowCateg),int(highCateg))] = [a]
            elif strategy == "average":
                lc = float(lowCateg)
                hc = float(highCateg)
                ac = (lc+hc)/2.0
                try:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(ac,int(highCateg),int(lowCateg))] = [a]
            else:  # optimistic by default
                try:
                    actionsCategories[(int(highCateg),int(lowCateg))].append(a)
                except:
                    actionsCategories[(int(highCateg),int(lowCateg))] = [a]      
                
        actionsCategIntervals = []
        for interval in actionsCategories:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])
        actionsCategIntervals.sort(reverse=Descending)
        weakOrdering = []
        for item in actionsCategIntervals:
        #print(item)
            if Comments:
                if strategy == "optimistic":
                    if self.LowerClosed:
                        if HTML:
                            html += '<tr><tdbgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])                            
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                elif strategy == "pessimistic":
                    if self.LowerClosed:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])

                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][0])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )                   
                elif strategy == "average":
                    if self.LowerClosed:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][2])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
            weakOrdering.append(item[1])
        if HTML:
            html += '</table>'
            return html
        else:
            return weakOrdering

    def computeQuantilesRating(self,Debug=True):
        """
          Renders an ordered dictionary of non empty quantiles in ascending order.
        """
        ranking = list(self.actionsRanking)
        if self.LowerClosed: # lower closed quantiles
            ranking.reverse()
        if Debug:
            print(ranking)
        
        n = len(ranking)
        ratingCategories = OrderedDict()
        New = True
        for i in range(n):
            if ranking[i] in self.newActions:
                if New:
                    c = i-1
                    ratingCategories[ranking[c]] = [ranking[i]]
                    New = False
                else:
                    if self.LowerClosed:
                        ratingCategories[ranking[c]].insert(0,ranking[i])
                    else:
                        ratingCategories[ranking[c]].append(ranking[i])
            else:
                New = True
        if Debug:
            print(ratingCategories)
        return ratingCategories

    def computeRatingRelation(self,Debug=False,StoreRating=True):
        """
        Computes a bipolar rating relation using a pre-ranking (list of lists)
        of the self-actions (self.newActions + self.profiles).
        """
        try:
            ratingCategories = self.ratingCategories
        except:
            ratingCategories = self.computeQuantilesRating(Debug=Debug)
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']

        # pre-ranking self.actions
        profiles = self.profiles
        preRanking = []
        if self.LowerClosed: #  in ascending order
            for c in profiles:
                preRanking.insert(0,[c])
                if c in ratingCategories:
                    preRanking.insert(0,ratingCategories[c])
        else: # computing in descending order
            for c in reversed(profiles):
                preRanking.append([c])
                if c in ratingCategories:
                    preRanking.append(ratingCategories[c])
        if Debug:
            print('preRanking',preRanking)

        
        actions = [x for x in self.actions]
        currentActions = set(actions)
        ratingRelation = {}
        # init the relation decitionaries
        for x in actions:
            ratingRelation[x] = {}
            for y in actions:
                ratingRelation[x][y] = Med
        # computing the relation in descending order
        for eqcl in preRanking:
            currRest = currentActions - set(eqcl)
            if Debug:
                print(currentActions, eqcl, currRest)
            for x in eqcl:
                for y in currRest:
                    ratingRelation[x][y] = Max
                    ratingRelation[y][x] = Min
            currentActions = currentActions - set(eqcl)
        
        if StoreRating:
            self.ratingRelation = ratingRelation
        return ratingRelation

    def computeSortingCharacteristics(self, action=None, Debug=False):
        """
        Renders a bipolar-valued bi-dictionary relation (newActions x profiles)
        representing the degree of credibility of the
        assertion that "action x in A belongs to quantile category c profiles",
        If LowerClosed is True, x outranks the category low limit
        and x does not outrank the category high limit, or
        If LowerClosed is False, ie UPPERCLosed is True, the category
        low limit does not outrank x and the category high limit does outrank x. 
        """
        Min = self.valuationdomain['min']
        Med = self.valuationdomain['med']
        Max = self.valuationdomain['max']

        actions = self.newActions
            
        categories = self.categories

        LowerClosed = self.LowerClosed

        if Debug:
            if LowerClosed:
                print('x  in  K_k\t r(x >= m_k)\t r(x < M_k)\t r(x in K_k)')
            else:
                print('x  in  K_k\t r(m_k < x)\t r(M_k >= x)\t r(x in K_k)')

        sorting = {}
        nq = len(self.quantilesFrequencies) - 1
        for x in actions:
            if Debug:
                print('action',x)
            sorting[x] = {}
            for c in categories:
                sorting[x][c] = {}
                if LowerClosed:
                    cKey= 'm'+c
                else:
                    cKey= 'M'+c
                if LowerClosed:
                    lowLimit = self.relation[x][cKey]
                    if int(c) < nq:
                        cMaxKey = 'm'+str(int(c)+1)
                        notHighLimit = Max - self.relation[x][cMaxKey] + Min
                    else:
                        notHighLimit = Max
                else:
                    if int(c) > 1:
                        cMinKey = 'M'+str(int(c)-1)
                        lowLimit = Max - self.relation[cMinKey][x] + Min
                    else:
                        lowLimit = Max
                    notHighLimit = self.relation[cKey][x]
                #if Comments:
                #    print('%s in %s: low = %.2f, high = %.2f' % \
                #          (x, c,lowLimit,notHighLimit), end=' ')
                if Debug:
                    print('%s in %s - %s\t' % (x, self.categories[c]['lowLimit'],self.categories[c]['highLimit'],), end=' ')
                categoryMembership = min(lowLimit,notHighLimit)
                sorting[x][c]['lowLimit'] = lowLimit
                sorting[x][c]['notHighLimit'] = notHighLimit
                sorting[x][c]['categoryMembership'] = categoryMembership

                if Debug:
                    #print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
                    print('%.2f\t\t %.2f\t\t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))

        return sorting

    def exportRatingGraphViz(self,fileName=None,relation=None,\
                             direction='best',Comments=True,\
                             graphType='png',graphSize='7,7',\
                             fontSize=10):
        """
        The rating drawing is using the :py:func:`transitiveDigraphs.TransitiveDigraph.exportGraphViz` method for
        drawing oriented Hasse diagrams of weak orderings, ie the negation
        of the corresponding preorder relation.

        Continuing the previous Python session:

        >>> nqr.showQuantilesRating()
        *-------- Quantile sorting result ---------
        [0.50 - 0.75[ ['a01']
        [0.25 - 0.50[ ['a07', 'a02', 'a10', 'a06', 'a03', 'a08', 'a09', 'a04']
        [0.00 - 0.25[ ['a05']
        >>> nqr.exportRatingGraphViz('quantilesRatingDigraph',Comments=False)
        *---- exporting a dot file for GraphViz tools ---------*
        Exporting to quantilesRatingDigraph.dot
        dot -Grankdir=TB -Tpng quantilesRatingDigraph.dot -o quantilesRatingDigraph.png

        .. image:: quantilesRatingDigraph.png
            :alt: usage example of Normed Quantiles Rating Digraph
            :width: 400 px
            :align: center
        
        .. warning::

             For graphviz, nodes' or actions' keys of the digraph must start with a letter
             and may not contain special characters like '-' or '_'.
             
        """
        from transitiveDigraphs import TransitiveDigraph
        from copy import deepcopy
        ratingRelation = self.computeRatingRelation()
        self.relationOrig = deepcopy(self.relation)
        self.relation = ratingRelation
        TransitiveDigraph.exportGraphViz(self,fileName=fileName,\
                             direction=direction,Comments=Comments,\
                             graphType=graphType,graphSize=graphSize,\
                             digraphClass=self.__class__,\
                             fontSize=fontSize)
        self.relation = self.relationOrig

    def htmlRatingHeatmap(self,argCriteriaList=None,
                               argActionsList=None,
                               quantiles=None,
                               ndigits=2,
                               contentCentered=True,
                               colorLevels=None,
                               pageTitle='Rating Heatmap',
                               Correlations=False,
                               Threading=False,
                               nbrOfCPUs=1,
                               Debug=False):
        """       
        Renders the Brewer RdYlGn 5,7, or 9 levels colored heatmap of the performance table
        actions x criteria in html format.

        See the corresponding :py:meth:`perfTabs.showHTMLPerformanceHeatMap` method.
        """
        print('see browser')
        from decimal import Decimal
                    
        brewerRdYlGn9Colors = [(Decimal('0.1111'),'"#D53E4F"'),
                               (Decimal('0.2222'),'"#F46D43"'),
                               (Decimal('0.3333'),'"#FDAE61"'),
                               (Decimal('0.4444'),'"#FEE08B"'),
                               (Decimal('0.5555'),'"#FFFFBF"'),
                               (Decimal('0.6666'),'"#D9EF8B"'),
                               (Decimal('0.7777'),'"#A6D96A"'),
                               (Decimal('0.8888'),'"#65BD63"'),
                               (Decimal('1.000'),'"#1A9850"')]
        brewerRdYlGn7Colors = [
                               (Decimal('0.1429'),'"#F46D43"'),
                               (Decimal('0.2857'),'"#FDAE61"'),
                               (Decimal('0.4286'),'"#FEE08B"'),
                               (Decimal('0.5714'),'"#FFFFBF"'),
                               (Decimal('0.7143'),'"#D9EF8B"'),
                               (Decimal('0.8571'),'"#A6D96A"'),
                               (Decimal('1.0000'),'"#65BD63"')
                               ]
        brewerRdYlGn5Colors = [
                               (Decimal('0.2'),'"#FDAE61"'),
                               (Decimal('0.4'),'"#FEE08B"'),
                               (Decimal('0.6'),'"#FFFFBF"'),
                               (Decimal('0.8'),'"#D9EF8B"'),
                               (Decimal('1.0'),'"#A6D96A"')
                               ]
        if colorLevels == None:
            colorLevels = 7
        if colorLevels == 7:
            colorPalette = brewerRdYlGn7Colors
        elif colorLevels == 9:
            colorPalette = brewerRdYlGn9Colors
        elif colorLevels == 5:
            colorPalette = brewerRdYlGn5Colors
        else:
            colorPalette = brewerRdYlGn7Colors
        nc = len(colorPalette)
        backGroundColor   = '"#FFFFFF"'
        naColor           = '"#FFFFFF"'
        columnHeaderColor = '"#CCFFFF"'
        rowHeaderColor    = '"#FFFFFF"'
        actionRowHeaderColor = '#FFF79B'

        html = '<!DOCTYPE html><html><head>\n'
        html += '<title>%s</title>\n' % 'Digraph3 performance heat map'
        html += '<style type="text/css">\n'
        #html += 'table {border-collapse: collapse;}'
        if contentCentered:
            html += 'td {text-align: center;}\n'
        html += 'td.na {color: rgb(192,192,192);}\n'
        html += 'tr.quantile {color: rgb(100,100,100);}\n'
        html += '</style>\n'
        html += '</head>\n<body>\n'
        html += '<h2>%s</h2>\n' % pageTitle
        
##        from sparseOutrankingDigraphs import PreRankedOutrankingDigraph
        if argCriteriaList == None:
            argCriteriaList = list(self.criteria.keys())
            criteriaList = None
        else:
            criteriaList = argCriteriaList

        rankingRule = self.rankingRule
        
        if argActionsList == None:
            actionsList = self.actionsRanking
        else:
            actionsList = argActionsList
        na = len(actionsList)
        profiles = self.profiles
        categories = self.categories
        if Correlations:
            rankCorrelation = self.computeOrderCorrelation(list(reversed(actionsList)))
        if Debug:
            print('1',actionsList)
            print('2',rankCorrelation)

        criteria = self.criteria
        if criteriaList == None:
            if Correlations:
                criteriaCorrelation =\
                        self.computeMarginalVersusGlobalRankingCorrelations(\
                                actionsList,ValuedCorrelation=True,Threading=Threading,
                                nbrCores=nbrOfCPUs)
                criteriaList = [c[1] for c in criteriaCorrelation]
            else:
                criteriaList = list(criteria.keys())
                criteriaList.sort()
                criteriaWeightsList = [(abs(criteria[g]['weight']),g) for g in criteriaList]
                criteriaWeightsList.sort(reverse=True)
                criteriaList = [g[1] for g in criteriaWeightsList]
                criteriaCorrelation = None
        else:
            criteriaList = list(criteria.keys())
            if Correlations:
                criteriaCorrelation =\
                        self.computeMarginalVersusGlobalRankingCorrelations(\
                                actionsList,ValuedCorrelation=True,Threading=Threading,
                                nbrCores=nbrOfCPUs)
            else:
                criteriaCorrelation = None
            
        quantileColor={}
        for x in actionsList:
            quantileColor[x] = {}
            for g in criteriaList:
                quantilexg = self.computeActionCriterionQuantile(x,g)
                if Debug:
                    print(x,g,quantilexg)
                if quantilexg != 'NA':
                    for i in range(nc):
                        if Debug:
                            print(i, colorPalette[i][0])
                        
                        if quantilexg <= colorPalette[i][0]:
                            quantileColor[x][g] = colorPalette[i][1]
                            break
                else:
                    quantileColor[x][g] = naColor
                if Debug:
                    print(x,g,quantileColor[x][g])
        # heatmap
        html += '<i>Ranking rule</i>: <b>%s</b>; <i>Ranking correlation</i>: <b>%.3f</b>\n'\
                % (self.rankingRule,self.rankingCorrelation['correlation'])
        html += '<table style="background-color:%s;" border="1">\n' % (backGroundColor) 
        html += '<tr bgcolor=%s><th>criteria</th>' % (columnHeaderColor)
        for g in criteriaList:
            try:
                gName = self.criteria[g]['shortName']
            except:
                gName = str(g)
            html += '<th>%s</th>' % (gName)
        html += '</tr>\n'
        html += '<tr><th bgcolor=%s>weights</th>' % (columnHeaderColor)
        for g in criteriaList:
            html += '<td align="center">%s</td>' % (str(self.criteria[g]['weight']))
        html += '</tr>\n'
        if criteriaCorrelation != None:
            html += '<tr><th bgcolor=%s>tau<sup>(*)</sup></th>' % (columnHeaderColor)
            for cg in criteriaCorrelation:
                html += '<td align="center">%.2f</td>' % (cg[0])
            html += '</tr>\n'
##        if Debug:
##            print(html)
        for x in actionsList:
            if x in profiles:
                xcat = profiles[x]['category']
                if self.LowerClosed:
                    xName = categories[xcat]['lowLimit'] + ' -'
                else:
                    xName = '- ' + categories[xcat]['highLimit']
            else:
                try:
                    xName = self.actions[x]['shortName']
                except:
                    xName = str(x)
            if x in profiles:
                html += '<tr class="quantile"><th bgcolor=%s>%s</th>' % (rowHeaderColor,xName)
            else:
                html += '<tr><th bgcolor=%s>%s</th>' % (actionRowHeaderColor,xName)                
            for g in criteriaList:
                if self.evaluation[g][x] != Decimal("-999"):
                    formatString = '<td bgcolor=%s align="right">%% .%df</td>' % (quantileColor[x][g],ndigits)
                    html += formatString % (self.evaluation[g][x])
                else:
                    html += '<td bgcolor=%s class="na">NA</td>' % naColor
##                if Debug:
##                    print(html)
            html += '</tr>\n'
        html += '</table>\n'
        # table legend
        html += '<b>Color legend: </b><br/>\n'
        html += '<table style="background-color:%s;" border="1">\n' % (backGroundColor) 
        html += '<tr bgcolor=%s><th>quantile</th>' % (columnHeaderColor)
        #html += '<td bgcolor=%s>&nbsp;[%.2f - %.2f[&nbsp;</td>' % (colorPalette[0][1],0.0,colorPalette[0][0])
        for col in range(0,nc):
            html += '<td bgcolor=%s>&nbsp;%.2f&#037;</td>' % (colorPalette[col][1],
                                                                  #colorPalette[col-1][0],
                                                                   colorPalette[col][0]*Decimal('100.0'))
        html += '</tr>\n'
        html += '</table>\n'
        if criteriaCorrelation != None:
            html += '<i>(*) tau: Ordinal (Kendall) correlation between</i><br/>'
            html += '<i>marginal criterion and global ranking relation.</i><br/>\n'
##        if rankCorrelation != None:
##            html += '<i>Ordinal (Kendall) correlation between global ranking and outranking relation: %.2f.</i>' % (rankCorrelation['correlation'])
        html += '</body></html>'
        return html

    def showActionCategories(self,action,Debug=False,Comments=True):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        Med = self.valuationdomain['med']
        try:
            sorting = self.sorting
        except:
            sorting = self.computeSortingCharacteristics(action=action,Debug=Debug)
        catKeys = self.orderedCategoryKeys()
        keys = [catKeys[0],[catKeys[-1]]]
        lowLimit = sorting[action][catKeys[0]]['lowLimit']
        notHighLimit = sorting[action][catKeys[-1]]['lowLimit']
        for c in self.orderedCategoryKeys():
            if sorting[action][c]['categoryMembership'] >= Med:
                if sorting[action][c]['lowLimit'] > Med:
                    lowLimit = sorting[action][c]['lowLimit']
                    keys[0] = c
                if sorting[action][c]['notHighLimit'] > Med:
                    notHighLimit = sorting[action][c]['notHighLimit']
                    keys[1] = c
                #keys.append(c)
                if Debug:
                    print(action, c, sorting[action][c], keys)
        credibility = min(lowLimit,notHighLimit)
        if Comments:
            print('%s - %s: %s with credibility: %.2f = min(%.2f,%.2f)' % (\
                                 self.categories[keys[0]]['lowLimit'],\
                                 self.categories[keys[-1]]['highLimit'],\
                                 action,\
                                 credibility,lowLimit,notHighLimit) )
        return action,\
                keys[0],\
                keys[1],\
                credibility            


    def showActionsSortingResult(self,actionSubset=None,Debug=False):
        """
        Shows the quantiles sorting result of all (default) or
        a subset of the decision actions.
        """
        if actionSubset == None:
            actions = [x for x in self.newActions]
            #actions.sort()
        else:
            actions = [x for x in flatten(actionSubset)]
        print('Quantiles sorting result per decision action')
        for x in actions:
            self.showActionCategories(x,Debug=Debug)

    def showHTMLRatingHeatmap(self,actionsList=None,
                                   criteriaList=None,
                                   colorLevels=7,
                                   pageTitle=None,
                                   ndigits=2,
                                   quantiles=None,
                                   rankingRule=None,
                                   Correlations=False,
                                   Threading=False,
                                   nbrOfCPUs=None,
                                   Debug=False):
        """
        Specialisation of html heatmap version showing the performance tableau in a browser window;
        see :py:meth:`perfTabs.showHTMLPerformanceHeatMap` method.

        **Parameters**:

              - *actionsList* and *criteriaList*, if provided,  give the possibility to show the decision alternatives, resp. criteria, in a given ordering.
              - *ndigits* = 0 may be used to show integer evaluation values.
              - If no *actionsList* is provided, the decision actions are ordered from the best to the worst following the ranking of the NormedQuatilesRatingDigraph instance.              
              - It may interesting in some cases to use *RankingRule* = 'NetFlows'.
              - With *Correlations* = *True* and *criteriaList* = *None*, the criteria will be presented from left to right in decreasing order of the correlations between the marginal criterion based ranking and the global ranking used for presenting the decision alternatives.
              - Computing the marginal correlations may be boosted with Threading = True, if multiple parallel computing cores are available.

        Suppose we observe the following rating result:
        
            >>> nqr.showQuantilesRating()
            [0.50 - 0.75[ ['a1005', 'a1010', 'a1008', 'a1002', 'a1006']
            [0.25 - 0.50[ ['a1003', 'a1001', 'a1007', 'a1004', 'a1009']
            >>> nqr.showHTMLRatingHeatmap(pageTitle='Heat map of the ratings',
            ...                           Correlations=True,
            ...                           colorLevels = 5)

        .. image:: heatMap1.png
            :alt: usage example of Normed Quantiles Rating Digraph
            :width: 550 px
            :align: center

        
        """
        if rankingRule != None:
            print('A ranking rule - Copeland (default) or NetFlows may be given with the NormedQuantilesRatingDigraph constructor')
        import webbrowser
        fileName = '/tmp/performanceHeatmap.html'
        fo = open(fileName,'w')
        if pageTitle == None:
            pageTitle = 'Heatmap of Performance Tableau \'%s\'' % self.name
            
        fo.write(self.htmlRatingHeatmap(argCriteriaList=criteriaList,
                                             argActionsList=actionsList,
                                             quantiles=quantiles,
                                             ndigits=ndigits,
                                             colorLevels=colorLevels,
                                             pageTitle=pageTitle,
                                             Correlations=Correlations,
                                             Threading=Threading,
                                             nbrOfCPUs=1,
                                             Debug=Debug))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)

    def showHTMLQuantilesSorting(self,Descending=True,strategy='average'):
        """
        Shows the html version of the quantile sorting result in a browser window.

        The ordring strategy is either:
            * **optimistic**, following the upper quantile limits (default),
            * **pessimistic**, following the lower quantile limits,
            * **average**, following the averag of the upper and lower quantile limits.
        """
        import webbrowser
        fileName = '/tmp/preOrdering.html'
        fo = open(fileName,'w')
        fo.write(self.computeQuantileOrdering(Descending=Descending,
                                              strategy=strategy,
                                              HTML=True,
                                              Comments=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open_new(url)

    def showOrderedRelationTable(self,relation=None,direction="decreasing"):
        """
        Showing the relation table in decreasing (default) or increasing order.
        """
        try:
            actionsList = self.actionsRanking
        except:
            actionsList = self.computeNetFlowsRanking()
        
        if direction != "decreasing":
            actionsList.reverse()

        if relation == None:
            relation = self.relation

        Digraph.showRelationTable(self,actionsSubset=actionsList,\
                                relation=relation,\
                                Sorted=False,\
                                ReflexiveTerms=False)
        
    def showQuantilesRating(self,Descending=True,Debug=False):
        try:
            ratingCategories = self.ratingCategories
        except:
            ratingCategories = self.computeQuantilesRating(Debug=Debug)
        print('*-------- Quantiles rating result ---------')
        if self.LowerClosed:
            if Descending:
                for cat in reversed(ratingCategories):
                    c = self.profiles[cat]['category']
                    print(self.categories[c]['name'],ratingCategories[cat])
            else:
                for cat in ratingCategories:
                    c = self.profiles[cat]['category']
                    print(self.categories[c]['name'],ratingCategories[cat])
        else:
            if Descending:
                for cat in ratingCategories:
                    c = self.profiles[cat]['category']
                    print(self.categories[c]['name'],ratingCategories[cat])
            else:
                for cat in reversed(ratingCategories):
                    c = self.profiles[cat]['category']
                    print(self.categories[c]['name'],ratingCategories[cat])

    def showQuantilesSorting(self,strategy='average'):
        """
        Dummy show method for the commenting computeQuantileOrdering() method.
        """
        print('*----- Quantiles sorting result ----')
        self.computeQuantileOrdering(strategy=strategy,Comments=True)
            
    def showRankingScores(self,direction='descending'):
        """
        Shows the ranking scores of the Copeland or the netflows ranking rule,
        the number of incoming arcs minus the number of outgoing arcs, resp.
        the sum of inflows minus the outflows.
        """
        print('%s Ranking Scores in %s Order' % (self.rankingRule,direction))
        print('action \t score')
        if direction == 'descending':
            for x in self.rankingScores:
                print('%s \t %.2f' %(x[1],-x[0]))
        else:
            for x in reversed(self.outFlows):
                print('%s \t %.2f' %(x[1],-x[0]))
                                         
##    def getActionsKeys(self,action=None,WithoutProfiles=True):
##        """
##        extract normal actions keys()
##        """
##        profiles = set([x for x in list(self.profiles.keys())])
##        if action == None:
##            actionsExt = set([x for x in list(self.newActions.keys())])
##            if WithoutProfiles:
##                return actionsExt - profiles
##            else:
##                return actionsExt | profiles
##        else:
##            return set([action])           

##########################################################3
#----------test SortingDigraph class ----------------
if __name__ == "__main__":
    from time import time
    from perfTabs import *
    from randomPerfTabs import *
    from outrankingDigraphs import *
    from sortingDigraphs import *
    from transitiveDigraphs import *
    from performanceQuantiles import *
    
    print("""
    ****************************************************
    * Python sortingDigraphs module                    *
    * depends on BipolarOutrankingDigraph and          *
    * $Revision$                                 *
    * Copyright (C) 2010 Raymond Bisdorff              *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    print('*-------- Testing class and methods -------')


    MP = False
##    t = PerformanceTableau('auditor2_1')
##    t.showHTMLPerformanceHeatmap(ndigits=0,quantiles=7,Correlations=True,Debug=False)
##    t = XMCDA2PerformanceTableau('spiegel2004')
##    t = XMCDA2PerformanceTableau('ex1')
##    t = RandomCBPerformanceTableau(numberOfActions=25,
##                                    numberOfCriteria=13,
##                                             NegativeWeights=True,
##                                    weightDistribution='equiobjectives',
##                                    missingDataProbability=0.05,
##                                    seed=1)
##    #t.showHTMLPerformanceHeatmap(Correlations=True)
##    nt = NormalizedPerformanceTableau(t)
##    nt.showHTMLPerformanceHeatmap(Correlations=True)
    
##    so = SortingDigraph(t,scaleSteps=5,LowerClosed=True,Debug=True)
####    so = SortingDigraph('grafittiPerfTab','grafittiCategories')
##    so = SortingDigraph(t,scaleSteps=7,Debug=True)
##    print(so.categories)
##    so.saveCategories('testCategories')
####    print(so.profiles)
####    print(so.criteriaCategoryLimits)
##    so.showSortingCharacteristics()
##    so.showSorting(Reverse=False)
##    so.showSorting()
##    print('optimistic')
##    so.showWeakOrder(Descending=True,strategy='optimistic')
##    print('pessimistic')
##    so.showWeakOrder(strategy='pessimistic')
##    print('average')
##    so.showWeakOrder()
##    so1 = SortingDigraph(nt,scaleSteps=10,LowerClosed=False)
##    so1.computeWeakOrder(Comments=True)
##    so1.showPerformanceTableau(actionsSubset=so1.profiles['min'])
##    so1.showPerformanceTableau(actionsSubset=so1.profiles['max'])
##    so1.showSorting()
##    so1.showSortingCharacteristics()
    
##    so.computeWeakOrder(Debug=True)
##    so1.computeWeakOrder(Comments=True,Debug=True)
                                                                            
##    so.saveProfiles('testProfile')
##    t.save()
##    nt = NormalizedPerformanceTableau(t)
##    so1 = SortingDigraph(nt,'testProfile')
##    so1.showSorting()
##    categoriesData = {'categories': so.categories,\
##                      'criteriaCategoryLimits': so.criteriaCategoryLimits}
##    so2 = SortingDigraph(nt,categoriesData)
##    so2.showSorting()
    
##    t.saveXMCDA2('test',servingD3=False)
##    #t = XMCDA2PerformanceTableau('test')  
##    #t.showHTMLPerformanceHeatmap(colorLevels=5,ndigits=0,Correlations=True)
##    qs = QuantilesSortingDigraph(t,limitingQuantiles=7,LowerClosed=False,
##                                     Threading=MP,tempDir='.',Comments=True,
##                                     Debug=False)
##    qs.showHTMLQuantileOrdering(strategy='average')
##    qs.showWeakOrder()
##    qs.showQuantileOrdering(strategy='average')
##    qs.showActionsSortingResult()
##    qs0 = _QuantilesSortingDigraph(t,15,LowerClosed=False,
##                                     Threading=False,
##                                     Debug=False)
##    qs0.showSorting()
##    qs0.showSortingCharacteristics('a01')
    #qs0.showWeakOrder()
    #qs.showQuantileOrdering(strategy=None)
    #qs0.exportGraphViz('test')
    #qs0.showActionsSortingResult()
    
##    qs0.showOrderedRelationTable()
##    qs0.exportGraphViz()
##    qs0.showSorting()
##    qs0.showActionsSortingResult(Debug=False)
##    qs0.computeWeakOrder(Debug=True)
##    qs0.recodeValuation()
##    qs0.showSorting()
##    qs0.showActionsSortingResult(Debug=False)
##    qs0.computeWeakOrder(Debug=True)
##    g = BipolarOutrankingDigraph(t,Normalized=True)
##    print(g.computeOrdinalCorrelation(qs0))
##    print(g.computeOrdinalCorrelation(qsrbc))
    
##    # test incremental rating agent
    MP = False
    seed = 1000
    nbrOfCPUs = 4

##    from randomPerfTabs import RandomPerformanceTableau
##    from randomPerfTabs import RandomPerformanceGenerator as PerfTabGenerator
##    nbrActions=1000
##    nbrCrit = 13
##    tp = RandomPerformanceTableau(numberOfActions=nbrActions,\
##                                    numberOfCriteria=nbrCrit,seed=seed)

##    from randomPerfTabs import RandomCBPerformanceTableau
##    from randomPerfTabs import RandomCBPerformanceGenerator as PerfTabGenerator
##    nbrActions=100
##    nbrCrit = 13
##    tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,\
##                                    numberOfCriteria=nbrCrit,\
##                                    Threading=MP,seed=seed)
##
    from randomPerfTabs import Random3ObjectivesPerformanceTableau
    from randomPerfTabs import RandomPerformanceGenerator as PerfTabGenerator
    nbrActions=100
    nbrCrit = 21
    tp = Random3ObjectivesPerformanceTableau(numberOfActions=nbrActions,\
                                    numberOfCriteria=nbrCrit,seed=seed)

    qs = QuantilesSortingDigraph(tp,7,LowerClosed=True)
    #qs.showSorting()
    print('==>> average')
    qs.showHTMLQuantileOrdering(strategy='average')
    print('==>> optimistic')
    qs.showQuantileOrdering(strategy='optimistic')
    print('==>> pessimistic')
    qs.showQuantileOrdering(strategy='pessimistic')
##    pq = PerformanceQuantiles(tp,20,LowerClosed=True,Debug=False)
##    tpg = PerfTabGenerator(tp,instanceCounter=0,seed=seed)
##    newActions = tpg.randomActions(100)
##    pq.updateQuantiles(newActions,historySize=None)
##    ira = NormedQuantilesRatingDigraph(pq,newActions,quantiles=20,\
##                                       #PrefThresholds=False,\
##                                   WithSorting=True,Debug=False,\
##                                       Threading=MP,nbrOfCPUs=nbrOfCPUs)
##    print(ira)
##    ira.showQuantilesRating()
##    #ira.sorting = ira.computeSortingCharacteristics()
##    #ira.categoryContent = ira.computeCategoryContents()
##    ira.showSorting()
##    for x in ira.newActions:
##        ira.showActionCategories(x,Comments=True)
##    ratingRelation = ira.computeRatingRelation()
##    ira.relation = ratingRelation
##    #ira.closeTransitive(Irreflexive=True,Reverse=True)
##    ira.showHTMLRelationTable(actionsList=ira.actionsRanking)
##    ira.exportRatingGraphViz(graphType='pdf')
##    #ira.showSorting()
##    #ira.showHTMLSorting()
##    ira.showActionsSortingResult()
##    ira.showQuantilesSorting()
##    ira.showHTMLQuantilesSorting()
##    #ira.showRefinedQuantileOrdering()
##    #ira.showOrderedRelationTable()
##    #ira.showSortingCharacteristics()
##    ira.showHTMLRatingHeatmap(pageTitle='Heat map of the ratings',
##                                   Correlations=True,
##                                   #rankingRule='best',
##                                   )
##    ira.showRankingScores()
##    print(ira)
##    print(ira.computeQuantileProfile(0.25))
##    print(ira.computeQuantileProfile(0.5))
##    print(ira.computeQuantileProfile(0.75))

#     nbrActions=1000
#     nbrCrit = 7
#     seed = 105
#     tp = RandomCBPerformanceTableau(numberOfActions=nbrActions,\
#                    numberOfCriteria=nbrCrit,seed=seed)
#     from performanceQuantiles import PerformanceQuantiles
#     pq = PerformanceQuantiles(tp,\
#                    numberOfBins = 'deciles',\
#                   LowerClosed=True,Debug=False)
# ##    pq.showLimitingQuantiles(ByObjectives=True)
#     # generate 100 new random decision actions
#     from randomPerfTabs import RandomPerformanceGenerator
#     rpg = RandomPerformanceGenerator(tp,seed=seed)
#     newActions = rpg.randomPerformanceTableau(10)
#     # Updating the quartile norms shown above
#     pq.updateQuantiles(newActions,historySize=None)
# ##    pq.showHTMLLimitingQuantiles(Transposed=True)
# ##    from sortingDigraphs import NormedQuantilesRatingDigraph
#     nqr = NormedQuantilesRatingDigraph(pq,newActions,rankingRule='best',\
#                                        quantiles=4,Debug=False)
#     print(nqr)
##    nqr.showHTMLRatingHeatmap(pageTitle='Heat map of the ratings', colorLevels=5,
##                                       Correlations=True,
##                                       )
##    nqr.showQuantilesRating()
##    nqr.exportRatingGraphViz(Comments=False)
##
##
##    pq1 = PerformanceQuantiles(tp,\
##                   numberOfBins = 'deciles',\
##                  LowerClosed=True,Debug=False)
##    pq1.showLimitingQuantiles(ByObjectives=True)
##    # Updating the quartile norms shown above
##    pq1.updateQuantiles(newActions,historySize=None)
##    pq1.showHTMLLimitingQuantiles(Transposed=True)
##    from sortingDigraphs import NormedQuantilesRatingDigraph
##    nqr1 = NormedQuantilesRatingDigraph(pq1,newActions,rankingRule='best',Debug=False)
##    print(nqr1)
##    nqr1.showHTMLRatingHeatmap(pageTitle='Heat map of the deciles rating',
##                                       colorLevels=7,
##                                       Correlations=True,
##                                       )
##    nqr1.showQuantilesRating()
##    nqr1.exportRatingGraphViz(Comments=False)
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. december 2010                *')
    print('* $Revision$                  *')
    print('*************************************')

#############################
# Log record for changes:
# $Log: sortingDigraphs.py,v $
#############################
