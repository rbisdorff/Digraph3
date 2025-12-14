#!/Usr/bin/env python3
#########################
"""
Python3+ implementation of the bipolarValuedSets module.

Copyright (C) 2025  Raymond Bisdorff

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
#######################

__version__ = "Branch: Python3.14.2$"
from collections import OrderedDict
from decimal import Decimal

#------------------

class BpvSet(object):
    """
    Root class. See the final scratch part
    """
    def __repr__(self):
        """
        Default presentation method for bipolar-valued set instances.
        """
        reprString = '*------- bvset instance description ------*\n'
        reprString += 'Instance class      : %s\n' % self.__class__.__name__
        reprString += 'Instance name       : %s\n' % self.name
        reprString += 'support dimension   : %s\n' % len(self.support)
        try:
            reprString += 'seed                : %s\n' % str(self.randomSeed)
        except:
            pass        
        reprString += 'Positive members    : %d\n' % self.computeCardinality()
        reprString += 'Valuation domain    : [%.2f;%.2f]\n'\
                      % (self.valuationDomain['min'],self.valuationDomain['max'])
        reprString += 'Determinateness (%%) : %.2f\n' % (self.determinateness * Decimal('100.0'))
        reprString += 'Attributes          : %s\n' % list(self.__dict__.keys())
        return reprString

    def __init__(self,fileName=None):
        from decimal import Decimal
        if fileName is None:
            self.name = 'emptyBvpSet'
            self.support = {}
            self.ndigits = 4
            self.valuationDomain = {'min':Decimal(-1),'med':Decimal(0),'max':Decimal(1)}
            self.membership = {}
            self.cardinality = 0
            self.determinateness = Decimal('0')
        else:
            fileNameExt = fileName+'.py'
            argDict = {}
            fi = open(fileNameExt,'r')
            fileText = fi.read()
            fi.close()
            exec(compile(fileText, fileName, 'exec'), argDict)
            self.name = fileNameExt
            self.support = argDict['support']
            self.ndigits = argDict['ndigits']
            self.valuationDomain = argDict['valuationDomain']
            self.membership = argDict['membership']
            self.cardinality = self.computeCardinality()
            self.determinateness = self.computeDeterminateness()

    def showMembershipCharacteristics(self,ndigits=None,Normalized=False):
        """
        When *Normalized*, the charactritic values are recoded into the [-1,1] range
        """
        from digraphsTools import scoredTuplesSort
        if Normalized:
            from copy import deepcopy
            cps = deepcopy(self)
            cps.recodeValuation()
            membership = cps.membership
            valuationDomain = cps.valuationDomain
        else:
            membership = self.membership
            valuationDomain = self.valuationDomain
        items = self.support
        if ndigits is None or ndigits > self.ndigits:
            ndigits = self.ndigits
        formatString = '  %%s:  %%+ .%df' % (ndigits)
        characteristics = [(membership[x],x) for x in items]
        scoredTuplesSort(characteristics,reverse=True)
        #print(characteristics)
        for it in characteristics:
            #print(it)
            x = it[1]
            print(formatString% (items[x]['shortName'], membership[x]) )
        print('Valuation domain: [%+.2f;%+.2f]' % (
            valuationDomain['min'],valuationDomain['max'] ))            

    def recodeValuation(self,newMin=-1,newMax=1,ndigits=2,Debug=False):
        """
        Specialization for recoding the valuation of a BpvSet membership chracteristics
        By default the valuation domain is normalized to [-1;1]
        """
        from decimal import Decimal
        from copy import deepcopy
        
        # saving old and new valuation domain
        oldMax = self.valuationDomain['max']
        oldMin = self.valuationDomain['min']
        oldMed = self.valuationDomain['med']
        oldAmplitude = oldMax - oldMin
        if Debug:
            print(oldMin, oldMed, oldMax, oldAmplitude)
        formatString = '%%2.%df' % ndigits
        newMin = Decimal(formatString % newMin)
        newMax = Decimal(formatString % newMax)
        newMed = Decimal(formatString % ( (newMax + newMin)/Decimal('2.0') ))
        newAmplitude = newMax - newMin
        if Debug:
            print(newMin, newMed, newMax, newAmplitude)
        # loop over all items
        #print('Recoding the valuation of a BpvSet instance')
        oldMembership = self.membership
        newMembership = {}
        for it in self.support:
            newMembership[it] = Decimal(formatString % (
                newMin + ((oldMembership[it] - oldMin)/oldAmplitude) * newAmplitude))
       # update valuation domain
        self.valuationDomain = { 'min':newMin, 'max':newMax, 'med':newMed }
        if ndigits == 0:
            self.valuationDomain['hasIntegerValuation'] = True
        else:
            self.valuationDomain['hasIntegerValuation'] = False 
        self.membership = deepcopy(newMembership)

    def computeDeterminateness(self):
        """
         Return the mean absolute characteristic value
        """
        from decimal import Decimal
        Med = self.valuationDomain['med']
        Max = self.valuationDomain['max']
        determinateness = Decimal(0)
        items = self.support
        n = len(items)
        membership = self.membership
        for it in items:
                determinateness += abs(membership[it])
        return determinateness / Decimal(str(n*Max))

    def computeCardinality(self):
        """
        Return the number of positively included elements
        """
        cardinality = 0
        Med = self.valuationDomain['med']
        items = self.support
        membership = self.membership
        for it in items:
            #print(it)
            if membership[it] > Med:
                cardinality += 1
        return cardinality

    def save(self,fileName='tempBpvSet'):
        """
        Permanent storage of a BvpSet instance
        """
        print('*--- Saving bvp-set in file: <' + fileName + '.py> ---*')
        support = self.support
        membership = self.membership
        Min = self.valuationDomain['min']
        Med = self.valuationDomain['med']
        Max = self.valuationDomain['max']
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved BvpSet instance\n')
        fo.write('from collections import OrderedDict\n')
        fo.write('from decimal import Decimal\n')
        
        fo.write('support = OrderedDict([\n')
        for x in support:
            fo.write('(\'' + str(x) + '\',\n')
            try:
                fo.write(str(support[x])+'),\n')
            except:
                fo.write('{\'name\': \'%s\'}),\n' % str(x))
        fo.write('])\n')
        fo.write('valuationDomain = {\'min\': Decimal("'+str(Min)+'"),\'med\': Decimal("'+str(Med)+'"),\'max\': Decimal("'+str(Max)+'")}\n')
        try:
            ndigits = self.ndigits
        except:
            ndigits = 4
        fo.write('ndigits = %d \n' % ndigits )
        fo.write('membership = {\n')
        for x in membership:
            fo.write('\'' + str(x) + '\':')
            valueString = 'Decimal(\'%%.%df\'),\n' % (ndigits)
            fo.write(valueString % membership[x])
        fo.write( '}\n')
        fo.close()

    def __and__(self,other,/):
        """
        Return the bipolar-valued self&other
        """
        return self.intersection(other)

    def intersection(self,other,/):
        """
        Return the set intersection of self and other
        """
        from copy import deepcopy
        from bipolarValuedSets import BpvSet
        newSelf = deepcopy(self)
        newSelf.recodeValuation()
        newOther = deepcopy(other)
        newOther.recodeValuation()
        inter = BpvSet()
        inter.name = self.name+'and'+other.name
        
        # union of the supports
        for it in newSelf.support:
            #print(it)
            if it not in inter.support:
                inter.support[it] = newSelf.support[it]
        for it in newOther.support:
            #print(it)
            if it not in inter.support:
                inter.support[it] = newOther.support[it]
        
        membership = {}
        Min = inter.valuationDomain['min']
        for it in inter.support:
            try:
                membership[it] = min(newSelf.membership[it],newOther.membership[it])
            except:
                membership[it] = Min
        inter.ndigits = max(newSelf.ndigits, newOther.ndigits)
        inter.membership = membership
        inter.determinateness = inter.computeDeterminateness()
        inter.cardinality = inter.computeCardinality()
        return inter

    def __or__(self,other,/):
        """      Return the bipolar-valued self|other set
        """
        return self.union(other)

    def union(self,other,/):
        """
        Return the bipolar-valued set union of self and other
        """

        from copy import deepcopy
        from bipolarValuedSets import BpvSet
        newSelf = deepcopy(self)
        newSelf.recodeValuation()
        newOther = deepcopy(other)
        newOther.recodeValuation()
        union = BpvSet()
        union.name = self.name+'or'+other.name

        # union of the supports
        for it in newSelf.support:
            #print(it)
            if it not in union.support:
                union.support[it] = newSelf.support[it]
        for it in newOther.support:
            #print(it)
            if it not in union.support:
                union.support[it] = newOther.support[it]

        membership = {}
        Max = union.valuationDomain['max']
        for it in union.support:
            try:
                membership[it] = max(newSelf.membership[it],newOther.membership[it])
            except:
                try:
                    membership[it] = newSelf.membership[it]
                except:
                    membership[it] = newOther.membership[it]
        union.ndigits = max(newSelf.ndigits, newOther.ndigits)
        union.membership = membership
        union.determinateness = union.computeDeterminateness()
        union.cardinality = union.computeCardinality()
        return union

    def __contains__(self,it,/):
        """
        x.__contains__(y) <==> y in x
        x is the identifier
        of a potential element
        """
        if it in self.support:
            return True
        else:
            return False

    def isSubset(self,other,/):
        """
        Return the bipolar-valued credibility that self is a bpv-subset of other
        """
        from copy import deepcopy
        newSelf = deepcopy(self)
        newSelf.recodeValuation()
        newOther = deepcopy(other)
        newOther.recodeValuation()
        Min = newSelf.valuationDomain['min']
        Max = newSelf.valuationDomain['max']
        res = Max
        for it in newSelf.support:
            print(it)
            try:
                resit = -( min(newSelf.membership[it],-(newOther.membership[it])) )
                print(res,newSelf.membership[it],newOther.membership[it],resit)
            except:
                print('other does not contain;^',it)
                return Min
            if resit < res:
                res = resit
        return res

    def __sub__(self,other,/):
        """
        Return the set difference self-other
        """
        return self.difference(other)

    def difference(self,other,/):
        """
        Return the set difference between self and other
        """
        from copy import deepcopy
        from bipolarValuedSets import BpvSet
        newSelf = deepcopy(self)
        newSelf.recodeValuation()
        newOther = deepcopy(other)
        newOther.recodeValuation()
        diff = BpvSet()
        diff.name = self.name+'-'+other.name

        # union of the supports
        for it in newSelf.support:
            #print(it)
            if it not in diff.support:
                diff.support[it] = newSelf.support[it]
        for it in newOther.support:
            #print(it)
            if it not in diff.support:
                diff.support[it] = newOther.support[it]

        membership = {}
        Min = diff.valuationDomain['min']
        Med = diff.valuationDomain['med']
        Max = diff.valuationDomain['max']
        for it in diff.support:
            try:
                membership[it] = -min(newSelf.membership[it],-newOther.membership[it])
            except:
                try:
                    membership[it] = newSelf.membership[it]
                except:
                    membership[it] = Min
        diff.ndigits = min(newSelf.ndigits, newOther.ndigits)
        diff.membership = membership
        diff.determinateness = diff.computeDeterminateness()
        diff.cardinality = diff.computeCardinality()
        return diff

    def __neg__(self,/):
        """
        Return the complement or dual of self wrt self.support
        """
        return self.dual()

    def dual(self,/):
        """
        Return the complement or dual of self wrt self.support
        """
        from copy import deepcopy
        from bipolarValuedSets import BpvSet
        #newSelf = deepcopy(self)
        #newSelf.recodeValuation()
        comp = BpvSet()
        comp.name = self.name+'comp'
        comp.support = self.support
        comp.valuationDomain = self.valuationDomain
        membership = {}
        for it in comp.support:
            membership[it] = -self.membership[it]
        comp.ndigits = self.ndigits
        comp.membership = membership
        comp.determinateness = comp.computeDeterminateness()
        comp.cardinality = comp.computeCardinality()
        return comp

    def __xor__(self,other,/):
        """
        Return all elements that are exactly in one of the sets
        """
        return ((self - other) | (other - self))

    def update(self,other,/):
        """
        Return the union of X and Y
        """
        return self.union(other)

    def strip(self,cutLevel=None,Strict=True,InSite=True):
        """
        Strip the support at cutLevel. If None, cutLevel is valuation minimum.
        If Strict is True, cutLevel is stripped !
        """
        if cutLevel is None:
            cutLevel = self.valuationDomain['min']
        new = BpvSet()
        new.name = self.name
        new.valuationDomain = self.valuationDomain
        support = self.support
        membership = self.membership
        for it in support:
            if Strict:
                if membership[it] > cutLevel:
                    new.support[it] = support[it]
                    new.membership[it] = membership[it]
            else:
                if membership[it] >= cutLevel:
                    new.support[it] = support[it]
                    new.membership[it] = membership[it]
        new.ndigits = self.ndigits
        if InSite:
            self.support = new.support
            self.membership = new.membership
            self.cardinality = new.computeCardinality()
            self.determinateness = new.computeDeterminateness()
            return self
        else:
            new.cardinality = new.computeCardinality()
            new.determinateness = new.computeDeterminateness()
            return new
                
                    
        
#-----------------                                        

class RandomBpvSet(BpvSet):
    """
    *undeterminateness* parameter (in float % [0.0,1.0], default=0.1)
    """
    def __init__(self,numberOfElements=5,
                 elementNamePrefix='x',
                 undeterminateness=0.1,
                 valuationRange=(-1,1),
                 ndigits = 4,
                 seed=None,
                 Debug=False):
        # store arguments
        self.cardinality = numberOfElements 
        self.elementNamePrefix = 'elementNamePrefix'
        self.randomSeed = seed
        self.ndigits = ndigits
        # set random seed (none by default)
        import random
        random.seed(seed)
        # setting object name
        self.name = 'randomBpvSet'
        # generate random items
        nd = len(str(numberOfElements))
        support = {}
        for i in range(1,numberOfElements+1):
            elementKey = ('%s%%0%dd' % (elementNamePrefix,nd)) % (i)
            support[elementKey] = {'shortName':elementKey,
                              'name': 'potential element #%d' % i,
                              'comment': 'RandomBpvset() generated.' }
        self.support = support
        # setting valuation domain
        
        valuationDomain = {'min': Decimal(str(valuationRange[0])),
                           'med': Decimal(0),
                           'max': Decimal(str(valuationRange[1]))}
        Max = valuationDomain['max']
        Med = valuationDomain['med']
        Min = valuationDomain['min']
        self.valuationDomain = valuationDomain
        # setting characetistc values
        membership = dict()
        formatString = '%%.%df' % ndigits
        #print(formatString)
        for it in support:
            u = (random.random() * 2.0) - 1.0 
            membership[it] = Decimal(formatString % u) * Max
            if Debug:
                print(it,u,membership[it])
            if u > -undeterminateness and u < undeterminateness:
                membership[it] = Med
                if Debug:
                    print(it,u,membership[it])
        self.membership = membership
        # setting bpvSet dimension
        cardinality = 0
        determinateness = Decimal(0)
        for it in support:
            if membership[it] > Med:
                cardinality += 1
        self.cardinality = cardinality
        self.determinateness = self.computeDeterminateness()       
        
#############################################
# scratch space for testing ongoing developments
#----------test the module ----------------
if __name__ == "__main__":

    print('*****************************************************')
    print('* bipolarValuedSets.py module                       *')
    print('* $Revision: Python3.13$                            *')
    print('* Copyright (C) 2025 Raymond Bisdorff               *')
    print('* The module comes with ABSOLUTELY NO WARRANTY      *')
    print('* to the extent permitted by the applicable law.    *')
    print('* This is free software, and you are welcome to     *')
    print('* redistribute it if it remains free software.      *')
    print('*****************************************************')

    print('*-------- Testing classes and methods -------')

    X = RandomBpvSet(numberOfElements=5,elementNamePrefix='s',
                      undeterminateness=0.1,
                      valuationRange=(-1,1),ndigits=4,
                      seed=1,
                      Debug=False)
    
    #X.showMembershipCharacteristics(Normalized=False)
    X.showMembershipCharacteristics()
    Y = RandomBpvSet(numberOfElements=3,elementNamePrefix='s',
                      undeterminateness=0.1,
                      valuationRange=(-1,1),
                      seed=2,ndigits=4,
                      Debug=False)
    
    #Y.showMembershipCharacteristics(Normalized=False)
    Y.showMembershipCharacteristics()
    D = Y - X
    E = D.strip(InSite=False)
    D.strip()
    
