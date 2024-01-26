#!/usr/bin/env python3
"""
Digraph3 collection of python3 modules for
Algorithmic Decision Theory applications.

Module for relative and absolute rating of multicriteria performance records 
with abstract *RatingDigraph* root class.

The module, better suitable for rating problems of small sizes (< 500 mulicriteria performance records), reimplements a simpler and more consistent version
of the MP optimised :py:class:`~sortingDigraphs.QuantilesSortingDigraph` and the
:py:class:`~sortingDigraphs.LearnedQuantilesRatingDigraph` classes from the
:py:mod:`sortingDigraphs` module.

Copyright (C) 2016-2023  Raymond Bisdorff.

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

.. note::
    The actions attribute of RatingDigraph instances contains besides the
    standard Digraph.actions (stored in *self.actionsOrig*) also the
    quantile limit profiles (stored in *self.profiles*).

    The *ratingDigraphs* module is not optimised for *BigData* applications.
    In such cases, it is recommended to use instead the
    MP optimised *sortingDigraph* module. 

"""
######### abstract root class
from outrankingDigraphs import BipolarOutrankingDigraph
class RatingDigraph(BipolarOutrankingDigraph):
    """
    Abstract root class with generic private and public methods
    """
    
    def __init__(self):
        print('Abstract root class with private and public methods for RatingDigraph instances')

    def __repr__(self):
        """
        Default presentation method for relative quantiles
        rating digraph instance.
        """
        from decimal import Decimal
        repString =  '*-----  Object instance description -----------*\n'
        repString += 'Instance class      : %s\n' % self.__class__.__name__
        repString += 'Instance name       : %s\n' % self.name
        repString += 'Actions             : %d\n' % len(self.actions)
        repString += 'Criteria            : %d\n' % len(self.criteria)
        repString += 'Quantiles           : %d\n' % len(self.categories)
        repString += 'Lowerclosed         : %s\n' % str(self.criteriaCategoryLimits['LowerClosed'])
        repString += 'Rankingrule         : %s\n' % self.rankingRule
        repString += 'Size                : %d\n' % self.computeSize()
        repString += 'Valuation domain    : [%.2f;%.2f]\n'\
                      % (self.valuationdomain['min'],self.valuationdomain['max'])
        try:
            if self.distribution == 'beta':
                repString += 'Uncertainty model  : %s(a=%.1f,b=%.1f)\n' %\
                    (self.distribution,self.betaParameter,self.betaParameter)
            else:
                repString += 'Uncertainty model    : %s(a=%s,b=%s)\n' %\
                             (self.distribution,'0','2w') 
            repString += 'Likelihood domain    : [-1.0;+1.0]\n'
            repString += 'Confidence level     : %.2f (%.1f%%)\n' %\
                         ( self.bipolarConfidenceLevel,\
                          (self.bipolarConfidenceLevel+1.0)/2.0*100.0 )
            repString += 'Confident majority   : %.2f (%.1f%%)\n' %\
                (self.confidenceCutLevel,\
                (self.confidenceCutLevel+Decimal('1.0'))/Decimal('2.0')*Decimal('100.0'))
        except:
            pass
        repString += 'Determinateness (%%): %.2f\n' %\
                         self.computeDeterminateness(InPercents=True)
        repString += 'Attributes          : %s\n' % list(self.__dict__.keys())
        repString += '*------  Constructor run times (in sec.) ------*\n'
        try:
            repString += 'Threads             : %d\n' % self.nbrThreads
        except:
            self.nbrThreads = 0
            repString += 'Threads             : %d\n' % self.nbrThreads
        try:
            repString += 'StartMethod         : %s\n' % self.startMethod
        except:
            self.startMethod = None
            repString += 'StartMethod         : %s\n' % self.startMethod
        repString += 'Total time          : %.5f\n' % self.runTimes['totalTime']
        repString += 'Data input          : %.5f\n' % self.runTimes['dataInput']
        repString += 'Compute quantiles   : %.5f\n' % self.runTimes['computeProfiles']
        repString += 'Compute outrankings : %.5f\n' % self.runTimes['outrankingRelation']
        repString += 'rating-by-sorting   : %.5f\n' % self.runTimes['sortingRelation']
        repString += 'rating-by-ranking   : %.5f\n' % self.runTimes['rating-by-ranking']
        return repString
    
    def exportRatingBySortingGraphViz(self,fileName=None,direction='decreasing',
                       Comments=True,graphType='png',bgcolor='cornsilk',
                       graphSize='7,7',
                       fontSize=10,
                       relation=None,
                       Debug=False):
        """
        export GraphViz dot file for weak order (Hasse diagram) drawing
        filtering from SortingDigraph instances.
        """
        from copy import deepcopy

        # backup actions and relation        
        relationBkp = deepcopy(self.relation)
        actionsBkp = deepcopy(self.actions)

        # computing rating preorder
        if direction == 'decreasing':
            ordering = self._computeQuantileOrdering(Descending=True)
        else:
            ordering = self._computeQuantileOrdering(Descending=False)
        if Debug:
            print(ordering)
                                
        #  the preorder reltion being transitive
        #  we use the exportGraphViz() method of the TransitiveDigraph class
        self.relation = self._computePreorderRelation(ordering)
        self.actions = self._getActionsKeys()
        if Debug:
            print(self.isTransitive())
        from transitiveDigraphs import TransitiveDigraph
        TransitiveDigraph.exportGraphViz(self,
                                         fileName=fileName,
                                         direction=direction,
                                         Comments=Comments,
                                         graphType=graphType,
                                         bgcolor=bgcolor,
                                         graphSize=graphSize,
                                         fontSize=10)


        # restore original actions and relation
        self.actions = actionsBkp
        self.relation = relationBkp
    
#------------
    def exportRatingByRankingGraphViz(self,fileName=None,
                             Comments=True,graphType='png',
                             graphSize='7,7',
                             fontSize=10,bgcolor='cornsilk',
                             Debug=False):
        """
        export GraphViz dot file for Hasse diagram drawing filtering.
        """
        import os
        from copy import deepcopy
        from decimal import Decimal
            
        def _safeName(t0,QuantileName=False):
            if QuantileName: # graphviz node names must not start with a digit
                t0 = t0[::-1]   
            t = t0.split(sep="-")
            t1 = t[0]
            n = len(t)
            if n > 1:
                for i in range(1,n):
                    t1 += '%s' % (t[i])
            return t1
        
        # working on a deepcopy of self
        digraph = deepcopy(self)
        if Debug:
            print('profile limits:\n',
                  digraph.profileLimits)
            print('relative quantile contents:\n',
                  digraph.relativeCategoryContent)

        # constructing rankingByBestChoosing result
        rankingByChoosing = []
        k = len(digraph.profileLimits)
        if digraph.LowerClosed:
            i = 0
            j = 1
            while i < k:
                rankingByChoosing.append((Decimal('1'),[self.profileLimits[i]]))
                if self.relativeCategoryContent[str(j)] != []:
                    rankingByChoosing.append((Decimal('1'),self.relativeCategoryContent[str(j)]))
                i += 1
                j += 1
        else:
            i = 0
            j = 1
            while i < k:
                if self.relativeCategoryContent[str(j)] != []:
                    rankingByChoosing.append((Decimal('1'),self.relativeCategoryContent[str(j)]))
                rankingByChoosing.append((Decimal('1'),[self.profileLimits[i]]))
                i += 1
                j += 1
        if Debug:
            print(rankingByChoosing)

            
        if Comments:
            print('*---- exporting a dot file for GraphViz tools ---------*')

        # install rating relation (weakly transitive)
        digraph.relation = digraph._computeRatingRelation()
        if Debug:
            print('digraph is transitive ?', digraph.isTransitive())
        
        # sorting actionsKeys
        actionKeys = digraph.computeCopelandRanking()
        n = len(actionKeys)
        
        Med = digraph.valuationdomain['med']
        i = 0
        if fileName is None:
            name = digraph.name+'_ratbyrank'
        else:
            name = fileName
        dotName = name+'.dot'
        if Comments:
            print('Exporting to '+dotName)
        # writing out graphviz instructions
        fo = open(dotName,'w')
        fo.write('digraph G {\n')
        if bgcolor is None:
            fo.write('graph [ ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "')
        else:
            fo.write('graph [ bgcolor = %s, ordering = out, fontname = "Helvetica-Oblique",\n fontsize = 12,\n label = "' % bgcolor)

        fo.write('\\nDigraph3 (graphviz)\\n R. Bisdorff, 2020", size="')
        fo.write(graphSize),fo.write('",fontsize=%d];\n' % fontSize)
        # nodes
        for x in actionKeys:
            #print(digraphClass)
            if x in digraph.profiles:
                cat = digraph.profiles[x]['category']
                if digraph.LowerClosed:
                    nodeName = digraph.categories[cat]['lowLimit'] + ' _'
                else:
                    nodeName = '_ ' +digraph.categories[cat]['highLimit']
                node = '%s [shape = "box", fillcolor=lightcoral, style=filled, label = "%s", fontsize=%d];\n'\
                       % (_safeName(str(x),QuantileName=True),_safeName(nodeName),fontSize)           
            else:
                try:
                    nodeName = digraph.actions[x]['shortName']
                except:
                    nodeName = str(x)
                node = '%s [shape = "circle", label = "%s", fontsize=%d];\n'\
                       % (str(_safeName(x)),_safeName(nodeName),fontSize)
            fo.write(node)
        
        # keep only relation skeleton
        if Debug:
            print(digraph.isTransitive())
        digraph.closeTransitive(Reverse=True,InSite=True)
        if Debug:
        #        actionKeys = digraph.computeCopelandRanking()
            digraph.showRelationMap()

        # write out relations between nodes
        for i in range(n):
            x = actionKeys[i]
            if x in self.profiles:
                xQuantileName=True
            else:
                xQuantileName=False
            for j in range(i+1,n):
                y = actionKeys[j]
                if y in self.profiles:
                    yQuantileName=True
                else:
                    yQuantileName=False
                if digraph.relation[x][y] > digraph.valuationdomain['med']:
                    arcColor = 'black'
                    edge = '%s-> %s [style="setlinewidth(%d)",color=%s] ;\n' %\
                           (_safeName(x,xQuantileName),_safeName(y,yQuantileName),1,arcColor)
                    fo.write(edge)

        fo.write('}\n \n')
        fo.close()
        
        commandString = 'dot -Grankdir=TB -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
            #commandString = 'dot -T'+graphType+' ' +dotName+' -o '+name+'.'+graphType
        if Comments:
            print(commandString)
        try:
            os.system(commandString)
        except:
            if Comments:
                print('graphViz tools not avalaible! Please check installation.')

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
            sorting = self._computeSortingCharacteristics(action=action)
            self.sorting = sorting

        actions = self._getActionsKeys(action)
            
        categories = self._orderedCategoryKeys()

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
                print('%s in %s - %s\t' % (x, self.categories[c]['lowLimit'],
                        self.categories[c]['highLimit'],), end=' ')
                print('%.2f\t\t %.2f\t\t %.2f' %\
                      (sorting[x][c]['lowLimit'],
                       sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
            print()


    def showHTMLRatingByQuantileSorting(self,title='Quantiles Preordering',
                                 Descending=True,strategy='average',
                                 htmlFileName=None):
        """
        Shows the html version of the quantile preordering in a browser window.

        The ordring strategy is either:
            * **average** (default), following the averag of the upper and lower quantile limits,
            * **optimistic**, following the upper quantile limits (default),
            * **pessimistic**, following the lower quantile limits.
            
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        fo.write(self._computeQuantileOrdering(Descending=Descending,
                                              strategy=strategy,
                                              HTML=True,
                                              title=title,
                                              Comments=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)


    def showHTMLSorting(self,Reverse=True,htmlFileName=None):
        """
        shows the html version of the sorting result in a browser window.
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        fo.write(self.showSorting(Reverse=Reverse,isReturningHTML=True))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)


    def showSorting(self,Reverse=True,isReturningHTML=False,Debug=False):
        """
        Shows sorting results in decreasing or increasing (Reverse=False)
        order of the categories. If isReturningHTML is True (default = False)
        the method returns a htlm table with the sorting result.
        
        """
        #from string import replace
        from copy import copy, deepcopy

        try:
            categoryContent = self.relativeCategoryContent
        except:
            categoryContent = self._computeCategoryContents()
            self.relativeCategoryContent = categoryContent

        categoryKeys = self._orderedCategoryKeys(Reverse=Reverse)
        try:
            LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        except:
            LowerClosed = True

        if Reverse:
            print('\n*--- Sorting results in descending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in descending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Quantiles</th><th>Assortment</th></tr>'
        else:
            print('\n*--- Sorting results in ascending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in ascending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Quantiles</th><th>Assortment</th></tr>'

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


    def showAllQuantiles(self):
        self.showCriteriaQuantileLimits()
        
    def showCriteriaQuantileLimits(self,ByCriterion=False):
        """
        Shows category minimum and maximum limits for each criterion.
        """
        catLimits = self.criteriaCategoryLimits
        try:
            LowerClosed = catLimits['LowerClosed']
        except:
            LowerClosed = True
        criteria = self.criteria
        categories = self.categories
        print('Quantile Class Limits (q = %d)' % len(self.categories))
        if LowerClosed:
            print('Lower-closed classes')
        else:
            print('Upper-closed classes')
        
        if ByCriterion:
            nc = len(categories)
            for g in criteria:
                print(g)
                catg = catLimits[g]
                for c in range(1,nc):
                    print('\t%.2f [%.2f; %.2f[' %\
                          (categories[str(c)]['quantile'], catg[c-1], catg[c]) )
        else:
            nc = len(categories)
            print('crit.', end='\t ')
            for c in categories:
                print('%.2f' % (categories[c]['quantile']), end='\t ')
            print('\n*----------------------------------------------')
            for g in criteria:
                print(g, end='\t ')
                catg = catLimits[g]
                for c in range(1,nc+1):
                    print('%.2f' % (catg[c-1]), end='\t ')
                print()

    def showHTMLPerformanceHeatmap(self):
        print('Please use the showHTMLRatingHeatmap() here !!')
    
    def showHTMLRatingHeatmap(self,#actionsList=None,
                                   WithActionNames=False,
                                   #criteriaList=None,
                                   colorLevels=7,
                                   pageTitle=None,
                                   ndigits=2,
                                   rankingRule=None,
                                   Correlations=False,
                                   Threading=False,
                                   nbrOfCPUs=None,
                                   startMethod=None,
                                   Debug=False,
                              htmlFileName=None):
        """
        Specialisation of html heatmap version showing the performance tableau in a browser window;
        see :py:meth:`perfTabs.showHTMLPerformanceHeatMap` method.

        **Parameters**:
              - *ndigits* = 0 may be used to show integer evaluation values.
              - If no *actionsList* is provided, the decision actions are ordered from the best to the worst following the ranking of the LearnedQuatilesRatingDigraph instance.              
              - It may interesting in some cases to use *RankingRule* = 'NetFlows'.
              - With *Correlations* = *True* and *criteriaList* = *None*, the criteria will be presented from left to right in decreasing order of the correlations between the marginal criterion based ranking and the global ranking used for presenting the decision alternatives.
              - Computing the marginal correlations may be boosted with Threading = True, if multiple parallel computing cores are available.
        
        """
        import webbrowser
        if htmlFileName == None:
            from tempfile import NamedTemporaryFile
            fileName = (NamedTemporaryFile(suffix='.html',
                                           delete=False,dir='.')).name
        else:
            from os import getcwd
            fileName = getcwd()+'/'+htmlFileName
        fo = open(fileName,'w')
        if pageTitle is None:
            pageTitle = 'Rating-by-ranking result of \'%s\'' % self.name
        #quantiles = len(self.quantilesFrequencies)
        fo.write(self._htmlRatingHeatmap( #argCriteriaList=criteriaList,
                                          #   argActionsList=actionsList,
                                         WithActionNames=WithActionNames,
                                             #quantiles=quantiles,
                                             ndigits=ndigits,
                                             colorLevels=colorLevels,
                                             pageTitle=pageTitle,
                                             rankingRule=rankingRule,
                                             Correlations=Correlations,
                                             Threading=Threading,
                                             nbrOfCPUs=1,
                                             Debug=Debug))
        fo.close()
        url = 'file://'+fileName
        webbrowser.open(url,new=2)

    def showRatingByQuantilesRanking(self,Descending=True,Debug=False):
        """
        Show rating-by-ranking result.
        """
        
        ratingCategories = self.ratingCategories
        
        print('*-------- rating by quantiles %s ranking result ---------' %\
                     (self.rankingRule) )
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


    def showRatingByQuantilesSorting(self,strategy='average'):
        """
        Dummy show method for the commenting _computeQuantileOrdering() method.
        """
        from decimal import Decimal
        if strategy is None:
            strategy = 'average'
        self._computeQuantileOrdering(strategy=strategy,Comments=True)

    def computeRatingByRankingCorrelation(self,Debug=False):
        from decimal import Decimal
        E = Decimal('0')
        D = Decimal('0')
        ratingRelation = self._computeRatingRelation()

        for q in self.ratingCategories:
            for x in self.actionsOrig:
                #print(q,x)
                #if self.LowerClosed:
                E += min( max(-self.relation[x][q],ratingRelation[x][q]),
                          max(self.relation[x][q],-ratingRelation[x][q]))
                D += min(abs(self.relation[x][q]),abs(ratingRelation[x][q]))

        if Debug:
            print(E,D,E/D)

        nq = len(self.categories)
        na = len(self.actionsOrig)
        return {'correlation':E/D, 'determination': D/Decimal((nq*na))}
    
##    def computeRatingBySortingCorrelation(self,strategy='average',Debug=False):
##        from decimal import Decimal
##        E = Decimal('0')
##        D = Decimal('0')
##        #qspo = self.computePreorderRelation(list(reversed(self._computeQuantileOrdering(strategy=strategy))))
##        qspo = self.computePreorderRelation(self._computeQuantileOrdering(strategy=strategy))
##        #print('qspo',qspo)
##        for q in self.ratingCategories:
##            for x in self.actionsOrig:
##                #if self.LowerClosed:
##                E -= min( max(-self.relation[x][q],qspo[x][q]),\
##                              max(self.relation[x][q],-qspo[x][q]))
##                D += min(abs(self.relation[x][q]),abs(qspo[x][q]))
####                else:
####                    E += min( max(self.relation[q][x],-qspo[q][x]),\
####                              max(-self.relation[q][x],qspo[q][x]))
####                    D += min(abs(self.relation[q][x]),abs(qspo[q][x]))
##        if Debug:      
##            print(E,D,E/D)
##        return E/D


#######  private genric class methods
        
    def _getActionsKeys(self,action=None,withoutProfiles=True):
        """
        extract normal actions keys()
        """
        profiles = set([x for x in self.profiles])
        if action is None:
            actionsExt = set([x for x in self.actions])
            if withoutProfiles:
                return actionsExt - profiles
            else:
                return actionsExt | profiles
        else:
            return set([action])
        
        
    def _computeCategoryContents(self,Reverse=False):
        """
        Computes the sorting results per category.
        """
        actions = list(self._getActionsKeys())
        actions.sort()
        try:
            sorting = self.sorting
        except:
            sorting = self._computeSortingCharacteristics()
        self.sorting=sorting

        categoryContent = {}
        for c in self._orderedCategoryKeys(Reverse=Reverse):
            categoryContent[c] = []
            for x in actions:
                if sorting[x][c]['categoryMembership'] >= self.valuationdomain['med']:
                    categoryContent[c].append(x)
        self.relativeCategoryContent = categoryContent
        
        return categoryContent

    def _computeLimitingQuantiles(self,g,Debug=False,PrefThresholds=True):
        """
        Renders the list of limiting quantiles on criteria g
        """
        from math import floor
        from copy import copy, deepcopy
        from decimal import Decimal
        
        LowerClosed = self.criteriaCategoryLimits['LowerClosed']
        LowerClosed = self.LowerClosed
        criterion = self.criteria[g]
        evaluation = self.evaluation
        NA = self.NA
        actionsOrig = self.actionsOrig
        gValues = []
        
        for x in actionsOrig:
            if Debug:
                print('g,x,evaluation[g][x]',g,x,evaluation[g][x])
            if evaluation[g][x] != NA:
                gValues.append(evaluation[g][x])
        gValues.sort()
        if PrefThresholds:
            try:
                gPrefThrCst = criterion['thresholds']['pref'][0]
                gPrefThrSlope = criterion['thresholds']['pref'][1]
            except:
                gPrefThrCst = Decimal('0')
                gPrefThrSlope = Decimal('0')            
        n = len(gValues)
        if Debug:
            print('g,n,gValues',g,n,gValues)
##        if n > 0:
##        nf = Decimal(str(n+1))
        nf = Decimal(str(n))
        quantilesFrequencies = copy(self.quantilesFrequencies)
        #limitingQuantiles.sort()
        if Debug:
            print(quantilesFrequencies)
        if LowerClosed:
            quantilesFrequencies = quantilesFrequencies[:-1]
        else:
            quantilesFrequencies = quantilesFrequencies[1:]
        if Debug:
            print(quantilesFrequencies)
        # computing the quantiles on criterion g
        gQuantiles = []
        if LowerClosed:
            # we ignore the 1.00 quantile and replace it with +infty
            for q in quantilesFrequencies:
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
            for q in quantilesFrequencies:
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

    def _computePreorderRelation(self,preorder,Normalized=True,Debug=False):
        """
        Renders the bipolar-valued relation obtained from
        a given preordering in increasing levels (list of lists) result.
        """
        from decimal import Decimal
        
        if Normalized:
            Max = Decimal('1')
            Med = Decimal('0')
            Min = Decimal('-1')
        else:   
            Max = self.valuationdomain['max']
            Med = self.valuationdomain['med']
            Min = self.valuationdomain['min']
            
        actions = list(self.actions.keys())
        currentActions = set(actions)
        preorderRelation = {}
        for x in actions:
            preorderRelation[x] = {}
            for y in actions:
                preorderRelation[x][y] = Med

        for eqcl in preorder:
            currRest = currentActions - set(eqcl)
            if Debug:
                print(currentActions, eqcl, currRest)
            for x in eqcl:
                for y in eqcl:
                    if x != y:
                        preorderRelation[x][y] = Med
                        preorderRelation[y][x] = Med

            for x in eqcl:
                for y in currRest:
                    preorderRelation[x][y] = Max
                    preorderRelation[y][x] = Min
            currentActions = currentActions - set(eqcl)
        return preorderRelation

    def _computeQuantileOrdering(self,strategy='average',
                                Descending=True,
                                HTML=False,
                                title='Quantiles Preordering',
                                Comments=False,
                                Debug=False):
        """
        *Parameters*:
            * Descending: listing in *decreasing* (default) or *increasing* quantile order.
            * strategy: ordering in an {'optimistic' | 'pessimistic' | 'average' (default)}
              in the uppest, the lowest or the average potential quantile.
        
        """
        from operator import itemgetter
        if strategy is None:
            strategy = 'optimistic'
        if HTML:
            html = '<h1>%s</h1>\n' % title
            html += '<table style="background-color:White;" border="1">\n'
            html += '<tr bgcolor="#9acd32"><th>quantile limits</th>\n'
            html += '<th>%s sorting</th>\n' % strategy
            html += '</tr>\n'
        actionsCategories = {}
        for x in self.actionsOrig:
            a,lowCateg,highCateg,credibility =\
                     self._showActionCategories(x,Comments=Debug)
            ilowCateg = int(lowCateg)
            ihighCateg = int(highCateg)
            if Debug:
                print(a,lowCateg,highCateg,credibility)
            if strategy == "optimistic":
                try:
                    actionsCategories[(ihighCateg,ilowCateg,ilowCateg)].append(a)
                except:
                    actionsCategories[(ihighCateg,ilowCateg,ilowCateg)] = [a]
            elif strategy == "pessimistic":
                try:
                    actionsCategories[(ilowCateg,ihighCateg,ilowCateg)].append(a)
                except:
                    actionsCategories[(ilowCateg,ihighCateg,ilowCateg)] = [a]
            elif strategy == "average":
                lc = float(lowCateg)
                hc = float(highCateg)
                ac = (lc+hc)/2.0
                try:
                    actionsCategories[(ac,ihighCateg,ilowCateg)].append(a)
                except:
                    actionsCategories[(ac,ihighCateg,ilowCateg)] = [a]
            else:
                print('Error: %s not a valid ordering strategy !!!' % strategy)
                break
                
        # sorting the quantile equivalence classes
        actionsCategoriesKeys = [key for key in actionsCategories]
        actionsCategoriesKeys = sorted(actionsCategoriesKeys,key=itemgetter(0,1,2), reverse=True)
        actionsCategIntervals = []
        for interval in actionsCategoriesKeys:
            actionsCategIntervals.append([interval,\
                                          actionsCategories[interval]])

        # gathering the result with output when Comments=True
        weakOrdering = []
        if Comments and not HTML:
            print('*---- rating by quantiles sorting result----*')
        for item in actionsCategIntervals:
            #print(item)
            if Comments:
                if strategy == "optimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><tdbgcolor="#FFF79B">%s-%s</td>' \
                                % (self.categories[str(item[0][1])]['lowLimit'],
                                   self.categories[str(item[0][0])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' \
                                  % (self.categories[str(item[0][1])]['lowLimit'],
                                     self.categories[str(item[0][0])]['highLimit'],
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' \
                                % (self.categories[str(item[0][0])]['lowLimit'],
                                   self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])                            
                        else:
                            print('%s-%s : %s' \
                                  % (self.categories[str(item[0][1])]['lowLimit'],
                                     self.categories[str(item[0][0])]['highLimit'],\
                                                str(item[1])) )
                elif strategy == "pessimistic":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' \
                                % (self.categories[str(item[0][0])]['lowLimit'],
                                   self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' \
                                  % (self.categories[str(item[0][0])]['lowLimit'],
                                     self.categories[str(item[0][1])]['highLimit'],
                                                 str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' \
                                % (self.categories[str(item[0][0])]['lowLimit'],
                                   self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])

                        else:
                            print('%s-%s : %s'\
                                  % (self.categories[str(item[0][0])]['lowLimit'],
                                     self.categories[str(item[0][1])]['highLimit'],\
                                                str(item[1])) )                   
                elif strategy == "average":
                    if self.criteriaCategoryLimits['LowerClosed']:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' \
                                % (self.categories[str(item[0][2])]['lowLimit'],
                                   self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' \
                                  % (self.categories[str(item[0][2])]['lowLimit'],
                                     self.categories[str(item[0][1])]['highLimit'],
                                                str(item[1])) )
                    else:
                        if HTML:
                            html += '<tr><td bgcolor="#FFF79B">%s-%s</td>' \
                                % (self.categories[str(item[0][2])]['lowLimit'],
                                   self.categories[str(item[0][1])]['highLimit'])
                            html += '<td>%s</td></tr>' % str(item[1])
                        else:
                            print('%s-%s : %s' \
                                  % (self.categories[str(item[0][2])]['lowLimit'],
                                     self.categories[str(item[0][1])]['highLimit'],
                                                str(item[1])) )
            weakOrdering.append(item[1])
        if HTML:
            html += '</table>'
            return html
        else:
            return weakOrdering
            
    def _computeQuantilesFrequencies(self,x,Debug=False):
        """
        renders the quantiles frequencies
        """
        from math import floor
        from decimal import Decimal
        
        if isinstance(x,int):
            n = x
        elif x is None:
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

        quantilesFrequencies = []
        for i in range(n+1):
            quantilesFrequencies.append( Decimal(str(i)) / Decimal(str(n)) )
        #self.name = 'sorting_with_%d-tile_limits' % n
        return quantilesFrequencies

    def _computeQuantilesRatingByRanking(self,Debug=False):
        """
          Renders an ordered dictionary of non empty quantiles in ascending order.
        """
        from collections import OrderedDict
        
        ranking = list(self.actionsRanking)
        if self.LowerClosed: # lower closed quantiles
            ranking.reverse()
        if Debug:
            print('9.1')
            print(ranking)
        
        n = len(ranking)
        ratingCategories = OrderedDict()
        if ranking[0] in self.actionsOrig:
            ranking[0],ranking[1] = ranking[1],ranking[0]
            if Debug:
                print('swapping',ranking)
        New = True
        for i in range(n):
            if ranking[i] in self.actionsOrig:
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

    def _computeRatingRelation(self,Debug=False,StoreRating=True):
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

        ratingRelation = self._computePreorderRelation(preRanking)

        if StoreRating:
            self.ratingRelation = ratingRelation
        return ratingRelation

    def _computeSortingRelation(self,categoryContents=None,Debug=False):
        """
        constructs a bipolar sorting relation using the category contents.
        """
        try:
            categoryContents = self.categoryContent
        except:
            pass
        if categoryContents is None:
            categoryContents = self._computeCategoryContents()
        Max = self.valuationdomain['max']
        Med = self.valuationdomain['med']
        Min = self.valuationdomain['min']
        #actions = [x for x in self.actionsOrig]
        actions = self._getActionsKeys()
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
    
    def _computeSortingCharacteristics(self, action=None, Comments=False):
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

        actions = self._getActionsKeys(action)
            
        categories = self._orderedCategoryKeys()

        try:
            #LowerClosed = self.criteriaCategoryLimits['LowerClosed']
            LowerClosed = self.LowerClosed
        except:
            LowerClosed = True

        if Comments:
            if LowerClosed:
                print('x  in  K_k\t r(x >= m_k)\t r(x < M_k)\t r(x in K_k)')
            else:
                print('x  in  K_k\t r(m_k < x)\t r(M_k >= x)\t r(x in K_k)')

        sorting = {}
        nq = len(self.quantilesFrequencies) - 1
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
                    print('%s in %s - %s\t' \
                          % (x, self.categories[c]['lowLimit'],
                             self.categories[c]['highLimit'],), end=' ')
                categoryMembership = min(lowLimit,notHighLimit)
                sorting[x][c]['lowLimit'] = lowLimit
                sorting[x][c]['notHighLimit'] = notHighLimit
                sorting[x][c]['categoryMembership'] = categoryMembership

                if Comments:
                    #print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))
                    print('%.2f\t\t %.2f\t\t %.2f\n' \
                          % (sorting[x][c]['lowLimit'],
                             sorting[x][c]['notHighLimit'],
                             sorting[x][c]['categoryMembership']))

        return sorting

    def _htmlRatingHeatmap(self, argCriteriaList=None,
                               argActionsList=None,
                               WithActionNames=False,
                               #quantiles=None,
                               ndigits=2,
                               contentCentered=True,
                               colorLevels=None,
                               pageTitle='Rating Heatmap',
                               rankingRule=None,
                               Correlations=False,
                               Threading=False,
                               startMethod=None,
                               nbrOfCPUs=None,
                               Debug=False):
        """       
        Renders the Brewer RdYlGn 5,7, or 9 levels colored heatmap of the performance table
        actions x criteria in html format.

        See the corresponding :py:meth:`perfTabs.showHTMLPerformanceHeatMap` method.
        """
        print('see browser')
        from decimal import Decimal
        from operator import itemgetter
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
        if colorLevels is None:
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
        html += '<title>%s</title>\n' % 'Rating heat map'
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
        if argCriteriaList is None:
            argCriteriaList = list(self.criteria.keys())
            criteriaList = None
        else:
            criteriaList = argCriteriaList

        if rankingRule is None:
            if argActionsList is None:
                actionsList = self.actionsRanking
                rankingRule = self.rankingRule
            else:
                actionsList = argActionsList
                rankingRule = self.rankingRule
        else:
            if argActionsList is None:
                if rankingRule == 'Copeland':
                    actionsList = self.computeCopelandRanking()
                elif rankingRule == 'NetFlows':
                    actionsList = self.computeNetFlowsRanking()
            else:
                rankingRule = None
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
        if criteriaList is None:
            if Correlations:
                criteriaCorrelation =\
                        self.computeMarginalVersusGlobalRankingCorrelations(
                            actionsList,ValuedCorrelation=True,
                            Threading=Threading,startMethod=startMethod,
                            nbrCores=nbrOfCPUs)
                criteriaList = [c[1] for c in criteriaCorrelation]
            else:
                criteriaList = list(criteria.keys())
                criteriaList.sort()
                criteriaWeightsList = [(abs(criteria[g]['weight']),g) for g in criteriaList]
                criteriaWeightsList.sort(reverse=True,key=itemgetter(0))
                criteriaList = [g[1] for g in criteriaWeightsList]
                criteriaCorrelation = None
        else:
            criteriaList = list(criteria.keys())
            if Correlations:
                criteriaCorrelation =\
                        self.computeMarginalVersusGlobalRankingCorrelations(
                            actionsList,ValuedCorrelation=True,
                            Threading=Threading,
                            startMethod=startMethod,    
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
        if criteriaCorrelation is not None:
            html += '<tr><th bgcolor=%s>tau<sup>(*)</sup></th>' % (columnHeaderColor)
            for cg in criteriaCorrelation:
                html += '<td align="center">%+.2f</td>' % (cg[0])
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
                if WithActionNames:
                    xName = self.actions[x]['name']
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
                if self.evaluation[g][x] != self.NA:
                    formatString = '<td bgcolor=%s align="right">%% .%df</td>' \
                        % (quantileColor[x][g],ndigits)
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
        if criteriaCorrelation is not None:
            html += '<i>(*) tau: Ordinal (Kendall) correlation between</i><br/>'
            html += '<i>marginal criterion and global ranking relation.</i><br/>\n'
##        if rankCorrelation is not None:
##            html += '<i>Ordinal (Kendall) correlation between global ranking and outranking relation: %.2f.</i>' % (rankCorrelation['correlation'])
        html += '</body></html>'
        return html

    def _orderedCategoryKeys(self,Reverse=False):
        """
        Renders the ordered list of category keys
        based on self.categories['order'] numeric values.
        """
        orderedCategoryKeys = list(self.categories.keys())
        if Reverse:
            orderedCategoryKeys.reverse()
        return orderedCategoryKeys

    def _showActionCategories(self,action,Debug=False,Comments=True):
        """
        Renders the union of categories in which the given action is sorted positively or null into.
        Returns a tuple : action, lowest category key, highest category key, membership credibility !
        """
        Med = self.valuationdomain['med']
        try:
            sorting = self.sorting
        except:
            sorting = self._computeSortingCharacteristics(action=action,\
                                                     Comments=Debug)
        catKeys = self._orderedCategoryKeys()
        keys = [catKeys[0],[catKeys[-1]]]
        lowLimit = sorting[action][catKeys[0]]['lowLimit']
        notHighLimit = sorting[action][catKeys[-1]]['lowLimit']
        for c in self._orderedCategoryKeys():
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

#########   relative quantiles raking
from perfTabs import PerformanceTableau 
class RatingByRelativeQuantilesDigraph(RatingDigraph,PerformanceTableau):
    """
    Constructor for a relative quantiles rating-by sorting and rating-by-ranking digraph.
    See the :py:class:`sortingDigraphs.QuantilesSortingDigraph` class.

    **Parameters**

       * *argPerfTab*: valid stored PerformanceTableau instance,
        
       * *quantiles*: integer number of quantile classes,
        
       * *LowerClosed*:  {True | False (default upper closed quantiles)},
        
       * *rankingRule*: 'NetFlows' (default).

       * *outrankingModel*: {'standard' (default) | 'confident' | 'robust' | 'mp' },

          Parameters for the *confident* outranking model: 

          *distribution*: {'triangular' (default)| 'uniform' | 'beta'},
        
          *betaParameter* : 2 (default), 
        
          *confidence*: alpha% confidence level (in percents, 90.0 default).
 
       * If *Threading* is set to *True*, or *outrankingModel* is set to 'mp',
         mind that when running from a script file, the main program code entry
         must start with a __name__=='__main__' test.
        
 
    Example usage:

    >>> # generating random multicriteria performance records
    >>> from randomPerfTabs import RandomPerformanceTableau
    >>> pt = RandomPerformanceTableau(numberOfActions=50,seed=3)
    >>> # rating-by-sorting with relative quantiles
    >>> from ratingDigraphs import RatingByRelativeQuantilesDigraph
    >>> g = RatingByRelativeQuantilesDigraph(pt,7,LowerClosed=True)
    >>> g.showRatingByQuantileSorting(strategy='average')
        *---- rating by quantiles sorting result----*
        [0.71-<[ : ['a07']
        [0.71-0.86[ : ['a08', 'a48']
        [0.57-0.71[ : ['a04', 'a06', 'a09', 'a12', 'a19', 'a23',
                       'a27', 'a33', 'a38', 'a39', 'a43']
        [0.43-0.71[ : ['a11', 'a18']
        [0.43-0.57[ : ['a03', 'a20', 'a22', 'a29', 'a30', 'a31',
                       'a41', 'a47', 'a49']
        [0.29-0.57[ : ['a01', 'a26', 'a46', 'a50']
        [0.29-0.43[ : ['a05', 'a10', 'a13', 'a16', 'a17', 'a21',
                       'a28', 'a32', 'a37']
        [0.14-0.43[ : ['a40']
        [0.14-0.29[ : ['a15', 'a24', 'a25', 'a34', 'a35', 'a36',
                       'a42', 'a44', 'a45']
        [0.00-0.29[ : ['a14']
        [0.00-0.14[ : ['a02']
    >>> g.showRatingByQuantilesRanking()
        *-------- rating by quantiles ranking result ---------
        [0.57 - 0.71[ ['a48', 'a23', 'a07']
        [0.43 - 0.57[ ['a04', 'a27', 'a33', 'a38', 'a09', 'a08',
                       'a41', 'a11', 'a06', 'a46', 'a19', 'a47',
                       'a49', 'a39', 'a43', 'a12', 'a22', 'a20',
                       'a32']
        [0.29 - 0.43[ ['a01', 'a18', 'a17', 'a37', 'a16', 'a30',
                       'a31', 'a21', 'a50', 'a05', 'a29', 'a02',
                       'a13', 'a26', 'a40']
        [0.14 - 0.29[ ['a03', 'a42', 'a28', 'a10', 'a36', 'a45',
                       'a44', 'a34', 'a25', 'a24', 'a35', 'a14',
                       'a15']

    """

    def __init__(self,argPerfTab,
                 quantiles=None,
                 LowerClosed=False,
                 outrankingModel='standard',
                 distribution='triangular',
                 betaParameter=2,
                 confidence=90.0,
                 rankingRule='NetFlows',
                 Threading=False,
                 startMethod=None,
                 nbrCores=None,
                 CopyPerfTab=True,
                 Debug=False):
        
        from time import time
        from copy import copy, deepcopy
        if CopyPerfTab:
            copy2self = deepcopy
        else:
            copy2self = copy
        from decimal import Decimal

        # import the performance tableau
        tt = time()
        if argPerfTab is None:
            print('Error: a valid performance tableau is required!')
        else:
            perfTab = argPerfTab

        # naming the digraph instance
        self.name = 'relative_rating_%s' % (perfTab.name) 

        # normalize the actions as a dictionary construct
        from collections import OrderedDict
        if isinstance(perfTab.actions,list):
            actions = OrderedDict()
            for x in perfTab.actions:
                actions[x] = {'name': str(x)}
        else:
            actions = copy2self(perfTab.actions)
        self.actions = actions

        # keep a copy of the original actions set before adding the profiles
        actionsOrig = OrderedDict(actions)
        self.actionsOrig = actionsOrig

        #  normalizing the performance tableau
        from perfTabs import NormalizedPerformanceTableau
        normPerfTab = NormalizedPerformanceTableau(perfTab)

        # instantiating the performance tableau part
        criteria = normPerfTab.criteria
        self.criteria = criteria
        self.convertWeight2Decimal()
        evaluation = normPerfTab.evaluation
        self.evaluation = evaluation
        self.NA = copy2self(perfTab.NA)
        self.convertEvaluation2Decimal()
        self.runTimes = {'dataInput': time()-tt}
        
        #  compute the limiting quantiles
        t0 = time()
        if isinstance(quantiles,list):
            #self.name = 'sorting_with_given_quantiles'
            quantilesFrequencies = []
            for x in quantiles:
                quantilesFrequencies.append(Decimal(str(x)))
            if Debug:
                print('convert to decimal!',quantilesFrequencies)
        else:
            quantilesFrequencies = self._computeQuantilesFrequencies(quantiles,Debug=Debug)
        self.quantilesFrequencies = quantilesFrequencies

        if Debug:
            print('quantilesFrequencies',self.quantilesFrequencies)
        # supposing all criteria scales between 0.0 and 100.0
        # with preference direction = max
        self.LowerClosed = LowerClosed
        lowValue = 0.0
        highValue = 100.00
        categories = OrderedDict()
        k = len(quantilesFrequencies)-1
        if LowerClosed:
            for i in range(0,k-1):
                categories[str(i+1)] = {'name':'[%.2f - %.2f['\
                %(quantilesFrequencies[i],quantilesFrequencies[i+1]),\
                                'order':i+1,\
                                'lowLimit': '[%.2f' % (quantilesFrequencies[i]),
                                'highLimit': '%.2f[' % (quantilesFrequencies[i+1]),
                                        'quantile': quantilesFrequencies[i]}
            categories[str(k)] = {'name':'[%.2f - <['\
                %(quantilesFrequencies[k-1]), 'order':k,\
                                  'lowLimit': '[%.2f' % (quantilesFrequencies[k-1]),\
                                  'highLimit': '<[',
                                'quantile': quantilesFrequencies[k-1] }                 
        else:
            categories[str(1)] = {'name':']< - %.2f]'\
                %(quantilesFrequencies[1]), 'order':1,
                    'highLimit': '%.2f]' % (quantilesFrequencies[1]),\
                    'lowLimit': ']<',
                    'quantile': quantilesFrequencies[1]}                                  
            for i in range(1,k):
                categories[str(i+1)] = {'name':']%.2f - %.2f]'\
                %(quantilesFrequencies[i],quantilesFrequencies[i+1]), 'order':i+1,
                        'lowLimit': ']%.2f' % (quantilesFrequencies[i]),
                        'highLimit': '%.2f]' % (quantilesFrequencies[i+1]),
                                        'quantile': quantilesFrequencies[i+1]}
        self.categories = categories
        if Debug:
            print('categories',self.categories)
            print('list',list(dict.keys(categories)))

        criteriaCategoryLimits = {}
        criteriaCategoryLimits['LowerClosed'] = LowerClosed
        self.criteriaCategoryLimits = criteriaCategoryLimits
        self.limitingQuantiles = criteriaCategoryLimits
        for g in dict.keys(criteria):
            gQuantiles = self._computeLimitingQuantiles(g,\
                            PrefThresholds=True,Debug=Debug)
##            if Debug:
##                print(g,gQuantiles)
            criteriaCategoryLimits[g] = gQuantiles
        self.criteriaCategoryLimits = criteriaCategoryLimits
        self.limitingQuantiles = criteriaCategoryLimits
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
                    evaluation[g][cKey] = Decimal(str(criteriaCategoryLimits[g][int(c)-1]))

        self.profiles = profiles
        profileLimits = list(profiles.keys())
        #profileLimits.sort()
        self.profileLimits = profileLimits
        self.order = len(actions) # actionsOrig + profiles
        
        if Debug:
            print('self.profiles',profiles)
            print('self.profileLimits',profileLimits)
            
        self.runTimes['computeProfiles'] = time() - t0

        # construct quantile limits extended outranking relation
        t0 = time()
##        if nbrCores=None:
##            self.nbrThreads = 1
##        else:
##            self.nbrThreads = nbrCores
        if outrankingModel == 'mp':
            import os
            from perfTabs import PerformanceTableau
            PerformanceTableau.save(self,'sharedPerfTab')
            while not os.path.exists('./sharedPerfTab.py'):
                pass
            from mpOutrankingDigraphs import MPBipolarOutrankingDigraph
            g = MPBipolarOutrankingDigraph(self,Normalized=True,
                                           startMethod=startMethod,
                                           nbrCores=nbrCores)
            self.nbrThreads = copy2self(g.nbrThreads)
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)
        if outrankingModel == 'standard':
            from outrankingDigraphs import BipolarOutrankingDigraph
            g = BipolarOutrankingDigraph(self,
                                    Threading=Threading,
                                    startMethod=startMethod,
                                    nbrCores=nbrCores)
            #self.nbrThreads = copy2self(g.nbrThreads)
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)
            self.nbrThreads = copy2self(g.nbrThreads)
        elif outrankingModel == 'confident':
            from outrankingDigraphs import ConfidentBipolarOutrankingDigraph
            g = ConfidentBipolarOutrankingDigraph(self,
                                distribution=distribution,
                                betaParameter=betaParameter,
                                confidence=confidence,
                                )
            self.nbrThreads = 0
            self.startMethod = None
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)
            self.bipolarConfidenceLevel = copy2self(g.bipolarConfidenceLevel)
            self.confidenceCutLevel = copy2self(g.confidenceCutLevel)
            self.distribution = copy2self(g.distribution)
            self.betaParameter = copy2self(g.betaParameter)
            self.likelihoods = copy2self(g.likelihoods)
        elif outrankingModel == 'robust':
            from outrankingDigraphs import RobustOutrankingDigraph
            g = RobustOutrankingDigraph(self)
            self.nbrThreads = 0
            self.startMethod = None,
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)
            self.stability = copy2self(g.stability)
            
        self.runTimes['outrankingRelation'] = time() - t0

        # compute quantiles by sorting
        t0 = time()
        self.sortingRelation = self._computeSortingRelation(
            Debug=Debug)
        self.runTimes['sortingRelation'] = time() - t0

        # compute rating-by-ranking
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
        elif rankingRule == 'NetFlows':
            from linearOrders import NetFlowsOrder
            nf = NetFlowsOrder(g)
            actionsList = nf.netFlowsRanking
            self.rankingRule = 'NetFlows'
            self.rankingScores = nf.decnetFlowScores
        elif rankingRule == 'RankedPairs':
            from linearOrders import RankedPairsRanking
            rp = RankedPairsRanking(g)
            actionsList = rp.rankedPairsRanking
            self.rankingRule = 'RankedPairs'
            self.rankingScores = None
        elif rankingRule == 'IteratedCopeland':
            from linearOrders import IteratedCopelandRanking
            rp = IteratedCopelandRanking(g)
            actionsList = rp.iteratedCopelandRanking
            self.rankingRule = 'IteratedCopeland'
            self.rankingScores = None
        elif rankingRule == 'IteratedNetFlows':
            from linearOrders import IteratedNetFlowsRanking
            rp = IteratedNetFlowsRanking(g)
            actionsList = rp.iteratedNetFlowsRanking
            self.rankingRule = 'IteratedNetFlows'
            self.rankingScores = None
##        elif rankingRule == 'Kemeny':
##            if g.order > 12:
##                print('Error: the digraph is to big for the Kemeny ranking rule üüü')
##            else:
##                from linearOrders import KemenyRanking
##                ke = KemenyRanking(g, orderLimit=g.order)
##                actionsList = ke.kemenyRanking
##                self.rankingRule = 'Kemeny'
##                self.rankingScores = None
        else:
            print('Errr: The ranking rule %s is not availbale !!' % rankingRule)
        if rankingRule != 'best':
            self.rankingCorrelation = g.computeRankingCorrelation(actionsList)
        self.actionsRanking = actionsList
        if Debug:
            print('6.')
            print('*',self.actionsRanking)
        self.ratingCategories = self._computeQuantilesRatingByRanking(Debug=Debug)
        if Debug:
            print('7.')
            print('Ranking rule        :', self.rankingRule)
            print('Actions ranking     :', self.actionsRanking)
            print('Ranking correlation :', self.rankingCorrelation)
            print('Rating categories:', self.ratingCategories)
        self.runTimes['rating-by-ranking'] = time() - t0
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['totalTime'] = time()-tt

 
#.....  specific relative rating class methods  ....
        
    def _computeMarginalRatingCorrelations(self,Debug=False):
        from perfTabs import PartialPerformanceTableau
        from digraphs import BipartitePartialDigraph
        from linearOrders import NetFlowsRanking,CopelandRanking
        #nf = NetFlowsRanking(self)
        #cop = CopelandRanking(self)
        bp = BipartitePartialDigraph(self,self.actionsOrig,self.profiles)
        marginalCorrelations = {}
        for g in self.criteria:
            #print(g)
            ptg = PartialPerformanceTableau(self,criteriaSubset=[g])
            #print(ptg)
            q = len(self.categories)
            selfg = RatingByRelativeQuantilesDigraph(ptg,quantiles=q,
                                    LowerClosed=self.LowerClosed)
            #print(selfg)
            bpg = BipartitePartialDigraph(selfg,self.actionsOrig,self.profiles)
            marginalCorrelations[g] = bp.computeOrdinalCorrelation(bpg)
            if Debug:
                print(g,marginalCorrelations[g])
        return marginalCorrelations   

    def _computeRatingConsensusQuality(self,Comments=False):
        """
        Renders the marginal criteria correlations with a given rating with summary.
        """
        #from outrankingDigraphs import BipolarOutrankingDigraph
        from math import sqrt
        from decimal import Decimal
        #g = BipolarOutrankingDigraph(self,Normalized=True)
        criteria = self.criteria
        marginalCorrelation =\
                        self._computeMarginalRatingCorrelations()
        ncrit = Decimal(str(len(marginalCorrelation)))
        meanMarginalCorrelation = Decimal('0.0')
        varMarginalCorrelation = Decimal('0.0')
        sumWeights = Decimal('0.0')
        for cg in marginalCorrelation:
            sumWeights += abs(criteria[cg]['weight'])
        for cg in marginalCorrelation:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg]['weight'])/sumWeights
            meanMarginalCorrelation += marginalCorrelation[cg]['correlation']*cgw
        for cg in marginalCorrelation:
            #if cg[0] < Decimal('0'):
            cgw = abs(criteria[cg]['weight'])/sumWeights
            varMarginalCorrelation +=\
                ((marginalCorrelation[cg]['correlation']-meanMarginalCorrelation)**2)*cgw
        sdMarginalCorrelation = sqrt(varMarginalCorrelation) 
        # showing the results
        if Comments:
            print('Consensus quality of rating:')
            print('criterion (weight): tau (deter.) equiv.')
            print('----------------------------------------')
            for cg in sorted(marginalCorrelation):
                print('%s (%.3f): \t %+.3f (%+.3f) %+.3f' %\
                      (cg,abs(criteria[cg]['weight'])/sumWeights,
                       marginalCorrelation[cg]['correlation'],
                       marginalCorrelation[cg]['determination'],
                       marginalCorrelation[cg]['correlation'] *\
                                  marginalCorrelation[cg]['determination']) )
            print('Summary:')
            print('Weighted mean marginal correlation (a): %+.3f' % meanMarginalCorrelation)
            print('Standard deviation (b)                : %+.3f' % sdMarginalCorrelation)
            print('Ranking fairness (a)-(b)              : %+.3f' %\
                  (float(meanMarginalCorrelation) - sdMarginalCorrelation) )
        return (marginalCorrelation,meanMarginalCorrelation,sdMarginalCorrelation)

    def showRatingConsensusQuality(self):
        self._computeRatingConsensusQuality(Comments=True)
    

#########################################
#########   learned quantiles rating
from performanceQuantiles import PerformanceQuantiles
class RatingByLearnedQuantilesDigraph(RatingDigraph,PerformanceQuantiles):
    """
    Constructor for a learned quantiles rating-by sorting and rating-by-ranking digraph.
    See the :py:class:`sortingDigraphs.LearnedQuantilesRatingDigraph` class.
    
    **Parameters**

    *argPerfQuantiles*: valid stored :py:class:`~performanceQuantiles.PerformanceQuantiles` instance,

    *newData*: new random actions or performance tableau
    generated with the :py:class:`~randomPerfTabs.RandomPerformanceGenerator` class,
        
    *quantiles*: integer number of quantile classes,
        
    *LowerClosed*:  {True | False (default upper closed quantiles)},
        
    *rankingRule*: 'NetFlows' (default).

    *outrankingModel*: {'standard' (default) | 'mp' | 'confident' | 'robust'},

        Parameters for the *confident* outranking model: 

        *distribution*: {'triangular' (default)| 'uniform' | 'beta'},
        
        *betaParameter* : 2 (default), 
        
        *confidence*: alpha% confidence level (in percents, 90.0 default).

     Example usage:

    >>> # generating random historical performance records and quantiles
    >>> from randomPerfTabs import RandomPerformanceTableau
    >>> hpt = RandomPerformanceTableau(numberOfActions=1000,seed=1)
    >>> from performanceQuantiles import PerformanceQuantiles
    >>> pq = PerformanceQuantiles(hpt,numberOfBins=7,LowerClosed=True,Debug=False)
    >>> # generating new incoming performance records of the same kind
    >>> from randomPerfTabs import RandomPerformanceGenerator
    >>> tpg = RandomPerformanceGenerator(hpt,instanceCounter=0,seed=1)
    >>> newRecords = tpg.randomActions(10)
    >>> # updating the historical performance quantiles
    >>> pq.updateQuantiles(newRecords,historySize=None)
    >>> # rating the new set of performance records after
    >>> from ratingDigraphs import RatingByLearnedQuantilesDigraph
    >>> lqr = RatingByLearnedQuantilesDigraph(pq,newRecords,Debug=False)
    >>> lqr.showRatingByQuantilesSorting(strategy='average')
        *---- rating by quantiles sorting result----*
        [0.86-<[ : ['a06']
        [0.71-0.86[ : ['a04']
        [0.57-0.71[ : ['a07']
        [0.43-0.57[ : ['a03', 'a05', 'a08']
        [0.29-0.43[ : ['a02', 'a09']
        [0.14-0.29[ : ['a01', 'a10']
    >>> lqr.showRatingByQuantilesRanking(Descending=True)
        *-------- rating by quantiles ranking result ---------
        [0.57 - 0.71[ ['a06']
        [0.43 - 0.57[ ['a07', 'a04', 'a05', 'a09']
        [0.29 - 0.43[ ['a08', 'a03', 'a02', 'a01']
        [0.14 - 0.29[ ['a10']

.. note:: Mind that when setting *Threading* to *True* in a Python script file,
   the main program code entry must start with a *__name__=='__main__'* test
   in order to avoid recursive execution of the submitted script.

    """

    def __init__(self,argPerfQuantiles=None,
                 newData=None,
                 quantiles=None,
                 #hasNoVeto=False,
                 rankingRule='NetFlows',
                 outrankingModel='standard',
                 distribution='triangular',
                 betaParameter=2,
                 confidence=90.0,
                 Threading=False,
                 startMethod=None,
                 nbrCores=None,
                 CopyPerfTab=True,
                 Debug=False):
        
        from time import time
        from copy import copy, deepcopy
        from collections import OrderedDict
        from decimal import Decimal
        
        if CopyPerfTab:
            copy2self = deepcopy
        else:
            copy2self = copy

        # import init parameters
        self.rankingRule = rankingRule
        self.outrankingModel = outrankingModel
        if outrankingModel == 'confident':
            self.distribution = distribution
            self.betaParameter = betaParameter
            self.confidence = confidence
        
        # import the performance quantiles
        self.runTimes = {}
        tt = time()
        if argPerfQuantiles is None:
            print('Error: valid PerformanceQuantiles instance is required!')
            return
        else:
            self.perfQuantiles = copy2self(argPerfQuantiles)
            
        # instantiating the performance quantiles part
        try:
            self.objectives = self.perfQuantiles.objectives
        except:
            pass
        self.criteria = self.perfQuantiles.criteria
        self.LowerClosed = self.perfQuantiles.LowerClosed
        self.quantilesFrequencies = self.perfQuantiles.quantilesFrequencies
        self.criteriaCategoryLimits = self.perfQuantiles.limitingQuantiles
        self.limitingQuantiles = self.perfQuantiles.limitingQuantiles
        self.historySizes = self.perfQuantiles.historySizes
        self.cdf = self.perfQuantiles.cdf
        self.NA = self.perfQuantiles.NA
        self.name = 'learnedRatingDigraph'

        # import the actions to rate
        if newData is not None:
            self.newData = copy2self(newData)
            try:  # randomActions format {'actions': .., 'evaluation':..}
                self.newActions = self.newData['actions']
                self.evaluation = self.newData['evaluation']
                ## need NA to found somewhere !!!
            except:
                try:  #  randomPerformanceTableau format
                    self.newActions = self.newData.actions
                    self.evaluation = self.newData.evaluation
                except:
                    print('Error !!!: valid new Actions or valid new PerformanceTableau required')
        else:
            print('Error !!!: newly observed decision actions with performance evaluations are required !!')
            return
        self.actionsOrig = self.newActions
        self.actions = copy2self(self.newActions)
        
        self.runTimes['dataInput'] = time()-tt

        # check if new quantile limits should be interpolated
        t0 = time()
        self.quantiles = quantiles
        if quantiles is not None:
            oldFreq = self.quantilesFrequencies
            newFreq = self._computeQuantilesFrequencies(quantiles)
            newLimitingQuantiles = {}
            for g in self.criteria:
                newLimitingQuantiles[g] = []
            for p in newFreq:
                if Debug:
                    print('p,oldFreq',p,oldFreq)
                newQuantiles = self.computeQuantileProfile(p,oldFreq)
                for g in self.criteria:
                    newLimitingQuantiles[g].append(newQuantiles[g])
            self.criteriaCategoryLimits = newLimitingQuantiles
            self.limitingQuantiles = newLimitingQuantiles
            self.quantilesFrequencies = newFreq
            
        # rating categories
        t0 = time()
        LowerClosed = self.LowerClosed
        quantFreq = self.quantilesFrequencies
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
            print('3.')
            print('categories',self.categories)
            print('list',list(dict.keys(categories)))

        # set the category limits type (LowerClosed = True is default)
        self.criteriaCategoryLimits['LowerClosed'] = self.LowerClosed
        criteriaCategoryLimits = self.criteriaCategoryLimits

        # add the profiles, ie quantile limits, to the actions set
        criteria = self.criteria
        profiles = OrderedDict()
        actions = self.actions
        for c in categories:
##            if LowerClosed:
##                cKey = c+'-m'
##            else:
##                cKey = c+'-M'
            if LowerClosed:
                cKey = c+'-m'
                actions[cKey] = {'name': 'categorical low limits',
                                 'comment': 'Inferior or equal limits for category membership assessment'}
                profiles[cKey] = {'category': c, 'name': categories[c]['lowLimit'] + ' -',\
                                  'comment': 'Inferior or equal limits for category membership assessment'}
            else:
                cKey = c+'-M'
                actions[cKey] = {'name': 'categorical high limits',
                                 'comment': 'Lower or equal limits for category membership assessment'}
                profiles[cKey] = {'category': c, 'name': '- ' + categories[c]['highLimit'],\
                                  'comment': 'Lower or equal limits for category membership assessment'}
            for g in criteria:
                if Debug:
                    print('criteriaCategoryLimits[g]',criteriaCategoryLimits[g])
                if LowerClosed:
                    self.evaluation[g][cKey] = Decimal(str(criteriaCategoryLimits[g][int(c)-1]))
                else:
                    self.evaluation[g][cKey] = Decimal(str(criteriaCategoryLimits[g][int(c)]))

        self.profiles = profiles
        profileLimits = list(profiles.keys())
        self.profileLimits = profileLimits
        
        if Debug:
            print('5.')
            print('self.profiles',profiles)
            print('self.actions',self.actions)
            print('self.profileLimits',profileLimits)
                        
        self.runTimes['computeProfiles'] = time() - t0

        # construct outranking relation
        t0 = time()

        self.order = len(self.actions)
        if outrankingModel == 'standard':
            from outrankingDigraphs import BipolarOutrankingDigraph
            g = BipolarOutrankingDigraph(self,
                                     Threading=Threading,
                                         startMethod=startMethod,
                                         nbrCores=nbrCores)
            self.nbrThreads = copy2self(g.nbrThreads)
            self.startMethod = copy2self(g.startMethod)
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)
            self.nbrThreads = copy2self(g.nbrThreads)
        elif outrankingModel == 'mp':
            import os
            from perfTabs import PerformanceTableau
            PerformanceTableau.save(self,'sharedPerfTab')
            while not os.path.exists('./sharedPerfTab.py'):
                pass
            from mpOutrankingDigraphs import MPBipolarOutrankingDigraph
            g = MPBipolarOutrankingDigraph(Normalized=True)
            self.nbrThreads = copy2self(g.nbrThreads)
            self.startMethod = copy2self(g.startMethod)
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)
            self.nbrThreads = copy2self(g.nbrThreads)
        elif outrankingModel == 'confident':
            from outrankingDigraphs import ConfidentBipolarOutrankingDigraph
            g = ConfidentBipolarOutrankingDigraph(self,
                                distribution=distribution,
                                betaParameter=betaParameter,
                                confidence=confidence,
                                )
            self.nbrThreads = 0
            self.startMethod = None
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)       
            self.bipolarConfidenceLevel = copy2self(g.bipolarConfidenceLevel)
            self.confidenceCutLevel = copy2self(g.confidenceCutLevel)
            self.distribution = copy2self(g.distribution)
            self.betaParameter = copy2self(g.betaParameter)
            self.likelihoods = copy2self(g.likelihoods)
        elif outrankingModel == 'robust':
            from outrankingDigraphs import RobustOutrankingDigraph
            g = RobustOutrankingDigraph(self)
            self.nbrThreads = 0
            self.startMethod = None
            self.relation = copy2self(g.relation)
            self.valuationdomain = copy2self(g.valuationdomain)       
            self.stability = copy2self(g.stability)
        else:
            print('Errr: The outranking model %s is not availbale !!' % outrankingModel)

        self.runTimes['outrankingRelation'] = time() - t0
        
        # compute quantiles by sorting
        t0 = time()
        self.sortingRelation = self._computeSortingRelation(
            Debug=Debug)
        self.runTimes['sortingRelation'] = time() - t0

        # compute rating-by-ranking
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
        elif rankingRule == 'NetFlows':
            from linearOrders import NetFlowsOrder
            nf = NetFlowsOrder(g)
            actionsList = nf.netFlowsRanking
            self.rankingRule = 'NetFlows'
            self.rankingScores = nf.decnetFlowScores
        elif rankingRule == 'RankedPairs':
            from linearOrders import RankedPairsRanking
            rp = RankedPairsRanking(g)
            actionsList = rp.rankedPairsRanking
            self.rankingRule = 'RankedPairs'
            self.rankingScores = None
        elif rankingRule == 'IteratedCopeland':
            from linearOrders import IteratedCopelandRanking
            rp = IteratedCopelandRanking(g)
            actionsList = rp.iteratedCopelandRanking
            self.rankingRule = 'IteratedCopeland'
            self.rankingScores = None
        elif rankingRule == 'IteratedNetFlows':
            from linearOrders import IteratedNetFlowsRanking
            rp = IteratedNetFlowsRanking(g)
            actionsList = rp.iteratedNetFlowsRanking
            self.rankingRule = 'IteratedNetFlows'
            self.rankingScores = None
        elif rankingRule == 'Kemeny':
            if g.order > 12:
                print('Error: the digraph is to big for the Kemeny ranking rule üüü')
            else:
                from linearOrders import KemenyRanking
                ke = KemenyRanking(g, orderLimit=g.order)
                actionsList = ke.kemenyRanking
                self.rankingRule = 'Kemeny'
                self.rankingScores = None
        else:
            print('Errr: The ranking rule %s is not availbale !!' % rankingRule)
            
        if rankingRule != 'best':
            self.rankingCorrelation = g.computeRankingCorrelation(actionsList)
        self.actionsRanking = actionsList
        if Debug:
            print('6.')
            print('*',self.actionsRanking)
        self.ratingCategories = self._computeQuantilesRatingByRanking(Debug=Debug)
        if Debug:
            print('7.')
            print('Ranking rule        :', self.rankingRule)
            print('Actions ranking     :', self.actionsRanking)
            print('Ranking correlation :', self.rankingCorrelation)
            print('Rating categories:', self.ratingCategories)
        self.runTimes['rating-by-ranking'] = time() - t0
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        self.runTimes['totalTime'] = time()-tt

#.....  specific absolute rating class methods  ....
#       see abstract ratingDigraphs class     

###############  testing
if __name__ == "__main__":

    print("""
    ****************************************************
    * Digraph3 ratingDigraphs module                   *
    * Copyright (C) 2022 Raymond Bisdorff              *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    print('*-------- Testing classes and methods -------')


    from randomPerfTabs import *
    MP = True
    nbrCores = 8

##    # relative quantiles rating
##    pt = RandomCBPerformanceTableau(numberOfActions=500,seed=9)
##    rrq = RatingByRelativeQuantilesDigraph(pt,quantiles=11,
##                                         LowerClosed=False,
##                                         outrankingModel='mp',
##                                         Threading=MP,
##                                         nbrCores=nbrCores,
##                                         Debug=False)
##    print(rrq)
##    #rrq.showHTMLRatingHeatmap()
##    #rrq.showRatingByQuantilesSorting(strategy='average')
##    rrq.showRatingByQuantilesRanking()
    
##    rlq = RatingByLearnedQuantilesDigraph(pt,quantiles=7,outrankingModel='mp')
##    print(rlq)
##    lrq.showRatingByQuantilesRanking()
    #corr = rrq.computeRatingByRankingCorrelation(Debug=False)
    #print('*-----Global Relative-Rating-By-Ranking Quality')
    #rrq.showCorrelation(corr)
    #rrq.showRatingConsensusQuality()

    # absolute quantiles rating from randomPerfTabs import
#   Random3ObjectivesPerformanceTableau
    hpt = Random3ObjectivesPerformanceTableau(numberOfActions=1000,seed=1)
    from performanceQuantiles import PerformanceQuantiles
    pq = PerformanceQuantiles(hpt,numberOfBins=20,LowerClosed=True,Debug=False)
    # new incoming decision actions of the same kind
    from randomPerfTabs\
    import RandomPerformanceGenerator as PerfTabGenerator
    tpg = PerfTabGenerator(hpt,instanceCounter=0,seed=1)
    newActions = tpg.randomActions(20)
    # rating the new set of decision actions after
    # updating the historical performance quantiles
    pq.updateQuantiles(newActions,historySize=1000)
    lqr = RatingByLearnedQuantilesDigraph(pq,newData=newActions,
                        quantiles=7, outrankingModel='mp',
                        rankingRule='best', Threading=MP,
                        startMethod=None,
                        nbrCores=nbrCores, Debug=False)
    print(lqr)

##    lqr.showRatingByQuantilesSorting()
##    lqr.showRatingByQuantilesRanking()
##    print(lqr.computeRatingByRankingCorrelation(Debug=True))
##    lqr.showRankingConsensusQuality(lqr.actionsRanking)
    # from outrankingDigraphs import *
    # t = PerformanceTableau(filePerfTab='pmax3')
    # qr = RatingByRelativeQuantilesDigraph(t,outrankingModel='mp')
    # PerformanceTableau.showHTMLPerformanceHeatmap(qr,Correlations=True)
    
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')


