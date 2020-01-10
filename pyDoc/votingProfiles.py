#!/usr/bin/env python3
"""
Python 3 implementation of voting digraphs
Refactored from revision 1.549 of the digraphs module
Current revision $Revision: 2484 $
Copyright (C) 2011-2019 Raymond Bisdorff

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

        if fileVotingProfile != None:
            fileName = fileVotingProfile+'.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            self.ballot = argDict['ballot']
        else:
            randv = RandomVotingProfile(seed=seed)
            self.name = 'randomCondorcet'
            self.candidates = randv.candidates
            self.voters = randv.voters
            self.ballot = randv.ballot

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
                print('voting of voter %s (weight = %.1f)' % (v,self.voters[v]['weight']))
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

    def save(self,name='tempVprofile'):
        """
        Persistant storage of an approval voting profile.
        """
        print('*--- Saving voting profile in file: <' + str(name) + '.py> ---*')
        candidates = self.candidates
        voters = self.voters
        ballot = self.ballot
        saveFileName = str(name)+str('.py')
        fo = open(saveFileName, 'w')
        fo.write('# Saved voting profile: \n')
        fo.write('from collections import OrderedDict \n')
        fo.write('candidates = OrderedDict([\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + candidateName + '\'},\n')
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
    
    >>> from votingDigraphs import *
    >>> v = RandomLinearVotingProfile(numberOfVoters=5,numberOfCandidates=3)
    >>> v.showLinearBallots()
    voters(weight)	 candidates rankings
    v4(1.0): 	 ['a1', 'a2', 'a3']
    v5(1.0): 	 ['a1', 'a2', 'a3']
    v1(1.0): 	 ['a2', 'a1', 'a3']
    v2(1.0): 	 ['a1', 'a2', 'a3']
    v3(1.0): 	 ['a1', 'a3', 'a2']
    >>> v.computeRankAnalysis()
    {'a1': [4.0, 1.0, 0],
     'a2': [1.0, 3.0, 1.0],
     'a3': [0, 1.0, 4.0]}
    >>> v.showRankAnalysisTable()
    *----  Rank analysis tableau -----*
      ranks |  1    2    3    | Borda score
     -------|------------------------------
       'a1' |  4    1    0    |   6
       'a2' |  1    3    1    |   10
       'a3' |  0    1    4    |   14
    >>> v.computeUninominalVotes()
    {'a1': 4.0, 'a3': 0, 'a2': 1.0}
    >>> v.computeSimpleMajorityWinner()
    ['a1']
    >>> v.computeBordaScores()
    {'a1': 6.0, 'a3': 14.0, 'a2': 10.0}
    >>> v.computeBordaWinners()
    ['a1']
    >>> v.computeInstantRunoffWinner()
    ['a1']

    """
    def __init__(self,fileVotingProfile=None,numberOfCandidates=5,numberOfVoters=9,seed=None):
        if fileVotingProfile != None:
            fileName = fileVotingProfile + '.py'
        ## else:
        ##     fileName = 'testapprovalvotingprofile.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            self.linearBallot = argDict['linearBallot']
            self.ballot = self.computeBallot()
        else:
            print('!!! Error: The name of a stored linear voting profile is required !!!')
            return
        self.sumWeights = Decimal('0')
        for v in self.voters:
            self.sumWeights += self.voters[v]['weight']

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

    def save(self,name='templinearprofile'):
        """
        Persistant storage of a linear voting profile.

        Parameter:
            name of file (without <.py> extension!).
        """
        print('*--- Saving linear profile in file: <' + str(name) + '.py> ---*')
        candidates = self.candidates
        voters = self.voters
        linearBallot = self.linearBallot
        saveFileName = str(name)+str('.py')
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
            print(formStr % (str(v),self.voters[v]['weight'],str(self.linearBallot[v])))
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
        scores.sort()
        BordaScores = OrderedDict([(x[1],{'BordaScore':x[0],'averageBordaScore':x[2]}) for x in scores])
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
        winners = [x for x in BordaScores if BordaScores[x]['BordaScore'] == BordaMinimum]
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
            uninominalVotes = self.computeUninominalVotes(remainingCandidates,remainingLinearBallot)
            if Comments:
                print('>>> stage = ', stage)
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

    def save2PerfTab(self,fileName='votingPerfTab',isDecimal=True,valueDigits=2):
        """
        Persistant storage of a linear voting profile in the format of a rank performance Tableau.
        For each voter *v*, the rank performance of candidate *x* corresponds to:

        number of candidates - linearProfile[v].index(x)
        """
        from copy import deepcopy
        print('*--- Saving as performance tableau in file: <' + str(fileName) + '.py> ---*')
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
                fo.write('\'%s\': %s,\n' % (it,repr(self.candidates[x][it])) )
            fo.write('}),\n')
        fo.write('])\n')
        # no objectives
        fo.write('objectives = OrderedDict()\n')            
        # criteria
        fo.write('criteria = OrderedDict([\n') 
        for g in self.voters:
            fo.write('(\'%s\', {\n' % str(g))
            for it in self.voters[g].keys():
                if it == 'weight':
                    fo.write('\'%s\': Decimal(\'%s\'),\n' % (it,repr(-self.voters[g][it])))
                else:
                    fo.write('\'%s\': Decimal(\'%s\'),\n' % (it,repr(self.voters[g][it])))
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
                    evaluationString = '\'%%s\':Decimal("%%.%df"),\n' % (valueDigits)
                    try:
                        xval = (self.linearBallot[g].index(x) + 1)
                    except:
                        xval = -999
                    fo.write(evaluationString % (x,Decimal(str(xval))))
                else:
                    fo.write('\'' + str(x) + '\':' + str(evaluation[g][x]) + ',\n')
                    
            fo.write('},\n')
        fo.write( '}\n')
        fo.close()

    def showHTMLVotingHeatmap(self,criteriaList=None, \
                              actionsList=None,\
                              SparseModel=False,\
                              minimalComponentSize=1, \
                              rankingRule='Copeland',\
                              quantiles=None,\
                              strategy='average', \
                              ndigits=0,\
                              colorLevels=None, \
                              pageTitle='Voting Heatmap', \
                              Correlations=True,\
                              Threading=False,\
                              nbrOfCPUs=1,\
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
        t.showHTMLPerformanceHeatmap(criteriaList=criteriaList, actionsList=actionsList,\
                              SparseModel=SparseModel, minimalComponentSize=minimalComponentSize, \
                              rankingRule=rankingRule, quantiles=quantiles, strategy=strategy, \
                              ndigits=ndigits, colorLevels=colorLevels, \
                              pageTitle=pageTitle, \
                              Correlations=True, Threading=Threading, nbrOfCPUs=nbrOfCPUs, Debug=Debug)
    


    def computeUninominalVotes(self,candidates=None,linearBallot=None):
        """
        compute uninominal votes for each candidate in candidates sublist
        and restricted linear ballots
        """
        if candidates==None:
            candidates = self.candidates
        if linearBallot == None:
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


class ApprovalVotingProfile(VotingProfile):
    """
    A specialised class for approval voting profiles

    Structure::

        candidates = OrderedDict([('a', {'name': ...}),
                      ('b', {'name': ...}),
                      ..., ...])
        voters = OrderedDict([('v1',{'weight':1.0}),('v2':{'weight':1.0}), ...])
        ## each specifies the subset of candidates he approves on
        approvalBallot = {
            'v1' : ['b'],
            'v2' : ['a','b'],
            ...
            }

        ## each specifies the subset -disjoint from the approvalBallot-  of candidates he disapproves on
        disApprovalBallot = {
            'v1' : ['a'],
            'v2' : [],
            ...
            }
    """
    def __init__(self,fileVotingProfile=None,seed=None):
        if fileVotingProfile != None:
            fileName = fileVotingProfile + '.py'
        ## else:
        ##     fileName = 'testapprovalvotingprofile.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            self.approvalBallot = argDict['approvalBallot']
            try:
                self.disApprovalBallot = argDict['disApprovalBallot']
            except:
                self.disApprovalBallot = {}
                for v in self.approvalBallot:
                    self.disApprovalBallot[v] = []
            self.ballot = self.computeBallot()
        else:
            randv = RandomApprovalVotingProfile(seed=seed)
            self.name = 'randApprovalVotingProfile'
            self.candidates = randv.candidates
            self.voters = randv.voters
            self.ballot = randv.ballot

    def showApprovalResults(self):
        """
        Renders the approval obtained by each candidates.
        """
        print('Approval results')
        candidates = [x for x in self.candidates]
        #candidates.sort()
        votesPerCandidate = {}
        for c in candidates:
            votesPerCandidate[c]=0.0
        ballot = self.approvalBallot
        for v in ballot:
            for c in ballot[v]:
                votesPerCandidate[c] += 1.0
        results = []
        for c in candidates:
            results.append((int(votesPerCandidate[c]),c))
        results.sort(reverse=True)
        for c in results:
            print('candidate: %s obtains %d votes' % (c[1],c[0] ))

    def showDisApprovalResults(self):
        """
        Renders the disapprovals obtained by each candidates.
        """
        print('Disapproval results')
        candidates = [x for x in self.candidates]
        #candidates.sort()
        votesPerCandidate = {}
        for c in candidates:
            votesPerCandidate[c]=0.0
        ballot = self.disApprovalBallot
        for v in ballot:
            for c in ballot[v]:
                votesPerCandidate[c] += 1.0
        results = []
        for c in candidates:
            results.append((int(votesPerCandidate[c]),c))
        results.sort(reverse=True)
        for c in results:
            print('candidate: %s obtains %d votes' % (c[1],c[0] ))

    def showResults(self):
        self.showApprovalResults()
        self.showDisApprovalResults()

    def computeBallot(self):
        """
        Computes a complete ballot from the approval Ballot.

        Parameters:
            approvalEquivalence=False, disapprovalEquivalence=False.
        """
        candidates = set(self.candidates)
        AVballot = self.approvalBallot
        DAVBallot = self.disApprovalBallot
        ballot = {}
        for v in AVballot:
            ballot[v] = {}
            for x in candidates:
                ballot[v][x] = {}
                for y in candidates:
                    ballot[v][x][y] = Decimal("0.0")
            voted = set(AVballot[v])
            non_voted = set(DAVBallot[v])
            maybe = candidates - (voted | non_voted)
            for x in candidates:
                for y in candidates:
                    if x != y:
                        if x in voted and y in voted:
                            ballot[v][x][y] = Decimal("0.0")
                        elif x in voted and y in maybe:
                            ballot[v][x][y] = Decimal("1.0")
                        elif x in voted and y in non_voted:
                            ballot[v][x][y] = Decimal("1.0")   
                        elif x in maybe and y in voted:
                            ballot[v][x][y] = Decimal("-1.0")
                        elif x in maybe and y in maybe:
                            ballot[v][x][y] = Decimal("0.0")
                        elif x in maybe and y in non_voted:
                            ballot[v][x][y] = Decimal("1.0")
                        elif x in non_voted and y in voted:
                            ballot[v][x][y] = Decimal("-1.0")
                        elif x in non_voted and y in maybe:
                            ballot[v][x][y] = Decimal("-1.0")
                        elif x in non_voted and y in non_voted:
                            ballot[v][x][y] = Decimal("0.0")    
        self.ballot = ballot
        return ballot

##    def computeBallot(self,approvalEquivalence=False,disapprovalEquivalence=False):
##        """
##        Computes a complete ballot from the approval Ballot.
##
##        Parameters:
##            approvalEquivalence=False, disapprovalEquivalence=False.
##        """
##        candidates = set(self.candidates)
##        AVballot = self.approvalBallot
##        ballot = {}
##        for v in AVballot:
##            ballot[v] = {}
##            for x in candidates:
##                ballot[v][x] = {}
##                for y in candidates:
##                    ballot[v][x][y] = Decimal("0.0")
##            voted = set(AVballot[v])
##            non_voted = candidates - voted
##            if approvalEquivalence:
##                for x in voted:
##                    for y in voted:
##                        ballot[v][x][y] = Decimal("1.0")
##            if disapprovalEquivalence:
##                for x in non_voted:
##                    for y in non_voted:
##                        ballot[v][x][y] = Decimal("1.0")
##            for x in voted:
##                for y in non_voted:
##                    ballot[v][x][y] = Decimal("1.0")
##                    ballot[v][y][x] = Decimal("-1.0")
##            for x in candidates:
##                ballot[v][x][x] = Decimal("-1.0")
##        self.ballot = ballot
##        return ballot

    def save(self,name='tempAVprofile'):
        """
        Persistant storage of an approval voting profile.

        Parameter:
            name of file (without <.py> extension!).
        """
        print('*--- Saving AV profile in file: <' + str(name) + '.py> ---*')
        candidates = self.candidates
        voters = self.voters
        approvalBallot = self.approvalBallot
        saveFileName = str(name)+str('.py')
        fo = open(saveFileName, 'w')
        fo.write('# Saved approval voting profile: \n')
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
        for v in approvalBallot:
            fo.write('\'' +str(v)+'\': [\n')
            for x in approvalBallot[v]:
                fo.write('\'' + str(x) + '\'' +',\n')
            fo.write('],\n')
        fo.write( '}\n')
        fo.close()

    def save2PerfTab(self,fileName='votingPerfTab',isDecimal=True,valueDigits=2):
        """
        Persistant storage of an approval voting profile in the format of a standard performance tableau.
        For each voter *v*, the performance of candidate *x* corresponds to:

              1, if approved;
              0, if disapproved;
              -999, miising evalaution otherwise,
        """
        from copy import deepcopy
        print('*--- Saving as performance tableau in file: <' + str(fileName) + '.py> ---*')
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
                fo.write('\'%s\': %s,\n' % (it,repr(self.candidates[x][it])) )
            fo.write('}),\n')
        fo.write('])\n')
        # no objectives
        fo.write('objectives = OrderedDict()\n')            
        # criteria
        minScale = 0
        maxScale = 1
        fo.write('criteria = OrderedDict([\n') 
        for g in self.voters:
            fo.write('(\'%s\', {\n' % str(g))
            for it in self.voters[g].keys():
                fo.write('\'%s\': %s,\n' % (it,repr(self.voters[g][it])))
                fo.write("\'scale\':(Decimal(\'%d\'),Decimal(\'%d\')),\n" % (minScale,maxScale) )
            fo.write('}),\n')
        fo.write('])\n')
        # evaluation
        AVballot = self.approvalBallot
        DAVBallot = self.disApprovalBallot
        fo.write('evaluation = {\n')
        for g in self.voters:
            fo.write('\'' +str(g)+'\': {\n')
            approved = AVballot[g]
            disapproved = DAVBallot[g]
            for x in self.candidates:
                if Decimal:
                    #fo.write('\'' + str(x) + '\':Decimal("' + str(evaluation[g][x]) + '"),\n')
                    evaluationString = '\'%%s\':Decimal("%%.%df"),\n' % (valueDigits)
                    if x in approved:
                        xval = maxScale
                    elif x in disapproved:
                        xval = minScale
                    else:  # ,issing evaluation
                        xval = -999
                    fo.write(evaluationString % (x,Decimal(str(xval))))
                else:
                    fo.write('\'' + str(x) + '\':' + str(evaluation[g][x]) + ',\n')
                    
            fo.write('},\n')
        fo.write( '}\n')
        fo.close()


class RandomApprovalVotingProfile(ApprovalVotingProfile):
    """
    A specialized class for approval voting profiles.
    """
    def __init__(self,numberOfVoters=9,numberOfCandidates=5,minSizeOfBallot=1,maxSizeOfBallot=2,seed=None):
        """
        Random profile creation parameters:
            | numberOfVoters=9, numberOfCandidates=5,
            | minSizeOfBallot=1, maxSizeOfBallot=2.
        """
        from collections import OrderedDict
##        import random
##        random.seed(seed)
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = OrderedDict()
        for v in votersList:
            voterID = 'v%d' % v
            voters[voterID] = {'weight':1.0}
        candidatesList = [x for x in range(1,numberOfCandidates + 1)]
        candidates = OrderedDict()
        for c in candidatesList:
            candidateID = 'a%d' % c
            candidates[candidateID] = {'name': candidateID}
        self.name = str('randAVProfile')
        self.candidates = candidates
        self.voters = voters
        self.approvalBallot = self.generateRandomApprovalBallot(minSizeOfBallot,maxSizeOfBallot,seed=seed)
        self.disApprovalBallot = self.generateRandomDisApprovalBallot(minSizeOfBallot,maxSizeOfBallot,seed=seed)
        self.ballot = self.computeBallot()

    def generateRandomApprovalBallot(self,minSizeOfBallot,maxSizeOfBallot,seed=None):
        """
        Renders a randomly generated approval ballot.
        """
        import random,copy
        random.seed(seed)
        approvalBallot = {}
        voters = self.voters
        candidates = self.candidates
        nc = len(candidates)
        for v in voters:
            candidatesList = list(candidates.keys())
            approvalBallot[v] = []
            nb = random.randint(minSizeOfBallot,maxSizeOfBallot)
            for x in range(nb):
                if candidatesList != []:
                    bx = random.choice(candidatesList)
                    approvalBallot[v].append(bx)
                    candidatesList.remove(bx)
        return approvalBallot

    def generateRandomDisApprovalBallot(self,minSizeOfBallot,maxSizeOfBallot,seed=None):
        """
        Renders a randomly generated approval ballot.
        """
        import random,copy
        random.seed(seed)
        disApprovalBallot = {}
        voters = self.voters
        candidates = self.candidates
        nc = len(candidates)
        for v in voters:
            candidatesList = list(candidates.keys())
            disApprovalBallot[v] = []
            nb = random.randint(minSizeOfBallot,maxSizeOfBallot)
            for x in range(nb):
                if candidatesList != []:
                    bx = random.choice(candidatesList)
                    if bx not in self.approvalBallot[v]:
                        disApprovalBallot[v].append(bx)
                    candidatesList.remove(bx)
        return disApprovalBallot

class RandomLinearVotingProfile(LinearVotingProfile):
    """
    A specialized class for random linwear voting profiles.
    Random reation parameters:
    
        numberOfVoters=5, numberOfCandidates=5,
        votersWeights = optional list of positive integers for instance [2,3,4,1,5].
        
    """
    def __init__(self,numberOfVoters=9,numberOfCandidates=5,votersWeights=None,seed=None):
        """
        """
        from collections import OrderedDict
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = OrderedDict()
        for v in votersList:
            voterID = 'v%d' % v
            if votersWeights != None:
                try:
                    weight = votersWeights[v-1]
                except:
                    weight = 1
            else:
                weight = 1
            voters[voterID] = {'weight':Decimal('%d' % weight)}
        candidatesList = [x for x in range(1,numberOfCandidates + 1)]
        candidates = OrderedDict()
        for c in candidatesList:
            candidateID = 'a%d' % c
            candidates[candidateID] = {'name': candidateID}
        self.name = str('randLinearProfile')
        self.candidates = candidates
        self.voters = voters
        self.sumWeights = Decimal('0')
        for v in self.voters:
            self.sumWeights += self.voters[v]['weight']
        self.linearBallot = self.generateRandomLinearBallot(seed)
        #print self.linearBallot
        self.ballot = self.computeBallot()


    def generateRandomLinearBallot(self,seed):
        """
        Renders a randomly generated linear ballot.
        """
        import random
        random.seed(seed)
        linearBallot = {}
        voters = self.voters
        candidateList = [x for x in self.candidates]
        #print candidateList
        for v in voters:
            random.shuffle(candidateList)
            #print candidateList
            linearBallot[v] = candidateList.copy()
        return linearBallot

class RandomVotingProfile(VotingProfile):
    """
    A subclass for generating random voting profiles.
    """
    def __init__(self,numberOfVoters=9,numberOfCandidates=5,\
                 hasRandomWeights=False,maxWeight=10,seed=None,Debug=False):
        """
        Random profile creation parameters:

            | numberOfVoters=9,
            | numberOfCandidates=5

        """
        from collections import OrderedDict
        import random
        random.seed(seed)
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = OrderedDict()
        for v in votersList:
            voterID = 'v%d' % v
            if hasRandomWeights:
                voters[voterID] = {'weight':random.randint(1,maxWeight)}
            else:
                voters[voterID] = {'weight':1}
        candidatesList = [x for x in range(1,numberOfCandidates + 1)]
        candidates = OrderedDict()
        for x in candidatesList:
            candidateID = 'a%d' % x
            candidates[candidateID] = {'name': candidateID}
        self.name = str('randAVProfile')
        self.candidates = candidates
        self.voters = voters
        self.ballot = self.generateRandomBallot(seed=seed,Debug=Debug)
        if Debug:
            self.showAll()

    def generateRandomBallot(self,seed,Debug=False):
        """
        Renders a randomly generated approval ballot
        from a shuffled list of candidates for each voter.
        """
        import random
        if seed != None:
            random.seed(seed)
        ballot = {}
        voters = [x for x in self.voters]
        candidatesList = [x for x in self.candidates]
        nc = len(candidatesList)
        for v in voters:
            ballot[v] = {}
            for i in range(nc):
                ballot[v][candidatesList[i]] = {}
                for j in range(nc):
                    ballot[v][candidatesList[i]][candidatesList[j]] = 0.0
            random.shuffle(candidatesList)
            if Debug:
                print(v, candidatesList)
            for i in range(nc):
                for j in range(i+1,nc):
                    ballot[v][candidatesList[i]][candidatesList[j]] = 1.0
                    ballot[v][candidatesList[j]][candidatesList[i]] = -1.0
        return ballot

#--------------------------------
class CondorcetDigraph(Digraph):
    """
    Specialization of the general Digraph class for generating
    bipolar-valued marginal pairwise majority difference digraphs.

    Parameters:

        | stored voting profile (fileName of valid py code) or voting profile object
        | optional, coalition (sublist of voters)

    Example Python3 session

    >>> from votingDigraphs import *
    >>> v = RandomLinearVotingProfile(numberOfVoters=101,numberOfCandidates=5)
    >>> v.showLinearBallots()
    v101(1.0): 	 ['a5', 'a1', 'a2', 'a4', 'a3']
    v100(1.0): 	 ['a4', 'a1', 'a5', 'a3', 'a2']
    v89(1.0): 	 ['a4', 'a5', 'a1', 'a2', 'a3']
    v88(1.0): 	 ['a3', 'a2', 'a5', 'a1', 'a4']
    v87(1.0): 	 ['a5', 'a2', 'a4', 'a3', 'a1']
    v86(1.0): 	 ['a5', 'a3', 'a1', 'a4', 'a2']
    v85(1.0): 	 ['a5', 'a3', 'a2', 'a4', 'a1']
    v84(1.0): 	 ['a3', 'a1', 'a2', 'a4', 'a5']
    ...
    ...
    >>> g = CondorcetDigraph(v,hasIntegerValuation=True)
    >>> g.showRelationTable()
    * ---- Relation Table -----
     S   |  'a1'  'a2'	 'a3'	'a4'  'a5'	  
    -----|------------------------------------------------------------
    'a1' |   -	   33	  9	 11    21	 
    'a2' |  -33	   -	 -19	 -1    -5	 
    'a3' |  -9	   19	 -	 5     -1	 
    'a4' |  -11	   1	  -5	 -     -9	 
    'a5' |  -21	   5	   1	 9      -
    >>> g.computeCondorcetWinner()
    ['a1']
    >>> g.exportGraphViz()
    *---- exporting a dot file dor GraphViz tools ---------*
    Exporting to rel_randLinearProfile.dot
    dot -Grankdir=BT -Tpng rel_randLinearProfile.dot -o rel_randLinearProfile.png

    .. image:: rel_randLinearProfile.png
    
    
    """
    def __init__(self,argVotingProfile=None,\
                 approvalVoting=False,coalition=None,\
                 majorityMargins=True,hasIntegerValuation=True):
        from copy import copy
        if isinstance(argVotingProfile, (VotingProfile,ApprovalVotingProfile)):
            votingProfile = argVotingProfile
        else:
            if argVotingProfile == None:
                votingProfile = VotingProfile()
            elif approvalVoting:
                votingProfile = ApprovalVotingProfile(argVotingProfile)
            else:
                votingProfile = VotingProfile(argVotingProfile)
        self.name = 'rel_' + votingProfile.name
        self.actions = copy(votingProfile.candidates)
        if coalition == None:
            voters = copy(votingProfile.voters)
        else:
            voters = {}
            for g in coalition:
                voters[g] = votingProfile.voters[g]
        self.voters = voters
        if isinstance(votingProfile, (VotingProfile)):
            self.ballot = copy(votingProfile.ballot)
            self.relation = self.constructBallotRelation(hasIntegerValuation)
        elif isinstance(votingProfile, (ApprovalVotingProfile)):
            self.approvalBallot = copy(votingProfile.approvalBallot)
            if majorityMargins:
                self.relation = self.constructMajorityMarginsRelation(hasIntegerValuation)
            else:
                self.relation = self.constructApprovalBallotRelation(hasIntegerValuation)
        else:
            print('Error')
            sys.exit(1)
        #self.valuationdomain = {'min':Decimal('-1.0'),'med':Decimal('0.0'),'max':Decimal('1.0')}
        self.order = len(self.actions)
        self.gamma = self.gammaSets()
        self.notGamma = self.notGammaSets()


    def constructApprovalBallotRelation(self,hasIntegerValuation=False):
        """
        Renders the votes differences between candidates
        on the basis of an approval ballot.
        """
        actions = set(self.actions)
        voters = self.voters
        sumWeight = Decimal('0.0')
        for v in voters:
            sumWeight += Decimal(str(voters[v]['weight']))
        if hasIntegerValuation:
            Min = -sumWeight
            Max = sumWeight
            Med = Decimal('0')
        else:
            Min = Decimal('-1.0')
            Max = Decimal('1.0')
            Med = Decimal('0.0')
        self.valuationdomain = {'min': Min, 'med': Med, 'max':Max, 'hasIntegerValuation': hasIntegerValuation}
        approvalBallot = self.approvalBallot
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Med
        for v in approvalBallot:
            voted = set(approvalBallot[v])
            non_voted = actions - voted
            for x in voted:
                for y in non_voted:
                    relation[x][y] += Decimal(str(voters[v]['weight']))
                    relation[y][x] += Decimal(str(-voters[v]['weight']))
        for x in actions:
            for y in actions:
                if x == y:
                    relation[x][y] = Med
                else:
                    if not hasIntegerValuation and Max != Decimal('0'):
                        relation[x][y] /= Max

        return relation

    def constructMajorityMarginsRelation(self,hasIntegerValuation=True):
        """
        Renders the marginal majority between candidates
        on the basis of an approval ballot.
        """
        actions = set(self.actions)
        voters = self.voters
        sumWeight = Decimal('0.0')
        for v in voters:
            sumWeight += Decimal(str(voters[v]['weight']))
        if hasIntegerValuation:
            Min = -sumWeight
            Max = sumWeight
            Med = Decimal('0')
        else:
            Min = Decimal('-1.0')
            Max = Decimal('1.0')
            Med = Decimal('0.0')
        self.valuationdomain = {'min': Min, 'med': Med, 'max':Max, 'hasIntegerValuation': hasIntegerValuation}
        approvalBallot = self.approvalBallot
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                relation[x][y] = Med
        for v in approvalBallot:
            voted = set(approvalBallot[v])
            non_voted = actions - voted
            for x in voted:
                for y in voted:
                    relation[x][y] += voters[v]['weight']
                for y in non_voted:
                    relation[x][y] += voters[v]['weight']
            for x in non_voted:
                for y in voted:
                    relation[x][y] += -voters[v]['weight']
                for y in non_voted:
                    relation[x][y] += voters[v]['weight']
        for x in actions:
            for y in actions:
                if x == y:
                    relation[x][y] = Med
                else:
                    if not hasIntegerValuation and Max != Decimal('0'):
                        relation[x][y] /= Max
        return relation

    def showMajorityMargins(self,**args):
        """
        Wrapper for the
        Digraph.showRelationTable(Sorted=True, IntegerValues=False,
        actionsSubset=None, relation=None, ndigits=2,
        ReflexiveTerms=True)

        See the :py:meth:`digraphs.Digraph.showRelationTable` description.
        """
        Digraph.showRelationTable(self,**args)
        
    def computeCondorcetWinner(self):
        """
        compute the Condorcet winner(s)
        renders always a, potentially empty, list
        """
        Med = self.valuationdomain['med']
        relation = self.relation
        candidatesList = [x for x in self.actions]
        condorcetWinners = []
        for x in candidatesList:
            Winner = True
            for y in candidatesList:
                if x != y and relation[x][y] <= Med:
                    Winner = False
            if Winner:
                condorcetWinners.append(x)
        return condorcetWinners


    def constructBallotRelation(self,hasIntegerValuation):
        """
        Renders the marginal majority between candidates
        on the basis of a complete ballot.
        """
        actions = self.actions
        voters = self.voters
        ballot = self.ballot
        sumWeight = Decimal('0.0')
        for v in voters:
            sumWeight += Decimal(str(voters[v]['weight']))
        if hasIntegerValuation:
            Min = -sumWeight
            Max = sumWeight
            Med = Decimal('0')
        else:
            Min = Decimal('-1.0')
            Max = Decimal('1.0')
            Med = Decimal('0.0')
        self.valuationdomain = {'min': Min, 'med': Med, 'max':Max, 'hasIntegerValuation': hasIntegerValuation}
        relation = {}
        for x in actions:
            relation[x] = {}
            for y in actions:
                n = len(voters)
                counter = Decimal('0')
                for v in voters:
                    counter += Decimal(str(ballot[v][x][y]))*Decimal(str(voters[v]['weight']))
                if hasIntegerValuation:
                    relation[x][y] = counter
                elif sumWeight != Decimal('0.0'):
                    relation[x][y] = counter/sumWeight
                else:
                    relation[x][y] = Med
        for x in actions:
            relation[x][x] = Med
        return relation

    def computeCopelandRanking(self,Debug=False):
        """
        Renders a ranking of the actions following Copeland's rule.
        Score(x_i) = Sum_j{ [[x_i > x_j]] - [[x_j > x_i]]}, where
        [[x > y]] = 1 if x>y is true, otherwise 0.

        The alternatives are ranked in decreasing order of their Scores.

        In case of a tie, we use a lexicographic rule applied to the identifiers.
        """
        from collections import OrderedDict
        from operator import itemgetter
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        scores = OrderedDict()
        for x in actions:
            scores[x] = 0
        for x in actions:
            for y in actions:
                if relation[x][y] > Med:
                    scores[x] += 1
                if relation[y][x] > Med:
                    scores[x] -= 1
        scoresRanking = [(x,scores[x]) for x in scores]
        scoresRanking = sorted(scoresRanking,key = itemgetter(1),reverse=True)
        ranking = [x[0] for x in scoresRanking]
        if Debug:
            print(actions)
            print(scores)
            print(scoresRanking)
            print(ranking)
        return ranking

    def computeNetFlowsRanking(self,Debug=False):
        """
        Renders a ranking of the actions following the Net Flows rule.
        Score(x_i) = Sum_j{M(x_i,x_j)} for i,j = 1..n

        The alternatives are ranked in decreasing order of their Scores.

        In case of a tie, we use a lexicographic rule applied to the identifiers.
        """
        from collections import OrderedDict
        from operator import itemgetter
        Med = self.valuationdomain['med']
        actions = [x for x in self.actions]
        relation = self.relation
        scores = OrderedDict()
        for x in actions:
            scores[x] = 0
        for x in actions:
            for y in actions:
                scores[x] += relation[x][y]
        scoresRanking = [(x,scores[x]) for x in scores]
        scoresRanking = sorted(scoresRanking,key = itemgetter(1),reverse=True)
        ranking = [x[0] for x in scoresRanking]
        if Debug:
            print(actions)
            print(scores)
            print(scoresRanking)
            print(ranking)
        return ranking

    def computeKohlerRanking(self,linearOrdered=True,Debug=False):
        """
        Renders a ranking of the actions following Kohler's rule.
        """
        Max = self.valuationdomain['max']
        actionsList = [x for x in self.actions]
        relation = self.relation
        rank = {}
        k = 1
        while actionsList != []:
            maximin = []
            for x in actionsList:
                xmin = Max
                for y in actionsList:
                    if x != y:
                        if relation[x][y] < xmin:
                            xmin = relation[x][y]
                if Debug:
                    print('x, xmin', x, xmin)
                maximin.append((xmin,x))
            maximin.sort()
            if Debug:
                print(maximin, maximin[-1][1])
            rank[maximin[-1][1]] = {'rank':k,'majorityMargin':maximin[-1][0]}
            actionsList.remove(maximin[-1][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        if Debug:
            print(rank)
        return rank

    def computeArrowRaynaudRanking(self,linearOrdered=True,Debug=False):
        """
        Renders a ranking of the actions following Arrow&Raynaud's rule.
        """
        Min = self.valuationdomain['min']
        actionsList = [x for x in self.actions]
        n = len(actionsList)
        relation = self.relation
        rank = {}
        k = 1
        while actionsList != []:
            minimax = []
            for x in actionsList:
                xmax = Min
                for y in actionsList:
                    if x != y:
                        if relation[x][y] > xmax:
                            xmax = relation[x][y]
                if Debug:
                    print('x, xmax', x, xmax)
                minimax.append((xmax,x))
            minimax.sort()
            if Debug:
                print(minimax, minimax[0][1])
            rank[minimax[0][1]] = {'rank':n-k+1,'majorityMargin':minimax[0][0]}
            actionsList.remove(minimax[0][1])
            k += 1
            if Debug:
                print('actionsList', actionsList)
        if Debug:
            print(rank)
        return rank

#----------test voting Digraph class ----------------
if __name__ == "__main__":
    import sys,array

    print('****************************************************')
    print('* Python voting digraphs module                    *')
    print('* $Revision: 2484 $                                   *')
    print('* Copyright (C) 2006-2007 University of Luxembourg *')
    print('* The module comes with ABSOLUTELY NO WARRANTY     *')
    print('* to the extent permitted by the applicable law.   *')
    print('* This is free software, and you are welcome to    *')
    print('* redistribute it if it remains free software.     *')
    print('****************************************************')

    print('*-------- Testing classes and methods -------')

    ## v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    ## v.save('testprofile')
    ## v.showAll()
    ## c = CondorcetDigraph(v)
    ## c.save('testcondorcet')
    ## c.showRelationTable()
    ## kr = c.computeKohlerRanking(Debug=False)
    ## kohlerRanking = [(kr[x]['rank'],x) for x in kr]
    ## kohlerRanking.sort()
    ## for x in kohlerRanking:
    ##     print '%s: %d (%.2f)' % (x[1], x[0], kr[x[1]]['majorityMargin'])
    ## aar = c.computeArrowRaynaudRanking(Debug=True)
    ## arrowRaynaudRanking = [(aar[x]['rank'],x) for x in aar]
    ## arrowRaynaudRanking.sort()
    ## for x in arrowRaynaudRanking:
    ##     print '%s: %d (%.2f)' % (x[1], x[0], aar[x[1]]['majorityMargin'])

    lvp = RandomLinearVotingProfile(numberOfCandidates=5,
                              numberOfVoters=9,
                              votersWeights=[1,2,3,4,3,2,1,3,2],seed=1)
##    ## lvp = LinearVotingProfile('templinearprofile')
    lvp.save()
    lvp1 = LinearVotingProfile('templinearprofile')
##    lvp1 = LinearVotingProfile('example1')
    lvp1.computeBallot()
    ## for x in lvp.voters:
    ##    print x, lvp.linearBallot[x]
    lvp1.showLinearBallots(IntegerWeights=True)
    lvp1.showVoterBallot('v1')
##    print(lvp.computeRankAnalysis())
    lvp1.computeInstantRunoffWinner()
    lvp1.showRankAnalysisTable(Debug=False)
    lvp1.showBordaRanking()
    lvp1.computeBordaWinners()
    lvp1.save2PerfTab('votingPerfTab')
    t = PerformanceTableau('votingPerfTab')
    t.showHTMLPerformanceHeatmap(Correlations=True,ndigits=0)
    c = CondorcetDigraph(lvp1)
    #c.recodeValuation()
    c.showRelationTable()
    print(c.computeCopelandRanking(Debug=True))
    print(c.computeNetFlowsRanking(Debug=True))
    
##    from linearOrders import NetFlowsOrder
##    nf = NetFlowsOrder(c,Debug=True)
##    from outrankingDigraphs import *
##    t1 = RandomCBPerformanceTableau(numberOfActions=5)
##    g1 = BipolarOutrankingDigraph(t1)
##    g1.showRelationTable()
##    nf1 = NetFlowsOrder(g1,Debug=True)
    
    
##    lvp1.showHTMLVotingHeatmap()
##    
##    print(lvp.computeBordaWinners())
##    print(lvp.computeUninominalVotes(lvp.candidates,lvp.linearBallot))
##    print(lvp.computeInstantRunoffWinner(Comments=True))
##    print(lvp.computeSimpleMajorityWinner(Comments=True))
##
##    c = CondorcetDigraph(lvp)
##    c.exportGraphViz()
##    print('Chordless circuits = ', c.computeChordlessCircuits())
##    print('Condorcet Winner = ', c.computeCondorcetWinner())
##    m = len(lvp.voters)
##    c.recodeValuation(-m,m)
##    c.showRelationTable()

##    av = ApprovalVotingProfile('approvalInvitation')
##    av.save2PerfTab()
##    t = PerformanceTableau('votingPerfTab')
##    t.showHTMLPerformanceHeatmap(Correlations=True,ndigits=0)
    
    

    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. September 2008               *')
    print('* $Revision: 2484 $                   *')
    print('*************************************')

#############################
# Log record for changes:
# $Log: votingDigraphs.py,v $#
#############################
