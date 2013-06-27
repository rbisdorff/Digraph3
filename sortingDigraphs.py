#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python implementation of digraphs
# Current revision $Revision$
# Copyright (C) 2006-2008  Raymond Bisdorff
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
from digraphs import *
from outrankingDigraphs import *
from sortingDigraphs import *

class SortingDigraph(BipolarOutrankingDigraph,PerformanceTableau):
    """
    Specialisation of the digraphs.BipolarOutrankingDigraph Class
    for Condorcet based multicriteria sorting of alternatives.

    Besides a valid PerformanceTableau instance we require a sorting profile,
    i.e.:

         | a dictionary <categories> of categories with 'name', 'order' and 'comment'
         | a dictionary <criteriaCategoryLimits> with double entry:

               [criteriakey][categoryKey] containing a ['minimum'] and
               a  ['maximum'] value in the scale of the criterion
               respecting the order of the categories.

    Template of required data::

        self.categories = {'c01': { 'name': 'week','order': 0,
                                    'comment': 'lowest category',},
                           'c02': { 'name': 'ok','order': 1,
                                    'comment': 'medium category',},
                           'c03': { 'name': 'good','order': 2,
                                    'comment': 'highest category',},
                           'c04': { 'name': 'excellent','order': 3,
                                    'comment': 'highest category',},
        }
        self.criteriaCategoryLimits['lowerClosed'] = True # default
        self.criteriaCategoryLimits[g] = {
                'c01': {'minimum':0, 'maximum':25},
                'c02': {'minimum':25, 'maximum':50},
                'c03': {'minimum':50, 'maximum':75},
                'c04': {'minimum':75, 'maximum':120},
         }

    A template named tempProfile.py is providied in the digraphs module distribution.


    .. warning::

        Adds the category low limit and high limit profiles as supplementary
        entries to its actions set and adds the corresponding evaluations
        to the underlying genuine outranking digraph.
        If this digraph is needed without profiles further on,
        it is necessary to create a separate BipolarOutrankingDigraph
        from the same performance tableau !

    """

    def __init__(self,argPerfTab=None,
                 argProfile=None,
                 scaleSteps=5,
                 minValuation=-100.0,
                 maxValuation=100.0,
                 isRobust=False,
                 hasNoVeto=False,
                 lowerClosed=True):
        """
        Constructor for SortingDigraph instances.

        .. note::

            We generally require an OutrankingDigraph instance g and a filename
            where categories and a profile my be read from. If no such filename is given, then a default profile with five, equally spaced, categories is used on each criteria. By default lower closed limts of categories are supposed to be used in the sorting.
        """

        import copy
        from decimal import Decimal

        # import the performance tableau
        if argPerfTab == None:
            perfTab = RandomPerformanceTableau(numberOfActions=10,
                                               numberOfCriteria=13)
        else:
            perfTab = argPerfTab
        # normalize the actions as a dictionary construct
        if isinstance(perfTab.actions,list):
            actions = {}
            for x in perfTab.actions:
                actions[x] = {'name': str(x)}
            self.actions = actions
        else:
            self.actions = copy.deepcopy(perfTab.actions)

        # keep a copy of the original actions set before adding the profiles
        self.actionsOrig = copy.deepcopy(self.actions)

        # actionsOrig = self.actionsOrig

        #  input the profiles
        if argProfile != None:
            defaultProfiles = False
            self.criteria = copy.deepcopy(perfTab.criteria)
            self.convertWeightFloatToDecimal()
            self.evaluation = copy.deepcopy(perfTab.evaluation)
            self.convertEvaluationFloatToDecimal()
            if isinstance(argProfile,str): # input from stored instantiation
                fileName = argProfile
                fileNameExt = fileName + '.py'
                profile = {}
                exec(compile(open(fileNameExt).read(), fileNameExt, 'exec'),profile)
                #print(profile)
                self.name = fileName
                self.categories = profile['categories']
                self.criteriaCategoryLimits = profile['criteriaCategoryLimits']
            else: # input from a profiles dictionary
                self.name = 'sorting_with_given_profile'
                self.categories = copy.deepcopy(argProfile['categories'])
                self.criteriaCategoryLimits = copy.deepcopy(argProfile['criteriaCategoryLimits'])
        else:
            defaultProfiles = True
            self.name = 'sorting_with_default_profiles'
            normPerfTab = NormalizedPerformanceTableau(perfTab)
            self.criteria = copy.deepcopy(normPerfTab.criteria)
            self.convertWeightFloatToDecimal()
            self.evaluation = copy.deepcopy(normPerfTab.evaluation)
            self.convertEvaluationFloatToDecimal()

            # supposing all criteria scales between 0.0 and 100.0

            lowValue = 0.0
            highValue = 100.00
            # with preference direction = max
            categories = {}
            k = int(100 / scaleSteps)
            for i in range(0,100+k,k):
                categories[str(i)] = {'name':str(i), 'order':i}
            self.categories = copy.deepcopy(categories)

            criteriaCategoryLimits = {}
            criteriaCategoryLimits['lowerClosed'] = lowerClosed
            for g in self.criteria:
                criteriaCategoryLimits[g] = {}
                for c in categories:
                    criteriaCategoryLimits[g][c]={
                        'minimum':int(c),
                        'maximum':int(c)+k
                        }
            self.criteriaCategoryLimits = copy.deepcopy(criteriaCategoryLimits)

        # set the category limits type (lowerClosed = True is default)
        self.criteriaCategoryLimits['lowerClosed'] = lowerClosed
        #print 'lowerClosed', lowerClosed

        # add the catogory limits to the actions set
        self.profiles = {'min':{},'max':{}}
        self.profileLimits = set()
        for c in list(self.categories.keys()):
            cMinKey = c+'-m'
            cMaxKey = c+'-M'
            self.profileLimits.add(cMinKey)
            self.profileLimits.add(cMaxKey)
            self.actions[cMinKey] = {'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
            self.actions[cMaxKey] = {'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
            self.profiles['min'][cMinKey] = {'category': c, 'name': 'categorical low limits', 'comment': 'Inferior or equal limits for category membership assessment'}
            self.profiles['max'][cMaxKey] = {'category': c, 'name': 'categorical high limits', 'comment': 'Lower or equal limits for category membership assessment'}
            for g in list(self.criteria.keys()):
                try:
                    if self.criteria[g]['preferenceDirection'] == 'max':
                        self.evaluation[g][cMinKey] = Decimal(str(self.criteriaCategoryLimits[g][c]['minimum']))
                        self.evaluation[g][cMaxKey] = Decimal(str(self.criteriaCategoryLimits[g][c]['maximum']))
                    elif self.criteria[g]['preferenceDirection'] == 'min':
                        if not defaultProfiles:
                            highValueg = Decimal(str(self.criteria[g]['scale'][1]))
                        else:
                            highValueg = Decimal(str(highValue))
                        #print 'highValue = ', highValue
                        self.evaluation[g][cMinKey] = -(highValueg - Decimal(str(self.criteriaCategoryLimits[g][c]['minimum'])))
                        self.evaluation[g][cMaxKey] = -(highValueg - Decimal(str(self.criteriaCategoryLimits[g][c]['maximum'])))
                    else:
                        print('===>>>>> Error')
                except:

                    self.evaluation[g][cMinKey] = Decimal(str(self.criteriaCategoryLimits[g][c]['minimum']))
                    self.evaluation[g][cMaxKey] = Decimal(str(self.criteriaCategoryLimits[g][c]['maximum']))



        self.convertEvaluationFloatToDecimal()

        # construct outranking relation
        if isRobust:
            g = RobustOutrankingDigraph(self)
            self.valuationdomain = copy.deepcopy(g.valuationdomain)
            self.relation = copy.deepcopy(g.relation)
        else:
            Min = Decimal('%.4f' % minValuation)
            Max = Decimal('%.4f' % maxValuation)
            Med = (Max + Min)/Decimal('2.0')
            self.valuationdomain = {'min': Min, 'med':Med ,'max':Max }
            if lowerClosed:
                self.relation = self.constructRelation(self.criteria,
                                                       self.evaluation,
                                                       initial=self.actionsOrig,
                                                       terminal=self.profileLimits,
                                                       hasNoVeto=hasNoVeto,
                                                       hasBipolarVeto=True)
            else:
                self.relation = self.constructRelation(self.criteria,
                                                       self.evaluation,
                                                       terminal=self.actionsOrig,
                                                       initial=self.profileLimits,
                                                       hasNoVeto=hasNoVeto, hasBipolarVeto=True)
            if lowerClosed:
                for x in self.actionsOrig:
                    for y in self.actionsOrig:
                        self.relation[x][y] = Med
                for x in self.profileLimits:
                    self.relation[x] = {}
                    for y in self.actions:
                        self.relation[x][y] = Med
            else:
                for x in self.actionsOrig:
                    self.relation[x] = {}
                    for y in self.actionsOrig:
                        self.relation[x][y] = Med
                for y in self.profileLimits:
                    for x in self.actions:
                        self.relation[x][y] = Med


        # init general digraph Data
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

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


    def showCriteriaCategoryLimits(self):
        """
        Shows category minimum and maximum limits for each criterion.
        """
        try:
            lowerClosed = self.criteriaCategoryLimits['lowerClosed']
        except:
            lowerClosed = True
        criterionKeys = [x for x in self.criteria]
        categoryKeys = [x for x in self.categories]
        for g in criterionKeys:
            print(g)
            for c in categoryKeys:
                if lowerClosed:
                    print('\t%s [%s; %s[' % (c, self.criteriaCategoryLimits[g][c]['minimum'],self.criteriaCategoryLimits[g][c]['maximum']))
                else:
                    print('\t%s ]%s; %s]' % (c, self.criteriaCategoryLimits[g][c]['minimum'],self.criteriaCategoryLimits[g][c]['maximum']))

    def getActionsKeys(self):
        """
        extract normal actions keys()
        """
        actionsExt = set([x for x in list(self.actions.keys())])
        profiles_m = set([x for x in list(self.profiles['min'].keys())])
        profiles_M = set([x for x in list(self.profiles['max'].keys())])
        return actionsExt - profiles_m - profiles_M

    def orderedCategoryKeys(self,Reverse=False):
        """
        Renders the ordered list of category keys
        based on self.categories['order'] numeric values.
        """
        categoriesSort = []
        for c in list(self.categories.keys()):
            categoriesSort.append((self.categories[c]['order'],c))
        categoriesSort.sort()
        orderedCategoryKeys = [x for (o,x) in categoriesSort]
        if Reverse:
            orderedCategoryKeys.reverse()
        return orderedCategoryKeys

    def computeSortingCharacteristics(self, Comments=False):
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

        actions = self.getActionsKeys()
        categories = self.orderedCategoryKeys()

        try:
            lowerClosed = self.criteriaCategoryLimits['lowerClosed']
        except:
            lowerClosed = True

        sorting = {}

        for x in actions:
            sorting[x] = {}
            for c in categories:
                sorting[x][c] = {}
                cMinKey= c+'-m'
                cMaxKey= c+'-M'
                if lowerClosed:
                    lowLimit = self.relation[x][cMinKey]
                    notHighLimit = Max - self.relation[x][cMaxKey] + Min
                else:
                    lowLimit = Max - self.relation[cMinKey][x] + Min
                    notHighLimit = self.relation[cMaxKey][x]
                if Comments:
                    print('%s in %s: low = %.2f, high = %.2f' % (x, c,self.relation[x][cMinKey],self.relation[x][cMaxKey]), end=' ')
                categoryMembership = min(lowLimit,notHighLimit)
                sorting[x][c]['lowLimit'] = lowLimit
                sorting[x][c]['notHighLimit'] = notHighLimit
                sorting[x][c]['categoryMembership'] = categoryMembership

                if Comments:
                    print('\t %.2f \t %.2f \t %.2f' % (sorting[x][c]['lowLimit'], sorting[x][c]['notHighLimit'], sorting[x][c]['categoryMembership']))

        return sorting

    def computePessimisticSorting(self, Comments=False):
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

    def computeCategoryContents(self,Reverse=False,Comments=False):
        """
        Computes the sorting results per category.
        """
        actions = list(self.getActionsKeys())
        actions.sort()
        sorting = self.computeSortingCharacteristics(Comments=Comments)

        categoryContent = {}
        for c in self.orderedCategoryKeys(Reverse=Reverse):
            categoryContent[c] = []
            for x in actions:
                if sorting[x][c]['categoryMembership'] >= self.valuationdomain['med']:
                    categoryContent[c].append(x)
        return categoryContent

    def showSorting(self,Reverse=True,isReturningHTML=False):
        """
        Shows sorting results in decreasing or increasing (Reverse=False)
        order of the categories. If isReturningHTML is True (default = False)
        the method returns a htlm table with the sorting result.
        """
        #from string import replace
        categoryContent = self.computeCategoryContents()
        try:
            lowerClosed = self.criteriaCategoryLimits['lowerClosed']
        except:
            lowerClosed = true
        if Reverse:
            print('\n*--- Sorting results in descending order ---*\n')
            prev_c = '>'
            if isReturningHTML:
                prev_c = '&gt;'
                html = '<h2>Sorting results in descending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'
            for c in self.orderedCategoryKeys(Reverse=Reverse):
                if lowerClosed:
                    print(']%s - %s]:' % (prev_c,c), end=' ')
                    print('\t',categoryContent[c])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">]%s - %s]</td>' % (prev_c,c)
                        catString = str(categoryContent[c])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')
                else:
                    print('[%s - %s[:' % (prev_c,c), end=' ')
                    print('\t',categoryContent[c])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">[%s - %s[</td>' % (prev_c,c)
                        catString = str(categoryContent[c])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')
                prev_c = c
        else:
            print('\n*--- Sorting results in ascending order ---*\n')
            if isReturningHTML:
                html = '<h2>Sorting results in ascending order</h2>'
                html += '<table style="background-color:White;" border="1"><tr bgcolor="#9acd32"><th>Categories</th><th>Assorting</th></tr>'
            cat = [x for x in self.orderedCategoryKeys(Reverse=Reverse)]
            if isReturningHTML:
                cat.append('&lt;')
            else:
                cat.append('<')

            for i in range(len(cat)-1):
                if lowerClosed:
                    print('[%s - %s[:' % (cat[i],cat[i+1]), end=' ')
                    print('\t',categoryContent[cat[i]])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">]%s - %s]</td>' % (cat[i],cat[i+1])
                        catString = str(categoryContent[cat[i]])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')
                else:
                    print(']%s - %s]:' % (cat[i],cat[i+1]), end=' ')
                    print('\t',categoryContent[cat[i]])
                    if isReturningHTML:
                        html += '<tr><td bgcolor="#FFF79B">[%s - %s[</td>' % (cat[i],cat[i+1])
                        catString = str(categoryContent[cat[i]])
                        html += '<td>%s</td></tr>' % catString.replace('\'','&apos;')

        if isReturningHTML:
            html += '</table>'
            return html

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
            ## ms = 100 * len(self.actions) + 500 * len(self.criteria) * 20 * len(self.evaluation)
            ## print 'estimated mapped memory size = %d' % (ms)
            ##fo = mmap.mmap(-1,ms)
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

class SortingByChoosingDigraph(Digraph):
    """
    Specialization of generic Digraph class for sorting by choosing results.
    """
    def __init__(self,digraph=None,CoDual=True,Odd=True,Limited=None,Comments=False,Debug=False):
        from copy import deepcopy
        if digraph == None:
            digraph = RandomValuationDigraph()
        digraph.recodeValuation(-1.0,1.0)
        digraphName = 'sorting-'+digraph.name
        self.name = deepcopy(digraphName)
        self.actions = deepcopy(digraph.actions)
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        self.sortingByChoosing = digraph.optimalRankingByChoosing(CoDual=CoDual,Odd=Odd,Limited=Limited,Comments=Comments,Debug=False)
        self.relation = digraph.computeRankingByChoosingRelation()
        #self.relation = deepcopy(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def showSorting(self,Debug=False):
        """
        A show method for self.sortingByChoosing result.
        """
        sortingByChoosing = self.sortingByChoosing['result']
        print('Sorting by Choosing and Rejecting')
        space = ''
        n = len(sortingByChoosing)
        for i in range(n):
            if i+1 == 1:
                nstr='st'
            elif i+1 == 2:
                nstr='nd'
            elif i+1 == 3:
                nstr='rd'
            else:
                nstr='th'
            ibch = set(sortingByChoosing[i][0][1])
            iwch = set(sortingByChoosing[i][1][1])
            iach = iwch & ibch
            if Debug:
                print('ibch, iwch, iach', i, ibch,iwch,iach)
            ch = list(ibch)
            ch.sort()
            print(' %s%s%s Choice %s (%.2f)' % (space,i+1,nstr,ch,sortingByChoosing[i][0][0]))
            if len(iach) > 0 and i < n-1:
                print('  %s Ambiguous Choice %s' % (space,list(iach)))
                space += '  '
            space += '  '
        for i in range(n):
            if n-i == 1:
                nstr='st'
            elif n-i == 2:
                nstr='nd'
            elif n-i == 3:
                nstr='rd'
            else:
                nstr='th'
            space = space[:-2]
            ibch = set(sortingByChoosing[n-i-1][0][1])
            iwch = set(sortingByChoosing[n-i-1][1][1])
            iach = iwch & ibch
            if Debug:
                print('ibch, iwch, iach', i, ibch,iwch,iach)
            ch = list(iwch)
            ch.sort()
            if len(iach) > 0 and i > 0:
                space = space[:-2]
                print('  %s Ambiguous Choice %s' % (space,list(iach)))
            if nstr == 'st':
                print(' Last Choice %s (%.2f)' % (ch,sortingByChoosing[n-i-1][1][0]))        
            else:
                print(' %s%s%s Last Choice %s (%.2f)' % (space,n-i,nstr,ch,sortingByChoosing[n-i-1][1][0])) 

class SortingByBestChoosingDigraph(Digraph):
    """
    Specialization of generic Digraph class for sorting by best-choosing results.
    """
    def __init__(self,digraph=None,CoDual=True,Odd=True,Limited=None,Comments=False,Debug=False):
        from copy import deepcopy
        if digraph == None:
            digraph = RandomValuationDigraph()
        #digraph.recodeValuation(-1.0,1.0)
        digraphName = 'sorting-by-best'+digraph.name
        self.name = deepcopy(digraphName)
        self.actions = deepcopy(digraph.actions)
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        self.sortingByBestChoosing = digraph.computeRankingByBestChoosing(CoDual=CoDual,Debug=False)
        self.relation = digraph.computeRankingByBestChoosingRelation()
        #self.relation = deepcopy(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        
    def showSorting(self):
        self.showRankingByBestChoosing(self.sortingByBestChoosing)

class SortingByLastChoosingDigraph(Digraph):
    """
    Specialization of generic Digraph class for sorting-by-rejecting results.
    """
    def __init__(self,digraph=None,CoDual=True,Odd=True,Limited=None,Comments=False,Debug=False):
        from copy import deepcopy
        if digraph == None:
            digraph = RandomValuationDigraph()
        #digraph.recodeValuation(-1.0,1.0)
        digraphName = 'sorting-by-last'+digraph.name
        self.name = deepcopy(digraphName)
        self.actions = deepcopy(digraph.actions)
        self.valuationdomain = deepcopy(digraph.valuationdomain)
        self.sortingByLastChoosing = digraph.computeRankingByLastChoosing(CoDual=CoDual,Debug=False)
        self.relation = digraph.computeRankingByLastChoosingRelation()
        #self.relation = deepcopy(digraph.relation)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
    
    def showSorting(self):
        self.showRankingByLastChoosing(self.sortingByLastChoosing)

class SortingByPrudentChoosingDigraph(SortingByChoosingDigraph):
    """
    Specialization of generic Digraph class for sorting-by-rejecting results with prudent single elimination of chordless circuits. By default, the cut level for circuits elimination is set to 20% of the valuation domain maximum (1.0).
    """
    def __init__(self,digraph=None,CoDual=True,Odd=True,Limited=0.2,Comments=False,Debug=False,SplitCorrelation=True):
        from copy import deepcopy
        from decimal import Decimal
        from time import time
        if Comments:          
            t0 = time()
            print('------- Commenting sorting by prudent chossing ------')
        if digraph == None:
            digraph_ = RandomValuationDigraph()
        else:
            digraph_ = deepcopy(digraph)
        digraph_.recodeValuation(-1,1)
        digraphName = 'sorting-by-prudent-choosing'+digraph_.name
        self.name = digraphName
        self.actions = digraph_.actions
        self.order = len(self.actions)
        self.valuationdomain = digraph_.valuationdomain
        #self.recodeValuation(-1.0,1.0)
        s1 = SortingByLastChoosingDigraph(digraph_,CoDual=CoDual,Debug=False)
        s2 = SortingByBestChoosingDigraph(digraph_,CoDual=CoDual,Debug=False)
        fus = FusionDigraph(s1,s2)
        cutLevel = min(digraph_.minimalValuationLevelForCircuitsElimination(Odd=Odd,Debug=Debug,Comments=Comments),Decimal(Limited))
        self.cutLevel = cutLevel
        if cutLevel > self.valuationdomain['med']:
            if cutLevel < self.valuationdomain['max']:
                gp = PolarisedDigraph(digraph_,level=cutLevel,StrictCut=True)
            else:
                gp = PolarisedDigraph(digraph_,level=cutLevel,StrictCut=False)
            s1p = SortingByLastChoosingDigraph(gp,CoDual=CoDual,Debug=False)
            s2p = SortingByBestChoosingDigraph(gp,CoDual=CoDual,Debug=False)
            fusp = FusionDigraph(s1p,s2p)
            corrgp = digraph_.computeOrdinalCorrelation(fusp)
            corrg = digraph_.computeOrdinalCorrelation(fus)
            if Comments:
                print('Correlation with cutting    : %.3f x %.3f = %.3f' % (corrgp['correlation'],corrgp['determination'],corrgp['correlation']*corrgp['determination']))
                print('Correlation without cutting : %.3f x %.3f = %.3f' % (corrg['correlation'],corrg['determination'],corrg['correlation']*corrg['determination']))
            if SplitCorrelation:
                if corrgp['correlation'] > corrg['correlation']:           
                    self.relation = deepcopy(fusp.relation)
                else:
                    self.relation = deepcopy(fus.relation)
            else:
                if (corrgp['correlation']*corrgp['determination']) > (corrg['correlation']*corrg['determination']):
                    self.relation = deepcopy(fusp.relation)
                else:
                    self.relation = deepcopy(fus.relation)                
        else:
            self.relation = deepcopy(fus.relation)
        self.sortingByChoosing = self.computeRankingByChoosing(CoDual=CoDual)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()
        if Comments:
            t1 = time()
            gdeter = digraph_.computeDeterminateness()
            self.showSorting()
            print('Circuits cutting level limit  : %.3f' % Limited)
            print('Circuits elimination cut level: %.3f' % self.cutLevel)
            print('Ordinal Correlation with given outranking')
            corr = digraph_.computeOrdinalCorrelation(self)
            print('Correlation     : %.3f' % corr['correlation'])
            print('Determinateness : %.3f (%.3f)' % (corr['determination'],gdeter))
            print('Execution time  : %.4f sec.' % (t1-t0))
        
    

#----------test SortingDigraph class ----------------
if __name__ == "__main__":
    from time import time
    from outrankingDigraphs import *
    from sortingDigraphs import *
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


    t = RandomCBPerformanceTableau(numberOfActions=20)
    t.saveXMCDA2('test')
    t = XMCDA2PerformanceTableau('uniSorting')
    #s = SortingDigraph(t,'tempProfile6')
    #s.showSorting()
    #s.showSorting(Reverse=True)
    print('------- testing sorting by prudent chossing ------')
    g = BipolarOutrankingDigraph(t)
    #g.recodeValuation(-1,1)
    #gdeter = g.computeDeterminateness()
    #t0 = time()
    s = SortingByPrudentChoosingDigraph(g,CoDual=True,Comments=True,Limited=0.2)
    #s = SortingByPrudentChoosingDigraph(g,CoDual=True,Comments=True,Limited=0.2,SplitCorrelation=False)
#    t1 = time()
#    s.showSorting()
#    print('Circuits elimination cut level: %.3f' % s.cutLevel)
#    print('Ordinal Correlation with given outranking')
#    corr = g.computeOrdinalCorrelation(s)
#    print('Correlation     : %.3f' % corr['correlation'])
#    print('Determinateness : %.3f (%.3f)' % (corr['determination'],gdeter))
#    print('Execution time  : %.4f sec.' % (t1-t0))

#    s1 = SortingByBestChoosingDigraph(g,CoDual=True)
#    s1.showSorting()
#    #s1.showRelationTable()
#    #s1.exportGraphViz()
#    print('Best: Ordinal Correlation with given outranking')
#    corr = g.computeOrdinalCorrelation(s1)
#    print('Correlation  : %.5f' % corr['correlation'])
#    print('Determination: %.5f' % corr['determination'])
#    #g.showPerformanceTableau()

#    s2 = SortingByLastChoosingDigraph(g,CoDual=True)
#    s2.showSorting()
#    #s2.showRelationTable()
#    #s2.exportGraphViz()
#    #print(s1.sortingByChoosing)
#    #s1.exportGraphViz()
#    print('Last: Ordinal Correlation with given outranking')
#    corr = g.computeOrdinalCorrelation(s2)
#    print('Correlation  : %.5f' % corr['correlation'])
#    print('Determination: %.5f' % corr['determination'])

#    print('Ordinal Correlation between Best- and Last-choosing')
#    corr = s1.computeOrdinalCorrelation(s2)
#    print('Correlation  : %.5f' % corr['correlation'])
#    print('Determination: %.5f' % corr['determination'])    

#    fusion = FusionDigraph(s1,s2)
#    #fusion.showRelationTable()
#    #g.showRelationTable()
#    print('Fusion: Ordinal Correlation with fusion ranking')
#    corr = g.computeOrdinalCorrelation(fusion)
#    print('Correlation  : %.5f' % corr['correlation'])
#    print('Determination: %.5f' % corr['determination'])
#    fusion.computeRankingByChoosing(CoDual=True)svn
#    fusion.showRankingByChoosing()
    

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
