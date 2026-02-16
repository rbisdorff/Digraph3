#!/usr/bin/env python3
"""
Python 3 implementation of voting digraphs
Refactored from revision 1.549 of the digraphs module
Copyright (C) 2011-2025 Raymond Bisdorff

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

__version__ = "$Revision: Python 3.13.13"

from digraphsTools import * 
from digraphs import *

#--------- Decimal precision --------------
from decimal import Decimal

#---------- voting profiles

class VotingProfile(object):
    """
    A generic class for storing voting profiles.

    General structure::

	candidates = OrderedDict([('a', ...),('b', ...),('c', ...), ( ... ) ])
	voters = OrderedDict([
        ('1', {'weight':1.0}),
        ('2', {'weight':1.0}),
        ...,
        ])
    	ballot = {     # voters x candidates x candidates
            '1': {     # bipolar characteristic {-1,0,1} of each voter's
                  'a': { 'a':0,'b':-1,'c':0, ...},   # pairwise preferences
                  'b': { 'a':1,'b':0, 'c':1, ...},
    	          'c': { 'a':0,'b':-1,'c':0, ...},
    	          ...,
    	    },
    	    '2': { 'a': { 'a':0, 'b':0, 'c':1, ...},
                   'b': { 'a':0, 'b':0, 'c':1, ...},
    	           'c': { 'a':-1,'b':-1,'c':0, ...},
    	           ...,
            },
    	    ...,
    	}

    """
    def __repr__(self):
        """
        Default description for VotingProfile instances.
        """
        reprString = '*------- VotingProfile instance description ------*\n'
        reprString += 'Instance class   : %s\n' % self.__class__.__name__
        reprString += 'Instance name    : %s\n' % self.name
        reprString += '# Candidates     : %d\n' % len(self.candidates)
        reprString += '# Voters         : %d\n' % len(self.voters)
        reprString += 'Attributes       : %s\n' % list(self.__dict__.keys())
       
        return reprString
    
    def __init__(self,fileVotingProfile=None,seed=None):

        if fileVotingProfile is not None:
            fileName = fileVotingProfile+'.py'
            argDict = {}
            fi = open(fileName,'r')
            exec(compile(fi.read(), fileName, 'exec'),argDict)
            fi.close()
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            self.ballot = argDict['ballot']
        else:
            print('Error: a stored voting profile is required!')
            return
    def showAll(self, WithBallots=True):
        """
        Show method for <VotingProfile> instances.
        """
        print('*------ VotingProfile instance: %s ------*' % self.name)
        voters = [x for x in self.voters]
        voters.sort()
        print('Voters     : %s' % str(voters))
        candidates = [x for x in self.candidates]
        candidates.sort()
        print('Candidates : %s' % str(candidates))
        if WithBallots:
            print('Ballots')
            for v in voters:
                print('voting of voter %s (weight = %.1f)' \
                      % (v,self.voters[v]['weight']))
                self.showVoterBallot(v)
                print('----------------------')

    def showVoterBallot(self, voter, hasIntegerValuation=False):
        """
        Show the actual voting of a voter.
        """
        candidates = [x for x in self.candidates]
        print('  >  |', end=' ')
        for x in candidates:
            print("'"+x+"', ", end=' ')
        print('\n-----|------------------------------------------------------------')
        for x in candidates:
            print("'"+x+"' | ", end=' ')
            for y in candidates:
                if hasIntegerValuation:
                    print('%d ' % (self.ballot[voter][x][y]), end=' ')
                else:
                    print('%.2f ' % (self.ballot[voter][x][y]), end=' ')
            print()
        print('\n')

    def save(self,fileName='tempVotingProfile'):
        """
        Persistant storage of an approval voting profile.
        """
        print('*--- Saving voting profile in file: <' + str(fileName) + '.py> ---*')
        candidates = self.candidates
        voters = self.voters
        ballot = self.ballot
        saveFileName = str(fileName)+str('.py')
        fo = open(saveFileName, 'w')
        fo.write('# Saved voting profile: \n')
        fo.write('from collections import OrderedDict \n')
        fo.write('candidates = OrderedDict([\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            fo.write('(\'%s\', {\'name\', \'%s\'}),\n' % (x,candidateName) )
        fo.write('])\n')
        fo.write('voters = OrderedDict([\n')
        for v in voters:
            fo.write('(\'' +str(v)+'\', {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'}),\n')
        fo.write('])\n')
        fo.write('ballot = {\n')
        for v in ballot:
            fo.write('\'' +str(v)+'\': {\n')
            for x in candidates:
                fo.write('\'' + str(x) + '\':{' +'\n')
                for y in candidates:
                    fo.write('\'' + str(y) + '\':' +str(ballot[v][x][y])+',\n')
                fo.write('},\n')
            fo.write('},\n')
        fo.write( '}\n')
        fo.close()

    def computePrerankedBallot(self,preranking,Debug=False):
        """
        Renders the bipolar-valued ballot obtained from
        given preorderings of the candidates per voter
        """
        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
            
        candidates = [c for c in self.candidates]
        currentCandidates = set(candidates)
        prerankedBallot = {}
        for x in candidates:
            prerankedBallot[x] = {}
            for y in candidates:
                prerankedBallot[x][y] = Med

        for eqcl in preranking:
            currRest = currentCandidates - set(eqcl)
            if Debug:
                print(currentCandidates, eqcl, currRest)
            for x in eqcl:
                for y in eqcl:
                    if x != y:
                        prerankedBallot[x][y] = Max
                        prerankedBallot[y][x] = Max

            for x in eqcl:
                for y in currRest:
                    prerankedBallot[x][y] = Max
                    prerankedBallot[y][x] = Min
            currentCandidates = currentCandidates - set(eqcl)
        return prerankedBallot

class RandomVotingProfile(VotingProfile):
    """
    A subclass for generating random voting profiles.
    
    When *IntraGroup* is set to *True*, the candidates are the voters themselves
    """
    def __init__(self,numberOfVoters=9,
                 votersIdPrefix='v',
                 IntraGroup=False,
                 numberOfCandidates=5,
                 candidatesIdPrefix='c',
                 hasRandomWeights=False,maxWeight=10,
                 seed=None,Debug=False):
        """
        Random profile creation parameters:

            | numberOfVoters=9,
            | numberOfCandidates=5

        """
        from collections import OrderedDict
        import random
        random.seed(seed)
        self.seed = seed
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = OrderedDict()
        nd = len(str(numberOfVoters))
        for v in votersList:
            voterID = ('%s%%0%dd' % (votersIdPrefix,nd)) % (v)
            if hasRandomWeights:
                voters[voterID] = {'weight':random.randint(1,maxWeight)}
            else:
                voters[voterID] = {'weight':1}
        if IntraGroup:
            candidates = voters
        else:
            candidatesList = [x for x in range(1,numberOfCandidates + 1)]
            candidates = OrderedDict()
            na = len(str(numberOfCandidates))
            for c in candidatesList:
                candidateID =('%s%%0%dd' % (candidatesIdPrefix,na)) % (c)
                candidates[candidateID] = {'name': candidateID}
        self.IntraGroup = IntraGroup
        self.name = str('randonVotingProfile')
        self.candidates = candidates
        self.voters = voters
        self.ballot = self.generateRandomBallot(seed=seed,Debug=Debug)
        if Debug:
            self.showAll()

    def generateRandomBallot(self,seed,Debug=False):
        """
        Renders a randomly generated approval ballot
        from a list of candidates for each voter.
        """
        from decimal import Decimal
        import random
        if seed is not None:
            random.seed(seed)
        ballot = {}
        voters = [x for x in self.voters]
        #candidatesList = [x for x in self.candidates]
        #nc = len(candidatesList)
        for v in voters:
            ballot[v] = {}
            candidatesList = [x for x in self.candidates]
            nc = len(candidatesList)
            for i in range(nc):
                ballot[v][candidatesList[i]] = {}
                for j in range(nc):
                    ballot[v][candidatesList[i]][candidatesList[j]] = Decimal('0.0')
            if self.IntraGroup:
                candidatesList.remove(v)
            random.shuffle(candidatesList)
            if Debug:
                print(v, candidatesList)
            for i in range(nc):
                for j in range(i+1,nc):
                    ballot[v][candidatesList[i]][candidatesList[j]] = Decimal('1.0')
                    ballot[v][candidatesList[j]][candidatesList[i]] = Decimal('-1.0')
        return ballot


#---------

class PrerankedVotingProfile(VotingProfile):
    """
    A specialised class for preranked voting profiles

    Structure::

        candidates = OrderedDict([('a', ...) ,('b', ...),('c', ...), ...])
        voters = OrderedDict([('1',{'weight':1.0}), ('2',{'weight':1.0}), ...])
        ## each specifies a a ranked list of lists of candidates
        ## from the best to the worst
        preorderBallot = {
            '1' : [['b','c'],['a'], ...],
            '2' : [['a'],['b','c'], ...],
            ...
            }
    """
    def __init__(self,fileVotingProfile=None):

        if fileVotingProfile is not None:
            fileName = fileVotingProfile+'.py'
            argDict = {}
            fi = open(fileName,'r')
            exec(compile(fi.read(), fileName, 'exec'),argDict)
            fi.close()
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            self.prerankedBallot = argDict['prerankedBallot']
            self.ballot = self.computeBallot()
        else:
            print('Error: a stored preranked voting profile is required!')
            return
        self.sumWeights = 0.0
        for v in self.voters:
            self.sumWeights += self.voters[v]['weight']


        
    def save(self,fileName='tempPreRankedProfile'):
        """
        Persistant storage of a  preranked voting profile.

        Parameter:
            name of file (without <.py> extension!).
        """
        print('*--- Saving preorder profile in file: <' + str(fileName) + '.py> ---*')
        candidates = self.candidates
        voters = self.voters
        prerankedBallot = self.prerankedBallot
        saveFileName = str(fileName)+str('.py')
        fo = open(saveFileName, 'w')
        fo.write('# Saved preranked voting profile: \n')
        fo.write('from collections import OrderedDict \n')
        fo.write('candidates = OrderedDict([\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + str(x)+ '\'},\n')
            fo.write('(\'%s\', {\'name\': \'%s\'}),\n' % (x,candidateName) )
        fo.write('])\n')
        fo.write('voters = OrderedDict([\n')
        for v in voters:
            fo.write('(\'' +str(v)+'\', {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'}),\n')
        fo.write('])\n')
        fo.write('prerankedBallot = {\n')
        for v in prerankedBallot:
            fo.write('\'' +str(v)+'\': [\n')
            for x in prerankedBallot[v]:
                fo.write(str(x) + ',\n')
            fo.write('],\n')
        fo.write( '}\n')
        fo.close()

    def showPrerankedBallots(self,IntegerWeights=True):
        """
        show the preranked ballots
        """
##        sumWeights = Decimal('0')
        if IntegerWeights:
            formStr = ' %s(%.0f):\t %s'
        else:
            formStr = ' %s(%.f):\t %s'
        print(' voters \t      marginal     ')
        print('(weight)\t candidates rankings')
        
        for v in self.voters:
##            sumWeights += self.voters[v]['weight']
            print(formStr \
                  % (str(v),self.voters[v]['weight'],
                     str(self.prerankedBallot[v])))
        print('# voters: ',str(self.sumWeights))

    def computeBallot(self,Debug=False):
        """
        compute ballots from the prerankeds
        """
        from copy import deepcopy
        ballot = {}
        for v in self.voters:
            preranked = self.prerankedBallot[v]
            ballot[v] = self.computePrerankedBallot(preranked)
            if Debug:
                print(preranked)
                print(ballot[v])
        return ballot

#-----------

class RandomPrerankedVotingProfile(PrerankedVotingProfile):
    """
    A specialized class for generating random preranked voting profiles.

    *Parameters*   
        * The *votersWeights* parameter may be a list of positive integers in order to
          deterministically attribute weights to the voters
          Is ignored when *RandomWeights* is True
        * When *voterWeights* are None and *RandomWeights* is False, each voter
          obtains a single vote (default setting)
        * the *lengthProbability* influences the expected cardinalities of the equivalence classes
          
    """
    def __init__(self,numberOfVoters=10,
                 numberOfCandidates=5,
                 votersIdPrefix='v',
                 candidatesIdPrefix='c',
                 votersWeights=None,
                 RandomWeights=False,
                 lengthProbability=0.4,
                 seed=None,Debug=False):
        """
        """
        from collections import OrderedDict
        import random
        if seed is None:
            seed = random.random()
        random.seed(seed)
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = OrderedDict()
        nd = len(str(numberOfVoters))
        for v in votersList:
            voterID = ('%s%%0%dd' % (votersIdPrefix,nd)) % (v)
            if votersWeights is not None:
                try:
                    weight = votersWeights[v-1]
                except:
                    weight = 1
            else:
                if RandomWeights:
                    weight = random.randint(1,numberOfVoters)
                else:
                    weight = 1
            voters[voterID] = {'weight':Decimal('%d' % weight)}
        candidatesList = [x for x in range(1,numberOfCandidates + 1)]
        candidates = OrderedDict()
        na = len(str(numberOfCandidates))
        for c in candidatesList:
            candidateID =('%s%%0%dd' % (candidatesIdPrefix,na)) % (c)
            candidates[candidateID] = {'name': 'Candidate '+ candidateID}
        # store instance attributes
        self.name = str('randprerankedProfile')
        self.seed = seed
        self.candidates = candidates
        self.voters = voters
        self.RandomWeights = RandomWeights
        self.sumWeights = Decimal('0')
        for v in self.voters:
            self.sumWeights += self.voters[v]['weight']
        self.lengthProbability = lengthProbability
        self.prerankedBallot = self.generateRandomPrerankedBallot(
                                                        seed=seed)
        self.ballot = self.computeBallot()


    def generateRandomPrerankedBallot(self,
                                   seed=None,Debug=False):
        """
        Renders a randomly generated preranked ballot.
        """
        import random
        random.seed(seed)
        prerankedBallot = {}
        voters = self.voters
        candidatesList = [x for x in self.candidates]
        n = len(candidatesList)
        if Debug:
            print(candidatesList)
        for v in voters:
            random.shuffle(candidatesList)
            if Debug:
                print(candidatesList)
            from randomNumbers import\
                     BinomialRandomVariable
            currIndex = 0
            prerankedBallotv = []
            length = BinomialRandomVariable(n,self.lengthProbability)
            while currIndex < n:
                endIndex = currIndex + length.random()
                if Debug:
                    print(v,n,currIndex,endIndex)
                if endIndex > currIndex:
                    if  endIndex < n:
                        prerankedBallotv.append(candidatesList[currIndex:endIndex])
                        currIndex = endIndex
                    else:
                        prerankedBallotv.append(candidatesList[currIndex:n])
                        currIndex = n
                if Debug:
                    print(v,prerankedBallotv)
            prerankedBallot[v] = prerankedBallotv 
        return prerankedBallot

#-------------
class LinearVotingProfile(VotingProfile):
    """
    A specialised class for linear voting profiles

    Structure::

        candidates = OrderedDict([('a', ...) ,('b', ...),('c', ...), ...])
        voters = OrderedDict([('1',{'weight':1.0}), ('2',{'weight':1.0}), ...])
        ## each specifies a a ranked list of candidates
        ## from the best to the worst
        linearBallot = {
            '1' : ['b','c','a', ...],
            '2' : ['a','b','c', ...],
            ...
            }

    Sample Python3 session
    
    >>> from votingProfiles import *
    >>> v = RandomLinearVotingProfile(numberOfVoters=5,numberOfCandidates=3)
    >>> v.showLinearBallots()
     voters 	      marginal     
    (weight)	 candidates rankings
     v1(1):	 ['c1', 'c3', 'c2']
     v2(1):	 ['c2', 'c1', 'c3']
     v3(1):	 ['c1', 'c3', 'c2']
     v4(1):	 ['c2', 'c1', 'c3']
     v5(1):	 ['c3', 'c1', 'c2']
    # voters:  5
    >>> v.computeRankAnalysis()
    {'c1': [Decimal('2'), Decimal('3'), 0],
     'c2': [Decimal('2'), 0, Decimal('3')],
     'c3': [Decimal('1'), Decimal('2'), Decimal('2')]}
    >>> v.showRankAnalysisTable()
    *----  Borda rank analysis tableau -----*
     candi- | alternative-to-rank |      Borda
     dates  |  1    2    3        | score  average
     -------|-------------------------------------
       'c1' |  2    3    0        |  8     1.60
       'c2' |  2    0    3        |  11     2.20
       'c3' |  1    2    2        |  11     2.20
    >>> v.computeUninominalVotes()
    {'c1': Decimal('2'), 'c2': Decimal('2'), 'c3': Decimal('1')}
    >>> v.computeSimpleMajorityWinner()
    ['c1', 'c2']
    >>> v.computeBordaScores()
    OrderedDict([
    ('c1', {'BordaScore': Decimal('8'), 'averageBordaScore': Decimal('1.6')}),
    ('c2', {'BordaScore': Decimal('11'), 'averageBordaScore': Decimal('2.2')}),
    ('c3', {'BordaScore': Decimal('11'), 'averageBordaScore': Decimal('2.2')})])
    >>> v.computeBordaWinners()
    ['a1']
    >>> v.computeInstantRunoffWinner()
    ['c1']

    """
    def __init__(self,fileVotingProfile=None,numberOfCandidates=5,
                 numberOfVoters=9):
        if fileVotingProfile is not None:
            fileName = fileVotingProfile + '.py'
        ##     fileName = 'testapprovalvotingprofile.py'
            argDict = {}
            fi = open(fileName,'r')
            exec(compile(fi.read(), fileName, 'exec'),argDict)
            fi.close()
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            try:
                self.seed = argDict('seed')
            except:
                pass
            try:
                self.withPolls = argDict('WithPolls')
            except:
                self.WithPolls = False
            try:
                self.RandomWeights = argDict('RandomWeights')
            except:
                pass
            try:
                self.sumWeights = argDict('sumWeights')
            except:
                pass
            try:
                self.poll1 = argDict('poll1')
            except:
                pass
            try:
                self.poll2 = argDict('poll2')
            except:
                pass
            try:
                self.other = argDict('other')
            except:
                pass
            try:
                self.partyRepartition = argDict('partyRepartition')
            except:
                pass
            self.linearBallot = argDict['linearBallot']
            self.ballot = self.computeBallot()
            self.sumWeights = 0.0
            for v in self.voters:
                self.sumWeights += self.voters[v]['weight']
        else:
            #print('!!! Error: The name of a stored linear voting profile is required !!!')
            return


    def convert2BipolarApprovalVotingProfile(self,approvalIndex=1, diapprovalIndex=1):
        """
        Converts a linear voting profile into a bipolar approval-disapproval profile.
        First approvalIndex ranked a re approved, last disapprovalIndex ranked are disapproved.
        """
        

    def computeBallot(self):
        """
        Computes a complete ballot from the linear Ballot.
        """
        candidates = [x for x in self.candidates]
        linearBallot = self.linearBallot
        ballot = {}
        for v in linearBallot:
            ballot[v] = {}
            for x in candidates:
                ballot[v][x] = {}
                for y in candidates:
                    ballot[v][x][y] = Decimal("0.0")
            n = len(linearBallot[v])
            for i in range(n):
                for j in range(i+1,n):
                    x = linearBallot[v][i]
                    y = linearBallot[v][j]
                    ballot[v][x][y] = Decimal("1.0")
                    ballot[v][y][x] = Decimal("-1.0")
        self.ballot = ballot
        return ballot

    def save2BipolarApprovalVotingProfile(self,fileName='tempBipolarApprovalprofile',
                                          approvalIndex=0,disapprovalIndex=None,
                                          Debug=True):
        """
        Convert a linear voting profile into a bipolar approval voting profile.
        """
        from decimal import Decimal
        print('*--- Saving bipolar approval profile in file: <' + str(fileName) + '.py> ---*')
        candidates = self.candidates
        nc = len(candidates)
        voters = self.voters
        linearBallot = self.linearBallot
        saveFileName = str(fileName)+str('.py')
        if approvalIndex > nc-1:
            print('Error: approvalIndex larger than number of candidates!!!')
            approvalIndex = nc-1
            disapprovalIndex = nc
        elif approvalIndex < 0:
            approvalIndex = 0
        if disapprovalIndex is None or disapprovalIndex < 0:
            disapprovalIndex = nc
        if Debug:
            print(nc,approvalIndex,disapprovalIndex)
        fo = open(saveFileName, 'w')
        fo.write('# Saved  bipolar approval voting profile: \n')
        fo.write('from decimal import Decimal \n')
        fo.write('from collections import OrderedDict \n')
        fo.write('candidates = OrderedDict([\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + str(x)+ '\'},\n')
            fo.write('(\'%s\', {\'name\': \'%s\'}),\n' % (x,candidateName) )
        fo.write('])\n')
        fo.write('voters = OrderedDict([\n')
        for v in voters:
            fo.write('(\'' +str(v)+'\', {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'}),\n')
        fo.write('])\n')
        fo.write('approvalBallot = {\n')
        for v in linearBallot:
            fo.write('\'' +str(v)+'\': {\n')
            lvx = [x for x in linearBallot[v]]
            nlvx = len(lvx)
            for x in lvx:
                if lvx.index(x) <= approvalIndex:
                    fo.write( '\'%s\': Decimal(%d),\n' % (x,1) )
                elif lvx.index(x) >= disapprovalIndex:
                    fo.write( '\'%s\': Decimal(%d),\n' % (x,-1) )
                else:
                    fo.write( '\'%s\': Decimal(%d),\n' % (x,0) )               
            fo.write( '},\n')
        fo.write( '}\n')
        fo.close()
    

    def save(self,fileName='templinearprofile'):
        """
        Persistant storage of a linear voting profile.

        Parameter:
            name of file (without <.py> extension!).
        """
        print('*--- Saving linear profile in file: <' + str(fileName) + '.py> ---*')
        candidates = self.candidates
        voters = self.voters
        linearBallot = self.linearBallot
        saveFileName = str(fileName)+str('.py')
        fo = open(saveFileName, 'w')
        fo.write('# Saved linear voting profile: \n')
        fo.write('from collections import OrderedDict \n')
        fo.write('candidates = OrderedDict([\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + str(x)+ '\'},\n')
            fo.write('(\'%s\', {\'name\': \'%s\'}),\n' % (x,candidateName) )
        fo.write('])\n')
        fo.write('voters = OrderedDict([\n')
        for v in voters:
            fo.write('(\'' +str(v)+'\', {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'}),\n')
        fo.write('])\n')
        fo.write('linearBallot = {\n')
        for v in linearBallot:
            fo.write('\'' +str(v)+'\': [\n')
            for x in linearBallot[v]:
                fo.write('\'' + str(x) + '\'' +',\n')
            fo.write('],\n')
        fo.write( '}\n')
        fo.close()

    def showLinearBallots(self,IntegerWeights=True):
        """
        show the linear ballots
        """
##        sumWeights = Decimal('0')
        if IntegerWeights:
            formStr = ' %s(%.0f):\t %s'
        else:
            formStr = ' %s(%.f):\t %s'
        print(' voters \t      marginal     ')
        print('(weight)\t candidates rankings')
        
        for v in self.voters:
##            sumWeights += self.voters[v]['weight']
            print(formStr \
                  % (str(v),self.voters[v]['weight'],
                     str(self.linearBallot[v])))
        print('# voters: ',str(self.sumWeights))

    def computeRankAnalysis(self):
        """
        compute the number of ranks each candidate obtains
        """
        ranks = {}
        candidatesList = [x for x in self.candidates]
        n = len(candidatesList)
        for x in candidatesList:
            ranks[x] = [0 for i in range(n)]
        for v in self.voters:
            for i in range(n):
                #print(v,i)
                try:
                    x = self.linearBallot[v][i]
                    #ranks[x][i] += 1
                    ranks[x][i] += self.voters[v]['weight']
                except:
                    pass
        #print ranks
        return ranks

    def showRankAnalysisTable(self,Sorted=True,ndigits=0,Debug=False):
        """
        Print the rank analysis tableau.
        
        If Sorted (True by default), the candidates
        are ordered by increasing Borda Scores.

        In case of decimal voters weights, ndigits allows
        to format the decimal precision of the numerical output.
        
        """
        print('*----  Borda rank analysis tableau -----*')
        bordaScores = self.computeBordaScores() 
        candidatesList = [(bordaScores[x]['BordaScore'],x) for x in self.candidates]
        if Sorted:
            candidatesList.sort()
        if Debug:
            print(candidatesList)
        nc = len(candidatesList)
        rankIndex = [i+1 for i in range(nc)]
        if Debug:
            print(nc,rankIndex)
        ranks = self.computeRankAnalysis()
        if Debug:
            print(ranks)
        if Debug:
            print(bordaScores)
            
        ## print table
        print(' candi- | alternative-to-rank       |      Borda')
        print(' dates  | ', end=' ')
        for x in rankIndex:
            print( str(x) + '   ', end=' ')
        print('| score  average')
        print('-------|-------------------------------------------------')
        for c in candidatesList:
            print('  \''+str(c[1])+'\' |', end=' ')
            for i in rankIndex:
                formatString = '%% .%df ' % ndigits
                print(formatString % (ranks[c[1]][(i-1)]), end='  ')
            formatString = ' | %% .%df     %%.2f' % ndigits
            print(formatString % (bordaScores[c[1]]['BordaScore'],\
                                  bordaScores[c[1]]['averageBordaScore']))      


    def computeBordaScores(self):
        """
        compute Borda scores from the rank analysis
        """
        from collections import defaultdict, OrderedDict
        from operator import itemgetter
        ranks = self.computeRankAnalysis()
        scores = []
        candidatesList = [x for x in self.candidates]
        n = len(candidatesList)
        for x in candidatesList:
            BordaScore_x = 0
            for i in range(n):
                BordaScore_x += (i+1)*ranks[x][i]
            averageBordaScore_x = BordaScore_x/self.sumWeights
            scores.append((BordaScore_x,x,averageBordaScore_x))
        scores.sort(key=itemgetter(0))
        BordaScores = OrderedDict([(x[1],
                            {'BordaScore':x[0],
                             'averageBordaScore':x[2]}) for x in scores])
        return BordaScores

    def showBordaRanking(self):
        """
        show Borda ranking in increasing order of the Borda score
        """
        BordaScores = self.computeBordaScores()
        print('Borda ranking of the candidates')
        for x in BordaScores:
            print(x,': ',BordaScores[x])
                  
    def computeBordaWinners(self):
        """
        compute the Borda winner from the Borda scores, ie the list of
        candidates with the minimal Borda score.
        """
        BordaScores = self.computeBordaScores()
        n = len(self.candidates)
        m = 0
        for v in self.voters:
            m += self.voters[v]['weight']
        BordaMinimum = n * m
        candidatesList = [x for x in self.candidates]
        for x in candidatesList:
            if BordaMinimum > BordaScores[x]['BordaScore']:
                BordaMinimum = BordaScores[x]['BordaScore']
        winners = [x for x in BordaScores \
                   if BordaScores[x]['BordaScore'] == BordaMinimum]
        return winners

    def computeInstantRunoffWinner(self,Comments=False):
        """
        compute the instant runoff winner from a linear voting ballot
        """
        from copy import deepcopy,copy
        from decimal import Decimal
        voters = copy(self.voters)
        votersList = [x for x in self.voters]
        totalWeight = Decimal("0.0")
        for v in votersList:
            totalWeight += Decimal('%.3f' % (voters[v]['weight']) )
        halfWeight = totalWeight/Decimal("2.0")
        if Comments:
            print('Total number of votes = ', totalWeight)
            print('Half of the Votes = ', halfWeight)
        candidates = copy(self.candidates)
        candidatesList = [x for x in candidates]
        remainingCandidates = copy(candidatesList)
        remainingLinearBallot = deepcopy(self.linearBallot)
        stage = 1
        while len(remainingCandidates) > 1:
            uninominalVotes = self.computeUninominalVotes(
                remainingCandidates,remainingLinearBallot)
            if Comments:
                print(' ==> stage = ', stage)
                print('    remaining candidates', remainingCandidates)
                print('    uninominal votes', uninominalVotes)
            minVotes = totalWeight
            maxVotes = Decimal("0.0")
            for x in uninominalVotes:
                if uninominalVotes[x] < minVotes:
                    minVotes = uninominalVotes[x]
                if uninominalVotes[x] > maxVotes:
                    maxVotes = uninominalVotes[x]
            if Comments:
                print('    minimal number of votes = ', minVotes)
                print('    maximal number of votes = ', maxVotes)
            if maxVotes <= halfWeight:
                currentCandidates = set(remainingCandidates)
                for x in currentCandidates:
                    if uninominalVotes[x] == minVotes:
                        if Comments:
                            print('    candidate to remove = ', x)
                        remainingCandidates.remove(x)
                        for v in voters:
                            try:
                                remainingLinearBallot[v].remove(x)
                            except:
                                pass
                if Comments:
                    print('    remaining candidates = ', remainingCandidates)
                    #print '    remaining ballots    = ', remainingLinearBallot
                stage += 1
            else:
                for x in remainingCandidates:
                    if uninominalVotes[x] == maxVotes:
                        if Comments:
                            print('    candidate %s obtains an absolute majority' % x)
                        return [x]
        return remainingCandidates

    def save2PerfTab(self,fileName='votingPerfTab',
                     isDecimal=True,NA=-9999,
                     valueDigits=2,NegativeWeights=True,
                     Comments=False):
        """
        Persistant storage of a linear voting profile in the format of a rank performance Tableau.
        For each voter *v*, the rank performance of candidate *x* corresponds to:

        number of candidates - linearProfile[v].index(x)
        
        """
        from copy import deepcopy
        if Comments:
            print('*--- Saving as performance tableau in file: <' \
                                       + str(fileName) + '.py> ---*')
        objectives = {}
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved performance Tableau: \n')
        fo.write('from decimal import Decimal\n')
        fo.write('from collections import OrderedDict\n')
        # actions
        nc = len(self.candidates)
        fo.write('actions = OrderedDict([\n')
        for x in self.candidates:
            fo.write('(\'%s\', {\n' % str(x))
            for it in self.candidates[x].keys():
                fo.write('\'%s\': %s,\n' \
                         % (it,repr(self.candidates[x][it])) )
            fo.write('}),\n')
        fo.write('])\n')
        # writing objectives if WithPolls
        if self.WithPolls:
            fo.write('objectives = OrderedDict([\n')
            p0 = [v for v in self.voters if self.voters[v]['party'] == 0]
            p1 = [v for v in self.voters if self.voters[v]['party'] == 1]
            p2 = [v for v in self.voters if self.voters[v]['party'] == 2]
            n0 = len(p0)
            n1 = len(p1)
            n2 = len(p2)          
            fo.write('(\'party0\',{\'name\':\'other\',\n')
            fo.write('\'weight\': %.2f,\n' % Decimal(str(n0)) )
            fo.write('\'criteria\': %s }),\n' % p0)
            fo.write('(\'party1\',{\'name\':\'party 1\',\n')
            fo.write('\'weight\': %.2f,\n' % Decimal(str(n1)) )
            fo.write('\'criteria\': %s }),\n' % p1)
            fo.write('(\'party2\',{\'name\':\'party 2\',\n')
            fo.write('\'weight\': %.2f,\n' % Decimal(str(n2)) )
            fo.write('\'criteria\': %s }),\n' % p2)
            fo.write('])\n')
        else:
            fo.write('objectives = OrderedDict()\n')  
        # criteria
        if self.WithPolls:
            NegativeWeights = False
        fo.write('criteria = OrderedDict([\n')
        for g in self.voters:
            fo.write('(\'%s\', {\'name\': \'%s\',\n' % (str(g),str(g)) )
            for it in self.voters[g].keys():
                if it == 'weight':
                    if NegativeWeights:
                        fo.write('\'%s\': %s,\n' \
                                 % (it,repr(-self.voters[g][it])))
                    else:
                        fo.write('\'%s\': %s,\n' \
                                 % (it,repr(self.voters[g][it])))
                else:
                    fo.write('\'%s\': %s,\n' % (it,repr(self.voters[g][it])))
            fo.write("\'scale\':(Decimal(1),Decimal(%d)),\n" % nc)
            fo.write("\'preferenceDirection\': \'%s\'" % 'min')
            fo.write('}),\n')
        fo.write('])\n')
        # evaluation
        fo.write('evaluation = {\n')
        for g in self.voters:
            fo.write('\'' +str(g)+'\': {\n')
            for x in self.candidates:
                if Decimal:
                    #fo.write('\'' + str(x) + '\':Decimal("' + str(evaluation[g][x]) + '"),\n')
                    evaluationString = '\'%%s\':Decimal("%%.%df"),\n' \
                                       % (valueDigits)
                    try:
                        xval = (self.linearBallot[g].index(x) + 1)
                    except:
                        xval = NA
                    if NegativeWeights:
                        fo.write(evaluationString % (x,Decimal(str(xval))))
                    else:
                        fo.write(evaluationString % (x,Decimal(str(-xval))))
                else:
                    fo.write('\'' + str(x) + '\':' \
                             + str(-evaluation[g][x]) + ',\n')
                    
            fo.write('},\n')
        fo.write('}\n')
        fo.write("NA = Decimal('%d')\n" % NA )
        fo.close()

    def showHTMLVotingHeatmap(self,criteriaList=None, 
                              actionsList=None,
                              fromIndex=None,
                              toIndex=None,
                              Transposed=True,
                              SparseModel=False,
                              minimalComponentSize=1, 
                              rankingRule='Copeland',
                              quantiles=None,
                              strategy='average', 
                              ndigits=0,
                              colorLevels=None, 
                              pageTitle='Voting Heatmap', 
                              Correlations=True,
                              Threading=False,
                              nbrOfCPUs=None,
                              Debug=False):
        """
        Show the linear voting profile as a rank performance heatmap.
        The linear voting profile is previously saved to a stored Performance Tableau.
        
        (see perfTabs.PerformanceTableau.showHTMLPerformanceHeatmap() )
        """
        from tempfile import mkdtemp
        tempDir = mkdtemp()
        perfTabFileName = '%s/votingPerfTab' % tempDir
        if SparseModel:
            self.save2PerfTab(perfTabFileName,_NegativeWeights=False)
        else:
            self.save2PerfTab(perfTabFileName)
        t = PerformanceTableau(perfTabFileName)
        t.showHTMLPerformanceHeatmap(criteriaList=criteriaList,
                            actionsList=actionsList,
                            fromIndex=fromIndex,toIndex=toIndex,
                            Transposed=Transposed,
                            SparseModel=SparseModel,
                            minimalComponentSize=minimalComponentSize,
                            rankingRule=rankingRule,
                            quantiles=quantiles, strategy=strategy, 
                            ndigits=ndigits, colorLevels=colorLevels,
                            pageTitle=pageTitle, Correlations=Correlations,
                            Threading=Threading, nbrOfCPUs=nbrOfCPUs,
                            Debug=Debug)

    def computeUninominalVotes(self,candidates=None,linearBallot=None):
        """
        compute uninominal votes for each candidate in candidates sublist
        and restricted linear ballots
        """
        if candidates==None:
            candidates = self.candidates
        if linearBallot is None:
            linearBallot = self.linearBallot
        uninominalVotes = {}
        for x in candidates:
            uninominalVotes[x] = 0
            for v in self.voters:
                if linearBallot[v][0] == x:
                    uninominalVotes[x] += self.voters[v]['weight']
        return uninominalVotes

    def computeSimpleMajorityWinner(self,Comments=False):
        """
        compute the winner in a uninominal Election from a linear ballot
        """
        uv = self.computeUninominalVotes(self.candidates,self.linearBallot)
        if Comments:
            print('uninominal votes ', uv)
        maxVotes = 0
        for x in self.candidates:
            if uv[x] > maxVotes:
                maxVotes = uv[x]
        if Comments:
            print('maxVotes ', maxVotes)
        simpleMajorityWinner = []
        for x in self.candidates:
            if uv[x] == maxVotes:
                simpleMajorityWinner.append(x)
        if Comments:
            print('simple majority winner(s) ', simpleMajorityWinner)
        return simpleMajorityWinner

class RandomLinearVotingProfile(LinearVotingProfile):
    """
    A specialized class for generating random liwear voting profiles.

    *Parameters*   
        * When *WithPolls* is True, each party supporting voter's linear ballot is randomly oriented
          by one of two random exponential poll results. The corresponding polls are stored
          in self.poll1, respectively self.poll2.
        * The *partyRepartition* sets the theoretical distribution of the two polls over the
          set of voters. If set to 0.0 or 1.0, only self.poll2, resp. self.poll1, will orient
          the respective party supporters.
        * The *other* paraemter sets the theoretical proportion of non party supporters.
        * The *DivisivePolitics* flag provides, if True, two reversed polls for
          generating the random linear ballots. 
        * The *votersWeights* parameter may be a list of positive integers in order to
          deterministically attribute weights to the voters.
          Is ignored when *RandomWeights* is True.
        * When *voterWeights* are None and *RandomWeights* is False, each voter
          obtains a single vote (default setting).
        * With *PartialLnearBallots* set to *True*, the linear voting ballots will be
          randomly shortened with the *lengthProbability* parameter.
          
    """
    def __init__(self,numberOfVoters=10,
                 numberOfCandidates=5,
                 IntraGroup=False,
                 votersIdPrefix='v',
                 candidatesIdPrefix='c',
                 PartialLinearBallots=False,
                 lengthProbability=0.5,
                 WithPolls=False,
                 partyRepartition=0.5,
                 other=0.05,
                 DivisivePolitics=False,
                 votersWeights=None,
                 RandomWeights=False,
                 seed=None,Debug=False):
        """
        """
        from collections import OrderedDict
        import random
        if seed is None:
            seed = random.random()
        random.seed(seed)
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = OrderedDict()
        nd = len(str(numberOfVoters))
        for v in votersList:
            voterID = ('%s%%0%dd' % (votersIdPrefix,nd)) % (v)
            if votersWeights is not None:
                try:
                    weight = votersWeights[v-1]
                except:
                    weight = 1
            else:
                if RandomWeights:
                    weight = random.randint(1,numberOfVoters)
                else:
                    weight = 1
            voters[voterID] = {'weight':Decimal('%d' % weight)}
        if IntraGroup:
            candidates = voters
        else:
            candidatesList = [x for x in range(1,numberOfCandidates + 1)]
            candidates = OrderedDict()
            na = len(str(numberOfCandidates))
            for c in candidatesList:
                candidateID =('%s%%0%dd' % (candidatesIdPrefix,na)) % (c)
                candidates[candidateID] = {'name': 'Candidate '+ candidateID}
        # store instance attributes
        self.name = str('randLinearProfile')
        self.seed = seed
        self.candidates = candidates
        self.voters = voters
        self.IntraGroup = IntraGroup
        self.WithPolls = WithPolls
        self.RandomWeights = RandomWeights
        self.sumWeights = Decimal('0')
        for v in self.voters:
            self.sumWeights += self.voters[v]['weight']
        if WithPolls:
            self.linearBallot \
                = self.generateRandomLinearBallotWithPoll(
                        partyRepartition,other,DivisivePolitics,
                        seed=seed,Debug=Debug)
        else:
            self.linearBallot = self.generateRandomLinearBallot(
                        PartialLinearBallots=PartialLinearBallots,
                        lengthProbability=lengthProbability,
                        seed=seed)
        self.ballot = self.computeBallot()


    def generateRandomLinearBallot(self,
                        PartialLinearBallots=False,
                        lengthProbability=0.5,
                                   seed=None,Debug=False):
        """
        Renders a randomly generated linear ballot.
        """
        from random import shuffle
##        random.seed(seed)
        linearBallot = {}
        voters = self.voters
        if Debug:
            print(candidatesList)
        for v in voters:
            candidatesList = [x for x in self.candidates]
            if self.IntraGroup:
                candidatesList.remove(v)
            n = len(candidatesList)
            shuffle(candidatesList)
            if Debug:
                print(v,candidatesList)
            if PartialLinearBallots:
                from randomNumbers import\
                     BinomialRandomVariable
                length = BinomialRandomVariable(n,lengthProbability)
                linearBallot[v] = candidatesList[:length.random()]
            else:
                linearBallot[v] = candidatesList.copy()
        return linearBallot

    def generateRandomLinearBallotWithPoll(self,partyRepartition,
                                           other,DivisivePolitics,
                                           seed=None,Debug=False):
        """
        Renders a random linear ballot in accordance with the given polls:
        self.poll1 and self.poll2.

        Polls are distributed in the *bipartisan* proportion.
        
        """
        import random
        random.seed(seed)
        from randomNumbers import DiscreteRandomVariable
        voters = self.voters
        candidatesList = [x for x in self.candidates]
        if Debug:
            print(candidatesList)
        nc = len(candidatesList)
          
        # divisive or independent polls
        poll1 = {}
        sumPoll = 0.0
        for c in candidatesList:
            poll1[c] = random.expovariate(1)
            sumPoll += poll1[c]
        for c in poll1:
            poll1[c] /= sumPoll
        self.poll1 = poll1
        poll2 = {}
        sumPoll = 0.0
        if DivisivePolitics:
            p1 = [(poll1[c],c) for c in candidatesList]
            p1 = list(sorted(p1))
            p2 = list(reversed(p1))
            if Debug:
                print(p1,p2)
            nc = len(candidatesList)
            for i in range(nc):
            #for c in candidatesList:
                #c = candidatesList[i]
                #poll2[c] = random.expovariate(1)
                c = p1[i][1]
                poll2[c] = p2[i][0]
                sumPoll += poll2[c]
        else:
            for c in candidatesList:
                poll2[c] = random.expovariate(1)
                sumPoll += poll2[c]
        for c in poll2:
            poll2[c] /= sumPoll

        # storing polls    
        self.poll1 = poll1
        self.poll2 = poll2
        self.other = other
        self.partyRepartition = partyRepartition
        if Debug:
            print(poll1,poll2,other,partyRepartition)

        # generating random linear ballots
        linearBallot = {}
        j = 1
        for v in voters:
            # each voter is attached to one of the polls
            u = random.random()
            if u < other: # random voting
                otherCandidatesList = list(candidatesList)
                random.shuffle(otherCandidatesList)
                voters[v]['party'] = 0
                linearBallot[v] = otherCandidatesList
            else:  # poll driven random
                
                if partyRepartition < random.random():
                    pollv = poll1
                    voters[v]['party'] = 1
                else:
                    pollv = poll2
                    voters[v]['party'] = 2
                # generating a random linear ranking    
                shuffledCandidatesList = []
                for i in range(nc-1):
                    NotShuffled = True
                    currPoll = pollv.copy()
                    rdv = DiscreteRandomVariable(currPoll,seed=j)
                    while NotShuffled:
                        xc = rdv.random()
                        if xc not in shuffledCandidatesList:
                            NotShuffled = False
                    shuffledCandidatesList.append(xc)
                    currPoll.pop(xc)
##                    if Debug:
##                        print(i,shuffledCandidatesList)
                            
                shc = set(shuffledCandidatesList)
                sc = set(candidatesList)
                xc = (sc-shc).pop()
                shuffledCandidatesList.append(xc)
##                if Debug:
##                    print('==>>', v,shuffledCandidatesList)           
                j += 1
                linearBallot[v] = shuffledCandidatesList
            
        return linearBallot

    def showRandomPolls(self,Debug=False):
        """
        Shows the random polls, the case given.
        """
        from operator import itemgetter
        try:
            poll1 = [(self.poll1[x],x) for x in self.poll1]
        except:
            poll1 = []
        nc = len(poll1)
        if nc > 1:
            voters = self.voters
            nv = len(voters)
            supportersParty1 = [x for x in voters if voters[x]['party'] == 1]
            supportersParty2 = [x for x in voters if voters[x]['party'] == 2]
            otherSupporters = [x for x in voters if voters[x]['party'] == 0]
            n0 = len(otherSupporters)
            p0 = float(n0)/float(nv)
            n1 = len(supportersParty1)
            p1 = float(n1)/float(nv)
            n2 = len(supportersParty2)
            p2 = float(n2)/float(nv)
            if Debug:
                print(n1,p1,n2,p2,n0,p0)
            poll1.sort(reverse=True,key=itemgetter(0))
            poll2 = [(self.poll2[x],x) for x in self.poll2]
            poll2.sort(reverse=True,key=itemgetter(0))
            poll = []
            for x in self.candidates:
                res = p1 * self.poll1[x] +\
                      p2 * self.poll2[x]
                poll.append( (res,x) )
            poll.sort(reverse=True,key=itemgetter(0))
            # print polls
            print('Random repartition of voters')
            print(' Party-1 supporters : %d (%05.2f%%)' % (n1,p1*100))
            print(' Party-2 supporters : %d (%05.2f%%)' % (n2,p2*100))
            print(' Other voters       : %d (%05.2f%%)' % (n0,p0*100))
            print('*---------------- random polls ---------------')
            print(' Party-1(%04.1f%%) | Party-2(%04.1f%%)|   expected  '\
                                             % (p1*100, p2*100) )
            print('-----------------------------------------------')
            for i in range(nc):
                print("  %s : %05.2f%%  |  %s : %05.2f%%  |  %s : %05.2f%%" %\
                        (poll1[i][1],poll1[i][0]*100.0,
                                      poll2[i][1],poll2[i][0]*100.0,
                                               poll[i][1], poll[i][0]*100.0) )
        else:
            print('No polls defined !')

class BipolarApprovalVotingProfile(VotingProfile):
    """
    A specialised class for approval-disapproval voting profiles.

    Structure::

        candidates = OrderedDict([('a', {'name': ...}),
                                  ('b', {'name': ...}),
                                   ...,   ...          ])
        voters = OrderedDict([('v1',{'weight':1.0}),('v2':{'weight':1.0}), ...])
        ## each voter characterises the candidates 
        ## he approves (+1), disapproves (-1) or ignores (0).
        approvalBallot = {
            'v1' : {'a': Decima('1'), 'b': Decimal('0'), ...}, 
            'v2' : {'a': Decima('0'), 'b': Decimal('-1'), ...},
            ...
            }
        ...
    """
    def __init__(self,fileVotingProfile=None,seed=None):
        if fileVotingProfile is not None:
            fileName = fileVotingProfile + '.py'
        ## else:
        ##     fileName = 'testapprovalvotingprofile.py'
            argDict = {}
            fi = open(fileName,'r')
            exec(compile(fi.read(), fileName, 'exec'), argDict)
            fi.close()
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            self.approvalBallot = argDict['approvalBallot']
            #self.disapprovalBallot = argDict['disapprovalBallot']
            self.netApprovalScores = self.computeNetApprovalScores()
            try:
                self.IntraGroup = argDict['IntraGroup']
            except:
                self.IntraGroup = False
            self.ballot = self.computeBallot()
        else:
            print('Error: a valid stored bipolar approval voting profile is required !')
            return
    def showBipolarApprovals(self):
        """
        Renders the approval and disapprovals per voter
        """
        print('Bipolar approval ballots')
        print('------------------------')
        for v in self.voters:
            app = [b for b in self.approvalBallot[v]\
                   if self.approvalBallot[v][b] == Decimal('1')]
            disapp = [b for b in self.approvalBallot[v]\
                   if self.approvalBallot[v][b] == Decimal('-1')]
            print(v, ':')
            print('Approvals   :',app)
            print('Disapprovals:',disapp)
            
        
    def showApprovalResults(self):
        """
        Renders the number of approvals obtained by each candidate.
        """
        from operator import itemgetter
        print('Approval results')
        candidates = [x for x in self.candidates]
        voters = self.voters
        Max = Decimal('1')
        Min = Decimal('-1')
        Med = Decimal('0')
        #candidates.sort()
        votesPerCandidate = {}
        for c in candidates:
            votesPerCandidate[c] = Decimal('0.0')
        ballot = self.approvalBallot
        sumApp = Decimal('0')
        for v in ballot:
            for c in ballot[v]:
                if ballot[v][c] > Med:
                    votesPerCandidate[c] += voters[v]['weight']
                    sumApp += voters[v]['weight']
        results = []
        for c in candidates:
            results.append((int(votesPerCandidate[c]),c))
        results.sort(reverse=True,key=itemgetter(0))
        for c in results:
            print(' Candidate: %s obtains %d votes' % (c[1],c[0] ))
        print('Total approval votes: %d' % (int(sumApp)) )
        tot = len(candidates) * len(voters)
        print('Approval proportion: %d/%d = %.2f' \
              % ( int(sumApp),tot,sumApp/Decimal(str(tot)) ) )

    def showDisapprovalResults(self):
        """
        Renders the number of disapprovals obtained by each candidate.
        """
        from operator import itemgetter
        print('Disapproval results')
        candidates = [x for x in self.candidates]
        voters = self.voters
        Max = Decimal('1')
        Min = Decimal('-1')
        Med = Decimal('0')
        #candidates.sort()
        votesPerCandidate = {}
        for c in candidates:
            votesPerCandidate[c] = Decimal('0.0')
        ballot = self.approvalBallot
        sumDisapp = Decimal('0')
        for v in ballot:
            for c in ballot[v]:
                if ballot[v][c] < Med:
                    votesPerCandidate[c] += voters[v]['weight']
                    sumDisapp += voters[v]['weight']
        results = []
        for c in candidates:
            results.append((int(votesPerCandidate[c]),c))
        results.sort(key=itemgetter(0))
        for c in results:
            print(' Candidate: %s obtains %d votes' % (c[1],c[0] ))
        print('Total disapproval votes: %d' % (int(sumDisapp)) )
        tot = len(candidates) * len(voters)
        print('Disapproval proportion: %d/%d = %.2f' \
                  % ( int(sumDisapp),tot,sumDisapp/Decimal(str(tot)) ) )

    def showHTMLVotingHeatmap(self,criteriaList=None, 
                              actionsList=None,
                              fromIndex=None,
                              toIndex=None,
                              Transposed=True,
                              rankingRule='NetFlows',
                              quantiles=None,
                              strategy='average', 
                              ndigits=0,
                              colorLevels=3, 
                              pageTitle='Voting Heatmap', 
                              Correlations=True,
                              Threading=False,
                              nbrOfCPUs=None,
                              Debug=False):
        """
        Show the linear voting profile as a rank performance heatmap.
        The linear voting profile is previously saved to a stored Performance Tableau.
        
        (see perfTabs.PerformanceTableau.showHTMLPerformanceHeatmap() )
        """
        from tempfile import mkdtemp
        tempDir = mkdtemp()
        perfTabFileName = '%s/votingPerfTab' % tempDir
        self.save2PerfTab(perfTabFileName)
        t = PerformanceTableau(perfTabFileName)
        t.showHTMLPerformanceHeatmap(criteriaList=criteriaList,
                            actionsList=actionsList,
                            fromIndex=fromIndex, toIndex=toIndex,
                            Transposed=Transposed,
                            rankingRule=rankingRule,
                            quantiles=quantiles, strategy=strategy,
                            ndigits=ndigits, colorLevels=colorLevels,
                            pageTitle=pageTitle, Correlations=Correlations,
                            Threading=Threading, nbrOfCPUs=nbrOfCPUs,
                            Debug=Debug)


    def computeNetApprovalScores(self,Debug=False):
        """
        Computes the approvals - disapprovals score obtained by each candidate.
        """
        from operator import itemgetter
        candidates = [x for x in self.candidates]
        voters = self.voters
        Max = Decimal('1')
        Min = Decimal('-1')
        Med = Decimal('0')
        #candidates.sort()
        votesPerCandidate = {}
        for c in candidates:
            votesPerCandidate[c] = Decimal('0.0')
        approved = self.approvalBallot
        #disapproved = self.disapprovalBallot
        for v in voters:
            for c in candidates:
                votesPerCandidate[c] += approved[v][c]*voters[v]['weight']
        results = []
        for c in candidates:
            results.append((int(votesPerCandidate[c]),c))
        results.sort(reverse=True,key=itemgetter(0))
        if Debug:
            print('Net Approval Scores')  
            for c in results:
                print('candidate: %s obtains %d net approvals' \
                                 % (c[1],c[0]) )
        return votesPerCandidate

    def showNetApprovalScores(self):
        """
        Prints the  approval - disapproval scores obtained by each candidate.
        """
        from operator import itemgetter
        candidates = self.candidates
        scores = self.netApprovalScores
        results = []
        for c in candidates:
            results.append((int(scores[c]),c))
        results.sort(reverse=True,key=itemgetter(0))
        print('Net Approval Scores')
        for c in results:
            print(' Candidate: %s obtains %d net approvals' \
                              % (c[1],c[0]) )

    def computeBallot(self,Debug=True):
        """
        Computes a complete ballot from the approval Ballot.

        """
        candidates = [x for x in self.candidates]
        n = len(candidates)
        app = self.approvalBallot
        Max = Decimal('1')
        Med = Decimal('0')
        Min = Decimal('-1')
        #DAVBallot = self.disapprovalBallot
        ballot = {}
        for v in app:
            av = app[v]
            ballot[v] = {}
            for x in candidates:
                ballot[v][x] = {}
                for y in candidates:
                    ballot[v][x][y] = Decimal("0.0")
            for i in range(n):
                x = candidates[i]
                for j in range(i+1,n):
                    y = candidates[j]
##                    if Debug:
##                        print(x,av[x],y,av[y])
                    if av[x] > av[y]:
                        ballot[v][x][y] = Max
                        ballot[v][y][x] = Min
                    elif av[x] < av[y]:
                        ballot[v][x][y] = Min
                        ballot[v][y][x] = Max
                    else:
                        ballot[v][x][y] = Med
        self.ballot = ballot
        return ballot

    def save(self,fileName='tempAVprofile'):
        """
        Persistant storage of a bipolar approval voting profile.

        Parameter:
            name of file (without <.py> extension!).
        """
        print('*--- Saving AV profile in file: <' + str(fileName) + '.py> ---*')
        candidates = self.candidates
        voters = self.voters
        approvalBallot = self.approvalBallot
        #disapprovalBallot = self.disapprovalBallot
        saveFileName = str(fileName)+str('.py')
        fo = open(saveFileName, 'w')
        fo.write('# Saved approval voting profile: \n')
        fo.write('from collections import OrderedDict\n')
        fo.write('from decimal import Decimal\n')
        fo.write('candidates = OrderedDict([\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + str(x)+ '\'},\n')
            fo.write('(\'%s\', {\'name\': \'%s\'}),\n' % (x,candidateName) )
        fo.write('])\n')
        fo.write('voters = OrderedDict([\n')
        for v in voters:
            fo.write('(\'' +str(v)+'\', {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'}),\n')
        fo.write('])\n')
        try:
            fo.write('IntraGroup = %s' % self.IntraGroup)
        except:
            fo.write('IntraGroup = %s' % False)
        fo.write('approvalProbability = %.2f\n' \
                                     % self.approvalProbability)
        fo.write('disapprovalProbability = %.2f\n' \
                                     % self.disapprovalProbability)
        fo.write('approvalBallot = {\n')
        for v in approvalBallot:
            fo.write('\'' +str(v)+'\': {\n')
            for x in approvalBallot[v]:
                fo.write('\'%s\': Decimal(\'%.f\'),\n' \
                          % (str(x),approvalBallot[v][x]) )
            fo.write('},\n')
        fo.write( '}\n')
##        fo.write('disapprovalBallot = {\n')
##        for v in disapprovalBallot:
##            fo.write('\'' +str(v)+'\': [\n')
##            for x in disapprovalBallot[v]:
##                fo.write('\'' + str(x) + '\'' +',\n')
##            fo.write('],\n')
##        fo.write( '}\n')
        fo.write('netVotingScores = {\n')
        for c in candidates:
            fo.write('\'%s\': Decimal(\'%.f\'),\n' \
                          % (str(c), self.netApprovalScores[c]))
        fo.write( '}\n') 
        fo.close()

    def save2PerfTab(self,fileName='votingPerfTab',valueDigits=2):
        """
        Persistant storage of an approval voting profile in the format of a standard performance tableau.
        For each voter *v*, the performance of candidate *x* corresponds to:

              1, if approved;
              -1, if disapproved;
              NA, missing evaluation otherwise,
        """
        from copy import deepcopy
        print('*--- Saving as performance tableau in file: <' \
                                      + str(fileName) + '.py> ---*')
        objectives = {}
        fileNameExt = str(fileName)+str('.py')
        fo = open(fileNameExt, 'w')
        fo.write('# Saved performance Tableau: \n')
        fo.write('from decimal import Decimal\n')
        fo.write('from collections import OrderedDict\n')
        # actions
        fo.write('actions = OrderedDict([\n')
        for x in self.candidates:
            fo.write('(\'%s\', {\n' % str(x))
            for it in self.candidates[x].keys():
                fo.write('\'%s\': %s,\n' \
                         % (it,repr(self.candidates[x][it])) )
            fo.write('}),\n')
        fo.write('])\n')
        # no objectives
        fo.write('objectives = OrderedDict()\n')            
        # criteria
        minScale = -1
        maxScale = 1
        medScale = 0
        NA = 999
        fo.write('criteria = OrderedDict([\n') 
        for g in self.voters:
            fo.write('(\'%s\', {\n' % str(g))
            for it in self.voters[g].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.voters[g][it])))
                fo.write("\'scale\':(Decimal(\'%d\'),Decimal(\'%d\')),\n" \
                         % (minScale,maxScale) )
            fo.write('}),\n')
        fo.write('])\n')
        # evaluation
        AVballot = self.approvalBallot
        Max = Decimal('1')
        Min = Decimal('-1')
        #DAVBallot = self.disapprovalBallot
        fo.write('NA = Decimal("%d")\n' % NA)
        fo.write('evaluation = {\n')
        for g in self.voters:
            fo.write('\'' +str(g)+'\': {\n')
            approved = AVballot[g]
            for x in self.candidates:
                evaluationString = '\'%%s\':Decimal("%%.%df"),\n' \
                                        % (valueDigits)
                if approved[x] == Max:
                    xval = maxScale
                elif approved[x] == Min:
                    xval = minScale
                else:  # ignored
                    xval = medScale
                fo.write(evaluationString % (x,Decimal(str(xval))))
            fo.write('},\n')
        fo.write( '}\n')
        fo.close()

# ------------------------
class RandomBipolarApprovalVotingProfile(BipolarApprovalVotingProfile,
                                         RandomLinearVotingProfile):
    """
    A specialized class for generating random approval-disapproval voting profiles
    with the help of random linear voting profiles.

    *approvalProbability* determines the number of first-ranked candidates approved
    *disapprovalProbability* determines the number of last-ranked candidates disapproved

    """
    def __init__(self,
                 numberOfVoters=100,
                 votersIdPrefix= 'v',
                 IntraGroup=False,
                 numberOfCandidates=15,
                 candidatesIdPrefix='c',
                 approvalProbability=0.25,
                 disapprovalProbability=0.3,
                 WithPolls=False,
                 partyRepartition=0.5,
                 other=0.05,
                 DivisivePolitics=False,
                 votersWeights=None,
                 RandomWeights=False,
                 seed=None,Debug=False):
        """
        Random profile creation parameters:
            | numberOfVoters=9, numberOfCandidates=5,
            | minSizeOfBallot=1, maxSizeOfBallot=2.
        """
        from collections import OrderedDict
        from votingProfiles import RandomLinearVotingProfile
        rlv = RandomLinearVotingProfile(
                 numberOfVoters=numberOfVoters,
                 votersIdPrefix=votersIdPrefix,
                 IntraGroup=IntraGroup,
                 numberOfCandidates=numberOfCandidates,
                 candidatesIdPrefix=candidatesIdPrefix,
                 WithPolls=WithPolls,
                 partyRepartition=partyRepartition,
                 other=other,
                 DivisivePolitics=DivisivePolitics,
                 votersWeights=votersWeights,
                 RandomWeights=RandomWeights,
                 seed=seed)
        if Debug:
            print(rlv)
            rlv.showRandomPolls()
        self.name = str('bipolarApprovalProfile')
        self.IntraGroup=IntraGroup
        self.candidates = rlv.candidates
        self.voters = rlv.voters
        self.seed = rlv.seed
        self.sumWeights = rlv.sumWeights
        self.WithPolls = rlv.WithPolls
        if WithPolls:
            self.poll1 = rlv.poll1
            self.poll2 = rlv.poll2
            self.other = rlv.other
            self.partyRepartition = rlv.partyRepartition
        self.linearBallot = rlv.linearBallot
        if approvalProbability <= 1.0 and approvalProbability >= 0.0:
            self.approvalProbability = approvalProbability
        else:
            print('!!! Invalid approval probability: %.3f' % approvalProbability)
            return
        if disapprovalProbability <= 1.0 and disapprovalProbability >= 0.0:
            self.disapprovalProbability = disapprovalProbability
        else:
            print('!!! Invalid disapproval probability: %.3f' % disapprovalProbability)
            return
        self.approvalBallot =\
                self._generateRandomApprovalBallot(rlv,
                     approvalProbability=approvalProbability,
                     disapprovalProbability=disapprovalProbability,
                     seed=seed,Debug=Debug)
        self.netApprovalScores = self.computeNetApprovalScores()
        self.ballot = self.computeBallot()

    def _generateRandomApprovalBallot(self,rlv,
                                      approvalProbability=0.25,
                                      disapprovalProbability=0.35,
                                      seed=None,Debug=True):
        """
        Renders a randomly generated approval ballot.
        """
        from randomNumbers import BinomialRandomVariable
        approvalBallot = {}
        #disapprovalBallot = {}
        voters = self.voters
        candidates = self.candidates
        nc = len(candidates)
        approvalNbr = BinomialRandomVariable(nc,approvalProbability)
        disapprovalNbr = BinomialRandomVariable(nc,disapprovalProbability)
        for v in voters:
            ac = approvalNbr.random()
            dc = disapprovalNbr.random()
            # !!! -0 == 0 so that [-0:] does not select [] as expected
            # !!!  but instead [0:] i.e. the complete list of n elements
            # !!! just like [-n:] 
            if Debug:
                print(v,nc,ac,dc)
            candidatesList = rlv.linearBallot[v]
            vApprovals = candidatesList[:ac]
            if dc > 0:
                vDisapprovals = candidatesList[-dc:]
            else:
                vDisapprovals = []
            for c in vApprovals:
                if c in vDisapprovals:
                    vDisapprovals.remove(c)                    
            if Debug:
                print(vApprovals)
                print(vDisapprovals)
            approvalBallot[v] = {}
            for c in candidates:
                if c in vApprovals and c not in vDisapprovals: 
                    approvalBallot[v][c] = Decimal('1')
                elif c in vDisapprovals and c not in vApprovals:
                    approvalBallot[v][c] = Decimal('-1')
                else:
                    approvalBallot[v][c] = Decimal('0')
            
        return approvalBallot

#--------------------------------
class MajorityMarginsDigraph(Digraph,VotingProfile):
    """
    Specialization of the general Digraph class for generating
    bipolar-valued marginal pairwise majority margins digraphs.

    Parameters:

        | stored voting profile (fileName of valid py code) or voting profile object
        | optional, coalition (sublist of voters)

    Example Python3 session

    >>> from votingProfiles import *
    >>> v = RandomLinearVotingProfile(numberOfVoters=101,
    ...                               numberOfCandidates=5)
    >>> v.showLinearBallots()
     voters 	      marginal     
    (weight)	 candidates rankings
     v001(1):	 ['c5', 'c3', 'c1', 'c4', 'c2']
     v002(1):	 ['c1', 'c3', 'c2', 'c5', 'c4']
     v003(1):	 ['c5', 'c1', 'c2', 'c4', 'c3']
     v004(1):	 ['c5', 'c1', 'c4', 'c2', 'c3']
     v005(1):	 ['c4', 'c5', 'c3', 'c1', 'c2']
     v006(1):	 ['c5', 'c1', 'c2', 'c4', 'c3']
    ...
    ...
    >>> g = MajorityMarginsDigraph(v,IntegerValuation=True)
    >>> g.showRelationTable()
    * ---- Relation Table -----
      S   |  'c1'   'c2'  'c3'	'c4'   'c5'	  
    ------|--------------------------------
     'c1' |    0     -3	   -9	-11	 1	 
     'c2' |    3      0	   -7	  7	-3	 
     'c3' |    9      7	    0	 17	-9	 
     'c4' |   11     -7	  -17	  0	-1	 
     'c5' |   -1      3	    9	  1	 0	 
    Valuation domain: [-101;+101]
    >>> g.computeCondorcetWinners()
    [']
    >>> g.exportGraphViz()
    *---- exporting a dot file for GraphViz tools ---------*
    Exporting to rel_randLinearProfile.dot
    dot -Grankdir=BT -Tpng rel_randLinearProfile.dot -o rel_randLinearProfile.png

    .. image:: rel_randLinearProfile.png
    
    
    """
    def __init__(self,argVotingProfile=None,
                 coalition=None,
                 IntegerValuation=True,
                 Debug=False):
        from copy import copy
        if isinstance(argVotingProfile, (VotingProfile,
                                         LinearVotingProfile,
                                         BipolarApprovalVotingProfile)):
            votingProfile = argVotingProfile
        elif argVotingProfile is not None:
            votingProfile = VotingProfile(argVotingProfile)
        else:
            print('Error: A valid voting profile has to be given!')
            return
        self.name = 'rel_' + votingProfile.name
        self.actions = copy(votingProfile.candidates)
        if coalition is None:
            voters = copy(votingProfile.voters)
        else:
            voters = {}
            for g in coalition:
                voters[g] = votingProfile.voters[g]
        self.criteria = voters
        self.ballot = copy(votingProfile.ballot)
        self.relation = self._constructMajorityMarginsRelation(
            IntegerValuation=IntegerValuation,Debug=Debug)
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()

    def _constructMajorityMarginsRelation(self,IntegerValuation=True,Debug=False):
        """
        Renders the marginal majority between candidates
        on the basis of an approval ballot.
        """
        candidates = set(self.actions)
        voters = self.criteria
        sumWeight = Decimal('0.0')
        for v in voters:
            sumWeight += Decimal(str(voters[v]['weight']))
        if Debug:
            print('sumweight',sumWeight)
        ballot = self.ballot
        relation = {}
        Med = Decimal('0')
        for x in candidates:
            relation[x] = {}
            for y in candidates:
                relation[x][y] = Med
        for v in voters:
            bv = ballot[v]
            for x in candidates:
                for y in candidates:
                    relation[x][y] += Decimal(str(bv[x][y]))\
                                      * Decimal(str(voters[v]['weight']))
        if Debug:
            print(relation)
        if IntegerValuation:
            Min = -sumWeight
            Max = sumWeight
            Med = Decimal('0')
        else:
            Min = Decimal('-1.0')
            Max = Decimal('1.0')
            Med = Decimal('0.0')
        self.valuationdomain = {'min': Min, 'med': Med, 'max':Max,
                                'hasIntegerValuation': IntegerValuation}
        if Debug:
            print(self.valuationdomain)
        if not IntegerValuation and Max != Decimal('0'):
            for x in candidates:
                for y in candidates:
                    relation[x][y] = relation[x][y]/sumWeight
        if Debug:
            print(relation)
        return relation

    def showMajorityMargins(self,**args):
        """
        Wrapper for the
        Digraph.showRelationTable(Sorted=True, IntegerValues=False,
        actionsSubset=None, relation=None, ndigits=2,
        ReflexiveTerms=True, fromIndex=None, toIndex=None)

        See the :py:meth:`digraphs.Digraph.showRelationTable` description.
        """
        Digraph.showRelationTable(self,**args)
        
class CondorcetDigraph(MajorityMarginsDigraph):
    """
    Dummy obsolete class name for MajorityMarginsDigraph class.
    """        

#----------test voting Digraph class ----------------
if __name__ == "__main__":
    #from transitiveDigraphs import *

    print('****************************************************')
    print('* Python voting digraphs module                    *')
    print('* $Revision: Python3.13 $                          *')
    print('* Copyright (C) 2006-2025 Raymond Bisdorff         *')
    print('* The module comes with ABSOLUTELY NO WARRANTY     *')
    print('* to the extent permitted by the applicable law.   *')
    print('* This is free software, and you are welcome to    *')
    print('* redistribute it if it remains free software.     *')
    print('****************************************************')

    print('*-------- Testing classes and methods -------')

    # adA = RandomBipolarApprovalVotingProfile(numberOfVoters=4,
    #                                          votersIdPrefix='a',
    #                                          IntraGroup=True,
    #                                          numberOfCandidates=5,
    #                                          approvalProbability=0.3,
    #                                          disapprovalProbability=0.3,
    #                                          candidatesIdPrefix='b',
    #                                          seed=1,Debug=True)
    # adA.showBipolarApprovals()
    # for a in adA.voters:
    #     adA.showVoterBallot(a)
##    adB = RandomBipolarApprovalVotingProfile(numberOfVoters=5,
##                                             votersIdPrefix='b',
##                                             approvalProbability=0.5,
##                                             disapprovalProbability=0.5,
##                                             numberOfCandidates=5,
##                                             candidatesIdPrefix='a')
##    pv = RandomPrerankedVotingProfile(numberOfVoters=5,
##                                     numberOfCandidates=15,
##                                     votersIdPrefix='a',
##                                     candidatesIdPrefix='b',
##                                      lengthProbability=0.3,
##                                     votersWeights=[1,2,3,4,5],
##                                     seed=1)
##    pv.showPrerankedBallots()
    
    k = 7
    lvA = RandomLinearVotingProfile(numberOfVoters=k,numberOfCandidates=k,
                                      votersIdPrefix='a',
                                      candidatesIdPrefix='b',
                                    PartialLinearBallots=False,
                                    lengthProbability=0.5,
                                 seed=50)
    lvA.save2BipolarApprovalVotingProfile(approvalIndex=2,disapprovalIndex=5)
##    lvB = RandomLinearVotingProfile(numberOfVoters=k,numberOfCandidates=k,
##                                      votersIdPrefix='b',
##                                    PartialLinearBallots=False,
##                                        candidatesIdPrefix='a',seed=114)
##
##    lvA.showLinearBallots()
##    lvB.showLinearBallots()
##    lvB.save('testpreorder')
    
##    v = RandomBipolarApprovalVotingProfile(numberOfVoters=1000,
##                                           numberOfCandidates=10,
##                                           approvalProbability=0.25,
##                                           disapprovalProbability=0.25,
##                                           seed=100,DivisivePolitics=True,
##                                           WithPolls=True,Debug=False)
##    print(v)
##    v.showApprovalResults()
##    v.showDisapprovalResults()
##    v.showNetApprovalScores()
##    v.save('testAV')
##    v = BipolarApprovalVotingProfile('testAV')
##    print(v)
##    v.save2PerfTab('testODG')
##    v.showHTMLVotingHeatmap(rankingRule='NetFlows',Transposed=False,Threading=True)
##    from outrankingDigraphs import BipolarOutrankingDigraph
##    g = BipolarOutrankingDigraph('testODG')
##    g.showHTMLPerformanceTableau(Transposed=True)
##    print(g)
##    v3 =
##    RandomLinearVotingProfile(votersIdPrefix='m',candidatesIdPrefix='w')
##    v3.showLinearBallots() m = MajorityMarginsDigraph(v3,Debug=True)
##    print(m) m.showRelationTable() # m.showBestChoiceRecommendation()
          
    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. September 2025               *')
    print('* $Revision: Python3.13 $           *')
    print('*************************************')

#############################
# Log record for changes:
# $Log: votingDigraphs.py,v $#
#############################
