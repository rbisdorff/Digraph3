#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python implementation of digraphs
# Current revision $Revision: 186 $
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
                exec(compile(open(fileNameExt).read(), fileNameExt, 'exec'))
                self.name = fileName
                self.categories = copy.deepcopy(locals()['categories'])
                self.criteriaCategoryLimits = copy.deepcopy(locals()['criteriaCategoryLimits'])
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

#----------test SortingDigraph class ----------------
if __name__ == "__main__":
    import sys,copy
    from digraphs import *
    from sortingDigraphs import *
    print("""
    ****************************************************
    * Python sortingDigraphs module                    *
    * depends on BipolarOutrankingDigraph and          * 
    * $Revision: 186 $                                *
    * Copyright (C) 2010 Raymond Bisdorff              *
    * The module comes with ABSOLUTELY NO WARRANTY     *
    * to the extent permitted by the applicable law.   *
    * This is free software, and you are welcome to    *
    * redistribute it if it remains free software.     *
    ****************************************************
    """)

    print('*-------- Testing class and methods -------')

             
    t = RandomCBPerformanceTableau()
    t.save('test')
    s = SortingDigraph(t,lowerClosed=True)
    s.showSorting(Reverse=True)
    s1 = SortingDigraph(t,lowerClosed=False)
    s1.showSorting(Reverse=True)
    
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')
        
    print('*************************************')
    print('* R.B. december 2010                *')
    print('* $Revision: 186 $                     *')                   
    print('*************************************')

#############################
# Log record for changes:
# $Log: sortingDigraphs.py,v $
# Revision 1.32  2012/05/09 10:51:43  bisi
# GPL version 3 licensing installed
#
# Revision 1.31  2012/02/20 09:48:31  bisi
# debugging
#
# Revision 1.30  2012/02/15 20:13:02  bisi
# Added lower open categories sorting
#
# Revision 1.22  2011/04/26 12:12:55  bisi
# added NormalizedPerformanceTableau Class
#
# Revision 1.13  2011/01/04 08:43:28  bisi
# added isReturninHTML falg to showSorting method
#
# Revision 1.12  2011/01/02 14:25:59  bisi
# Added XMCDA 2 export of profiles description,
#  ie categories and criterionCategoryLimits.
#
# Revision 1.8  2010/12/27 10:04:56  bisi
# enhanced sorting characteristics return
#
# Revision 1.4  2010/12/12 03:19:01  bisi
# Added showSorting() method
#
# Revision 1.1  2010/12/11 19:39:32  bisi
# Added sortingDigraphs.py submodule
#
#############################
