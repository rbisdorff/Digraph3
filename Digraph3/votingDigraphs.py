#!/usr/bin/env python3
# Python 3 implementation of voting digraphs
# Refactored from revision 1.549 of the digraphs module
# Current revision $Revision$
# Copyright (C) 2011  Raymond Bisdorff
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

#--------- Decimal precision --------------
from decimal import Decimal

#---------- voting profiles

class VotingProfile(object):
    """
    A general class for storing voting profiles.

    General structure::

	candidates = {'a': ...,'b': ...,'c': ...,  ... }
	voters = {
        '1':{'weight':1.0},
        '2':{'weight':1.0},
        ...,
        }
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
    def __init__(self,fileVotingProfile=None):

        if fileVotingProfile != None:
            fileName = fileVotingProfile+'.py'
            argDict = {}
            exec(compile(open(fileName).read(), fileName, 'exec'),argDict)
            self.name = str(fileVotingProfile)
            self.candidates = argDict['candidates']
            self.voters = argDict['voters']
            self.ballot = argDict['ballot']
        else:
            randv = RandomVotingProfile()
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
        fo.write('candidates = {\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + candidateName + '\'},\n')
            fo.write('\'%s\': {\'name\': \'%s\'},\n' % (x,candidateName) )
        fo.write('}\n')
        fo.write('voters = {\n')
        for v in voters:
            fo.write('\'' +str(v)+'\': {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'},\n')
        fo.write('}\n')
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

        candidates = {'a': ,'b':  ,'c', ..., ...}
        voters = {'1':{'weight':1.0},'2':{'weight':1.0}, ...}
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
    def __init__(self,fileVotingProfile=None,numberOfCandidates=5,numberOfVoters=9):
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
            randv = RandomLinearVotingProfile(numberOfCandidates=numberOfCandidates,
                                              numberOfVoters=numberOfVoters)
            self.name = 'randLinearVotingProfile'
            self.candidates = randv.candidates
            self.voters = randv.voters
            self.linearBallot = randv.linearBallot
            self.ballot = randv.ballot

    def computeBallot(self):
        """
        Computes a complete ballot from the linear Ballot.
        """
        candidates = set(self.candidates)
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
        fo.write('candidates = {\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + str(x)+ '\'},\n')
            fo.write('\'%s\': {\'name\': \'%s\'},\n' % (x,candidateName) )
        fo.write('}\n')
        fo.write('voters = {\n')
        for v in voters:
            fo.write('\'' +str(v)+'\': {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'},\n')
        fo.write('}\n')
        fo.write('linearBallot = {\n')
        for v in linearBallot:
            fo.write('\'' +str(v)+'\': [\n')
            for x in linearBallot[v]:
                fo.write('\'' + str(x) + '\'' +',\n')
            fo.write('],\n')
        fo.write( '}\n')
        fo.close()

    def showLinearBallots(self):
        """
        show the linear ballots
        """
        print('voters(weight)\t candidates rankings')
        for v in self.voters:
            print('%s(%s): \t %s' % (str(v),str(self.voters[v]['weight']),str(self.linearBallot[v])))


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
                x = self.linearBallot[v][i]
                #ranks[x][i] += 1
                ranks[x][i] += self.voters[v]['weight']
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
        print('*----  Rank analysis tableau -----*')
        bordaScores = self.computeBordaScores() 
        candidatesList = [(bordaScores[x],x) for x in self.candidates]
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

        print(' ranks | ', end=' ')
        for x in rankIndex:
            print( str(x) + '   ', end=' ')
        print('| Borda score')
        print('-------|-----------------------------------------')
        for c in candidatesList:
            print('  \''+str(c[1])+'\' |', end=' ')
            for i in rankIndex:
                formatString = '%% .%df ' % ndigits
                print(formatString % (ranks[c[1]][(i-1)]), end='  ')
            formatString = ' |  %% .%df' % ndigits
            print(formatString % (bordaScores[c[1]]) )      


    def computeBordaScores(self):
        """
        compute Borda scores from the rank analysis
        """
        ranks = self.computeRankAnalysis()
        BordaScores={}
        candidatesList = [x for x in self.candidates]
        n = len(candidatesList)
        for x in candidatesList:
            BordaScores[x] = 0
            for i in range(n):
                BordaScores[x] += (i+1)*ranks[x][i]
        return BordaScores

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
            if BordaMinimum > BordaScores[x]:
                BordaMinimum = BordaScores[x]
        winners = [x for x in BordaScores if BordaScores[x] == BordaMinimum]
        return winners

    def computeInstantRunoffWinner(self,Comments=False):
        """
        compute the instant runoff winner from a linear voting ballot
        """
        import copy
        from decimal import Decimal
        voters = [x for x in self.voters]
        totalWeight = Decimal("0.0")
        for v in voters:
            totalWeight += Decimal('%.3f' % (self.voters[v]['weight']) )
        halfWeight = totalWeight/Decimal("2.0")
        if Comments:
            print('Total number of votes = ', totalWeight)
            print('Half of the Votes = ', halfWeight)
        candidatesList = [x for x in self.candidates]
        remainingCandidates = copy.copy(candidatesList)
        remainingLinearBallot = copy.deepcopy(self.linearBallot)
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
                            remainingLinearBallot[v].remove(x)
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

        candidates = {'a': {'name': ...},
                      'b': {'name': ...},
                      ..., ...}
        voters = {'v1':{'weight':1.0},'v2':{'weight':1.0}, ...}
        ## each specifies the subset of candidates he approves on
        approvalBallot = {
            'v1' : ['b'],
            'v2' : ['a','b'],
            ...
            }

    """
    def __init__(self,fileVotingProfile=None):
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
            self.ballot = self.computeBallot()
        else:
            randv = RandomApprovalVotingProfile()
            self.name = 'randApprovalVotingProfile'
            self.candidates = randv.candidates
            self.voters = randv.voters
            self.ballot = randv.ballot

    def showResults(self):
        """
        Renders the votes obtained by each candidates.
        """
        print('Voting results')
        candidates = [x for x in self.candidates]
        candidates.sort()
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

    def computeBallot(self,approvalEquivalence=False,disapprovalEquivalence=False):
        """
        Computes a complete ballot from the approval Ballot.

        Parameters:
            approvalEquivalence=False, disapprovalEquivalence=False.
        """
        candidates = set(self.candidates)
        AVballot = self.approvalBallot
        ballot = {}
        for v in AVballot:
            ballot[v] = {}
            for x in candidates:
                ballot[v][x] = {}
                for y in candidates:
                    ballot[v][x][y] = Decimal("0.0")
            voted = set(AVballot[v])
            non_voted = candidates - voted
            if approvalEquivalence:
                for x in voted:
                    for y in voted:
                        ballot[v][x][y] = Decimal("1.0")
            if disapprovalEquivalence:
                for x in non_voted:
                    for y in non_voted:
                        ballot[v][x][y] = Decimal("1.0")
            for x in voted:
                for y in non_voted:
                    ballot[v][x][y] = Decimal("1.0")
                    ballot[v][y][x] = Decimal("-1.0")
            for x in candidates:
                ballot[v][x][x] = Decimal("-1.0")
        self.ballot = ballot
        return ballot

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
        fo.write('candidates = {\n')
        for x in candidates:
            try:
                candidateName = candidates[x]['name']
            except:
                candidateName = x
            #fo.write('\'' + str(x) + '\': {\'name\': \'' + str(x)+ '\'},\n')
            fo.write('\'%s\': {\'name\': \'%s\'},\n' % (x,candidateName) )
        fo.write('}\n')
        fo.write('voters = {\n')
        for v in voters:
            fo.write('\'' +str(v)+'\': {\n')
            fo.write('\'weight\':'+str(voters[v]['weight'])+'},\n')
        fo.write('}\n')
        fo.write('approvalBallot = {\n')
        for v in approvalBallot:
            fo.write('\'' +str(v)+'\': [\n')
            for x in approvalBallot[v]:
                fo.write('\'' + str(x) + '\'' +',\n')
            fo.write('],\n')
        fo.write( '}\n')
        fo.close()


class RandomApprovalVotingProfile(ApprovalVotingProfile):
    """
    A specialized class for approval voting profiles.
    """
    def __init__(self,numberOfVoters=9,numberOfCandidates=5,minSizeOfBallot=1,maxSizeOfBallot=2):
        """
        Random profile creation parameters:
            | numberOfVoters=9, numberOfCandidates=5,
            | minSizeOfBallot=1, maxSizeOfBallot=2.
        """
        import random
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = {}
        for v in votersList:
            voterID = 'v%d' % v
            voters[voterID] = {'weight':1.0}
        candidatesList = [x for x in range(1,numberOfCandidates + 1)]
        candidates = {}
        for c in candidatesList:
            candidateID = 'a%d' % c
            candidates[candidateID] = {'name': candidateID}
        self.name = str('randAVProfile')
        self.candidates = candidates
        self.voters = voters
        self.approvalBallot = self.generateRandomApprovalBallot(minSizeOfBallot,maxSizeOfBallot)
        self.ballot = self.computeBallot()

    def generateRandomApprovalBallot(self,minSizeOfBallot,maxSizeOfBallot):
        """
        Renders a randomly generated approval ballot.
        """
        import random,copy
        random.seed()
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

class RandomLinearVotingProfile(LinearVotingProfile):
    """
    A specialized class for random linwear voting profiles.
    """
    def __init__(self,seed=None,numberOfVoters=9,numberOfCandidates=5):
        """
        Random profile creation parameters:
            | numberOfVoters=9, numberOfCandidates=5,
        """
        import random
        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = {}
        for v in votersList:
            voterID = 'v%d' % v
            voters[voterID] = {'weight':1.0}
        candidatesList = [x for x in range(1,numberOfCandidates + 1)]
        candidates = {}
        for c in candidatesList:
            candidateID = 'a%d' % c
            candidates[candidateID] = {'name': candidateID}
        self.name = str('randLinearProfile')
        self.candidates = candidates
        self.voters = voters
        self.linearBallot = self.generateRandomLinearBallot(seed)
        #print self.linearBallot
        self.ballot = self.computeBallot()

    def generateRandomLinearBallot(self,seed):
        """
        Renders a randomly generated linear ballot.
        """
        import random,copy
        if seed == None:
            random.seed()
        else:
            random.seed(seed)
        linearBallot = {}
        voters = self.voters
        candidateList = [x for x in self.candidates]
        #print candidateList
        for v in voters:
            random.shuffle(candidateList)
            #print candidateList
            linearBallot[v] = copy.copy(candidateList)
        return linearBallot

class RandomVotingProfile(VotingProfile):
    """
    A subclass for generating random voting profiles.
    """
    def __init__(self,numberOfVoters=9,numberOfCandidates=5,hasRandomWeights=False,maxWeight=10,seed=None,Debug=False):
        """
        Random profile creation parameters:

            | numberOfVoters=9,
            | numberOfCandidates=5

        """
        import random
        if seed != None:
            random.seed(seed)

        votersList = [x for x in range(1,numberOfVoters + 1)]
        voters = {}
        for v in votersList:
            voterID = 'v%d' % v
            if hasRandomWeights:
                voters[voterID] = {'weight':random.randint(1,maxWeight)}
            else:
                voters[voterID] = {'weight':1}
        candidatesList = [x for x in range(1,numberOfCandidates + 1)]
        candidates = {}
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
    def __init__(self,argVotingProfile=None,approvalVoting=False,coalition=None,majorityMargins=False,hasIntegerValuation=False):
        import copy
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
        self.actions = copy.deepcopy(votingProfile.candidates)
        if coalition == None:
            voters = copy.deepcopy(votingProfile.voters)
        else:
            voters = {}
            for g in coalition:
                voters[g] = votingProfile.voters[g]
        self.voters = voters
        if isinstance(votingProfile, (VotingProfile)):
            self.ballot = copy.deepcopy(votingProfile.ballot)
            self.relation = self.constructBallotRelation(hasIntegerValuation)
        elif isinstance(votingProfile, (ApprovalVotingProfile)):
            self.approvalBallot = copy.deepcopy(votingProfile.approvalBallot)
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

    def computeCondorcetWinner(self):
        """
        compute the Condorcet winner(s)
        renders always a, potentially empty, list
        """
        Med = self.valuationdomain['med']
        relation = self.relation
        candidatesList = [x for x in self.actions]
        CondorcetWinner = []
        for x in candidatesList:
            winner = True
            for y in candidatesList:
                if x != y and relation[x][y] <= Med:
                    winner = False
            if winner:
                CondorcetWinner.append(x)
        return CondorcetWinner


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
    print('* $Revision$                                   *')
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

    lvp = LinearVotingProfile(numberOfCandidates=5,numberOfVoters=9)
    ## lvp = LinearVotingProfile('templinearprofile')
    lvp.save()
    ## for x in lvp.voters:
    ##    print x, lvp.linearBallot[x]
    lvp.showLinearBallots()
    print(lvp.computeRankAnalysis())
    lvp.showRankAnalysisTable(Debug=True)
    print(lvp.computeBordaScores())
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

    print('*------------------*')
    print('If you see this line all tests were passed successfully :-)')
    print('Enjoy !')

    print('*************************************')
    print('* R.B. September 2008               *')
    print('* $Revision$                   *')
    print('*************************************')

#############################
# Log record for changes:
# $Log: votingDigraphs.py,v $#
#############################
