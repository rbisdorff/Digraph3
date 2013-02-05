#######################
# R. Bisdorff 
# digraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsVotingDigraph.py
# # Current $Revision$
########################

from digraphs import *
from votingDigraphs import *

def testVotingProfiles():
    print('*==>> testing voting profiles ----*')
    vt = VotingProfile('testvotingprofile')
    print(vt.candidates)
    print(vt.voters)
    print(vt.ballot)
    vt.showAll()
    vt.save('tempVprofile')
    g = CondorcetDigraph(vt,hasIntegerValuation=False)
    g.showRelationTable()
    g.showStatistics()
    vt1 = VotingProfile('tempVprofile')
    print(vt1.candidates)
    print(vt1.voters)
    print(vt1.ballot)
    g1 = CondorcetDigraph(vt1,hasIntegerValuation=True)
    g1.showRelationTable()
    g1.showStatistics()
    g2 = CondorcetDigraph('tempVprofile',majorityMargins=True)
    g2.showStatistics()        
    g = CondorcetDigraph(vt)
    g.showRelationTable()

def testApprovalVotingProfiles():
    print('*==>> testing approval voting profiles ----*')
    vt = RandomApprovalVotingProfile(minSizeOfBallot=3,maxSizeOfBallot=3)
    print('Candidates: ', vt.candidates)
    print('Voters: ',vt.voters)
    print('Approval Ballot: ', vt.approvalBallot)
    vt.showResults()
    vt.showAll()
    g = CondorcetDigraph(vt,approvalVoting=True,hasIntegerValuation=True)
    g.showRelationTable()
    g.showStatistics()
    g.showPreKernels()
    g.showRubyChoice()
    g.showBadChoices()
    vt.computeBallot(approvalEquivalence=True,disapprovalEquivalence=True)
    vt.showAll()
    g1 = CondorcetDigraph(vt)
    g1.showStatistics()
    g1.showPreKernels()
    g1.showRubyChoice()
    g1.showBadChoices()

def testRandomVotingProfiles():
    print('*==>> testing random voting profiles ----*')
    c = CondorcetDigraph()
    c.showAll()
    v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    c = CondorcetDigraph(v)   
    c.showRelationTable()

def testRandomApprovalVotingProfiles():
    print('*==>> testing random approval voting profiles ----*')
    vt = RandomApprovalVotingProfile(numberOfVoters=10,numberOfCandidates=6,maxSizeOfBallot=1)
    print('Candidates: ', vt.candidates)
    print('Voters: ',vt.voters)
    print('Approval Ballot: ', vt.approvalBallot)
    vt.showResults()
    vt.save('testAVprofile')
    vt1 = ApprovalVotingProfile('testAVprofile')
    vt1.showResults()

def testKohlerRanking():
    print("*==>> testing Kohler's Ranking Rule ----*")
    v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    v.save('testprofile')
    v.showAll()
    c = CondorcetDigraph(v)
    c.save('testcondorcet')
    c.showRelationTable()
    kr = c.computeKohlerRanking(Debug=False)
    kohlerRanking = [(kr[x]['rank'],x) for x in kr]
    kohlerRanking.sort()
    for x in kohlerRanking:
        print('%s: %d (%.2f)' % (x[1], x[0], kr[x[1]]['majorityMargin']))

def testArrowRaynaudRanking():
    print("*==>> testing Arrow&Raynaud's Ranking Rule ----*")
    v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    v.save('testprofile')
    v.showAll()
    c = CondorcetDigraph(v)
    c.save('testcondorcet')
    c.showRelationTable()
    aar = c.computeArrowRaynaudRanking(Debug=True)
    arrowRaynaudRanking = [(aar[x]['rank'],x) for x in aar]
    arrowRaynaudRanking.sort()
    for x in arrowRaynaudRanking:
        print('%s: %d (%.2f)' % (x[1], x[0], aar[x[1]]['majorityMargin']))

def testNonPrudentRankings():
    print("*==>> testing non prudent ranking rules ----*")
    v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    v.save('testprofile')
    v.showAll()
    c = CondorcetDigraph(v)
    c.save('testcondorcet')
    c.showRelationTable()
    c.computeRankedPairsOrder(Debug=True)
    print(c.computeRankedPairsOrder())

    c.computeKemenyOrder(Debug=True)
    print(c.computeKemenyOrder(isProbabilistic=True, seed=1,sampleSize=500, Debug=True))
    c.computeSlaterOrder(Debug=True)
    print(c.computeSlaterOrder(isProbabilistic=True, seed=1,sampleSize=500, Debug=True))

def testLinearVotingBallots():
    print("*==>> testing linear voting profiles ----*")
    lvp = LinearVotingProfile()
    lvp.save()
    lvp = LinearVotingProfile('templinearprofile')
    lvp.showLinearBallots()
    print(lvp.computeRankAnalysis())
    print(lvp.computeBordaScores())
    print(lvp.computeBordaWinners())
    c = CondorcetDigraph(lvp)
    c.exportGraphViz()
    print(c.computeChordlessCircuits())

def testInstantRunoffVoting():
    print('*==> test instant runoff voting ---*')
    lvp = LinearVotingProfile()
    lvp.save()
    lvp.showLinearBallots()
    print(lvp.computeRankAnalysis())
    print(lvp.computeBordaScores())
    print(lvp.computeBordaWinners())
    print(lvp.computeUninominalVotes(lvp.candidates,lvp.linearBallot))
    print(lvp.computeInstantRunoffWinner(Comments=True))
