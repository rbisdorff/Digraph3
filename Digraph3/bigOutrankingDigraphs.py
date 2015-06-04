#!/usr/bin/env python3
# Python 3 implementation of digraphs
# sub-module for big outranking digraphs
# Copyright (C) 2015  Raymond Bisdorff
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#######################

from outrankingDigraphs import *
from sortingDigraphs import *
from time import time

#####
def _initTask1(compID):
    """
    Task definition for multiprocessing threaded jobs in BigOutrankingDigraph
    construction
    
    .. Note::
    
          The local outranking digraph for each indiviual quantile classes
          is contructed on the baisi of a partial,
          ie component restricted, performance tableau.
    """
    from pickle import dumps, loads, load
    from copy import copy as deepcopy
    from outrankingDigraphs import BipolarOutrankingDigraph
    Comments = True
    if Comments:
        print("Starting working on component %d" % (compID), end=" ")
    fiName = 'partialPerfTab-'+str(compID)+'.py'
    fi = open(fiName,'rb')
    pt = loads(fi.read())
    fi.close()
    g = BipolarOutrankingDigraph(pt,Normalized=True)
    nc = g.order
    if Comments:
        print(nc)
    foName = 'splitCompRelation-'+str(compID)+'.py'
    fo = open(foName,'wb')                                            
    fo.write(dumps(g.relation,-1))
    fo.close()
    writestr = 'Finished component %d %d' % (compID,nc)
    return writestr


class BigBipolarOutrankingDigraph(QuantilesSortingDigraph,
                                  BipolarOutrankingDigraph):
    """
    Multiprocessing implementation of the OutrankingDigraph class for large instances (order > 100)
    """
    def __init__(self,argPerfTab=None,quantiles=None,
                 quantilesOrderingStrategy='average',
                 LowerClosed=True,
                 Threading=True,nbrOfCPUs=None,
                 Comments=True,
                 Debug=True):
        
        from time import time
        from os import cpu_count
        from multiprocessing import Pool

        
        ttot = time()
        perfTab = argPerfTab
        na = len(perfTab.actions)
        if quantiles == None:
            if na < 200:
                quantiles = na // 2
            else:
                quantiles = 100
        self.sortingParameters = {}
        self.sortingParameters['limitingQuantiles'] = quantiles
        self.sortingParameters['strategy'] = quantilesOrderingStrategy
        self.sortingParameters['LowerClosed'] = LowerClosed
        self.sortingParameters['Threading'] = Threading
        self.sortingParameters['nbrOfCPUs'] = nbrOfCPUs
        self.sortingParameters['PrefThresholds'] = False
        self.sortingParameters['hasNoVeto'] = False
        

        t0 = time()
        if Comments:        
            print('Computing the %d-quantiles sorting digraph ...' % (quantiles))
        if Threading:
            QuantilesSortingDigraph.__init__(self,argPerfTab=perfTab,
                                            limitingQuantiles=quantiles,
                                            LowerClosed=LowerClosed,
                                            CompleteOutranking=False,
                                            Threading=Threading,
                                            nbrCores=nbrOfCPUs,
                                            Debug=Debug)
        else:
            QuantilesSortingDigraph.__init__(self,argPerfTab=perfTab,
                                            limitingQuantiles=quantiles,
                                            LowerClosed=LowerClosed,
                                            CompleteOutranking=True,
                                            Threading=Threading,
                                            nbrCores=nbrOfCPUs,
                                            Debug=Debug)
        self.runTimes = {'sorting': time() - t0}
        if Comments:
            print('execution time: %.4f' % (self.runTimes['sorting']))

        self.name = perfTab.name + '_mp'
        tw = time()
        self.quantilesOrderingStrategy = self.sortingParameters['strategy']
        if self.quantilesOrderingStrategy == 'average':
            self.decomposition = [((self.categories[str(item[0][2])]['lowLimit'],
                                    self.categories[str(item[0][1])]['highLimit']),item[1])\
                                  for item in self._computeQuantileOrdering(strategy=self.quantilesOrderingStrategy,
                                         Descending=False)]
        elif self.quantilesOrderingStrategy == 'optimistic':
            self.decomposition = [((self.categories[str(item[0][1])]['lowLimit'],
                                    self.categories[str(item[0][0])]['highLimit']),item[1])\
                                  for item in self._computeQuantileOrdering(strategy=self.quantilesOrderingStrategy,
                                         Descending=False)]
        elif self.quantilesOrderingStrategy == 'pessimistic':
            self.decomposition = [((self.categories[str(item[0][0])]['lowLimit'],
                                    self.categories[str(item[0][1])]['highLimit']),item[1])\
                                  for item in self._computeQuantileOrdering(strategy=self.quantilesOrderingStrategy,
                                         Descending=False)]

        self.nbrOfCPUSs = nbrOfCPUs
        componentsList = [comp[1] for comp in self.decomposition]
        nwo = len(componentsList)
        self.runTimes['preordering'] = time() - tw
        if Comments:
            print('weak ordering execution time: %.4f' % self.runTimes['preordering']  )
        

        if Threading and cpu_count() > 2:
            from pickle import dumps, loads, load
            from tempfile import TemporaryDirectory
            from os import getcwd, chdir
            with TemporaryDirectory() as tempDirName:
                cwd = getcwd()
                chdir(tempDirName)
                unorderedfilledCompKeys = []
                if Comments:
                    print('Preparing the thread data ...')
                t0 = time()
                for c in range(nwo):
                    comp = componentsList[c]
                    nc = len(comp)
                    if Comments:
                        print('%d/%d %d' %(c,nwo,nc))
                    if nc > 1:
                        unorderedfilledCompKeys.append((nc,c))
                        pt = PartialPerformanceTableau(argPerfTab,actionsSubset=comp)                     
                        foName = 'partialPerfTab-'+str(c)+'.py'
                        fo = open(foName,'wb')
                        ptDp = dumps(pt,-1)
                        fo.write(ptDp)
                        fo.close()
                t1 = time()
                unorderedfilledCompKeys.sort(reverse=True)
                filledCompKeys = [ x[1] for x in unorderedfilledCompKeys]
                self.runTimes['threadPreparing'] = t1 - t0
                if Comments:
                    print(unorderedfilledCompKeys)
                    print(filledCompKeys)
                    print('%d of %d' % (len(filledCompKeys),nwo))
                    print('Execution time: %.4f sec.' % (t1-t0))
                
                if Comments:
                    print('Threading ... !')
                t0 = time()
                with Pool(processes=nbrOfCPUs) as pool:
                    for res in pool.imap_unordered(_initTask1,
                                                       filledCompKeys,
                                                       1):
                        if Comments:
                            print(res)
                self.runTimes['threadingTime'] = time() - t0
                if Comments:
                    print('Finished all threads in %.4f sec.' % (self.runTimes['threadingTime']) )
                t0 = time()
                for c in range(nwo):
                    comp = componentsList[c]
                    nc = len(comp)
                    #print('%d/%d' % (c,nwo), end = ',')
                    if nc > 1:
                        fiName = 'splitCompRelation-'+str(c)+'.py'
                        fi = open(fiName,'rb')
                        splitCompRelation = loads(fi.read())
                        fi.close()
                        if Debug:
                            print(c,comp,splitCompRelation)
                        for x in comp:
                            for y in comp:
                                self.relation[x][y] = splitCompRelation[x][y]
                    else:
                        if Debug:
                            print('singleton component %d : %d' % (c,nc))
                            print(comp)                    
                chdir(cwd)
                self.runTimes['postThreading'] = time() - t0 
        else:
            ## without threading using self.relationOrig (CompleteOutranking = True)
            if Comments:
                print('Without threading ...')
            t0 = time()
            for comp in componentsList:
                self._constructComponentRelation(comp)
            self.runTimes['withoutThreading'] = time() - t0
            
        self.runTimes['totalTime'] = time() - ttot
        if Comments:
            print(self.runTimes)

    def computeSortingRelation(self,categoryContents=None,Debug=False):
        """
        constructs a bipolar sorting relation using the category contents.
        """
##        if categoryContents == None:
        componentsList = self._computeQuantileOrdering()
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        actions = [x for x in self.actions]
        currActions = set(actions)
        sortingRelation = {}
        for x in actions:
            sortingRelation[x] = {}
            for y in actions:
                sortingRelation[x][y] = Med
                
        if Debug:
            print('componentsList',componentsList)
        nc = len(componentsList)
        for i in range(nc):
            comp = componentsList[i][1]
            ibch = set(comp)
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


    def _constructComponentRelation(self,comp):
        for x in comp:
            for y in comp:
                self.relation[x][y] = self.relationOrig[x][y]
        
        

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
            strategy = self.sortingParameters['strategy']
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

    def showQuantileOrdering(self,
                             strategy=None,
                             Descending=True,
                             HTML=False,
                             Debug=False):
        """
        *Parameters*:
            * Descending: listing in *decreasing* (default) or *increasing* quantile order.
        
        """
        if strategy == None:
            strategy = self.quantilesOrderingStrategy
        if HTML:
            html = '<h1>Quantiles preordering</h1>'
            html += '<table style="background-color:White;" border="1">'
            html += '<tr bgcolor="#9acd32"><th>quantile limits</th>'
            html += '<th>%s sorting</th>' % strategy
            html += '</tr>'
        actionsCategIntervals = self.decomposition.copy()
        actionsCategIntervals.sort(reverse=Descending)
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
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' % (self.categories[str(item[0][1])]['lowLimit'],\
                                                self.categories[str(item[0][0])]['highLimit'])
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
                                                self.categories[str(item[0][2])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' % (self.categories[str(item[0][2])]['lowLimit'],\
                                                self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )
        if HTML:
            html += '</table>'
            return html

    def showDecomposition(self):
        print('*--- quantiles decomposition in increasing order---*')
        k=1
        for comp in self.decomposition:
            print('%s-%s : %s' % (comp[0][0],comp[0][1],comp[1]))
            k += 1

    def showShort(self):
        """
        concise presentation method for big digraphs.
        """
        print('*----- show short --------------*')
        print('Digraph          :', self.name)
        print('Order            :', self.order)
        print('Size             :', self.size())
        print('Valuation domain :', self.valuationdomain)
        print('# components     :', len(self.decomposition))
        g.showDecomposition()
        print('Constructor run times')
        print('Total time       :', self.runTimes['totalTime'])
        print('QuantilesSorting :', self.runTimes['sorting'])
        print('Preordering      :', self.runTimes['preordering'])
        try:
            print('preThreading     :', self.runTimes['threadPreparing'])
            print('Threading time   :', self.runTimes['threadingTime'])
            print('postThreading    :', self.runTimes['postThreading'])
            
        except:
            print('Without Threads  :', self.runTimes['withoutThreading'])
        
    def _showComponentRelationTable(self,comp,ndigits=2,ReflexiveTerms=False):
        OutrankingDigraph.showRelationTable(self,Sorted=False,
                                            actionsSubset=comp,
                                            #relation=self.relationOrig,
                                            ReflexiveTerms=ReflexiveTerms
                                            )
        
        
    def showRelationTable(self):
        """
        Specialized for showing the quantiles decomposed relation table.
        """
        nc = len(self.decomposition)
        print('%d quantiles decomposed relation table in increasing order' % nc)
        for comp in g.decomposition:
            comp[1].sort()
            print('Component :', comp[1])
            if len(comp[1]) > 1:
                g._showComponentRelationTable(comp[1])


#----------test classes and methods ----------------
if __name__ == "__main__":
    Threading=True
    t = RandomCBPerformanceTableau(numberOfActions=1000,Threading=Threading,seed=100)
    g = BigBipolarOutrankingDigraph(t,quantiles=None,quantilesOrderingStrategy='average',
                                    LowerClosed=False,
                                    Threading=Threading,Debug=False)
    g.showShort()

