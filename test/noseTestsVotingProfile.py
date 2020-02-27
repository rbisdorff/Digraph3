#######################
# R. Bisdorff 
# digraphs.py module tests for nose
#
# ..$ easyinstall nose   # installing the nose test environment
# ..$ nosetests -vs noseTestsVotingDigraph.py
# # Current $Revision$
########################

from digraphs import *
from votingProfiles import *

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
    vt.save('testAP')
    vt = ApprovalVotingProfile('testAP')
    print('Candidates: ', vt.candidates)
    print('Voters: ',vt.voters)
    print('Approval Ballot: ', vt.approvalBallot)
    vt.showResults()
    vt.showAll()
    g = CondorcetDigraph(vt,approvalVoting=True,hasIntegerValuation=True)
    g.showRelationTable()
    g.showStatistics()
    print(g.condorcetWinners())
    print(g.weakCondorcetWinners())
    print(g.condorcetLoosers())
    print(g.weakCondorcetLoosers())
    g.showPreKernels()
    g.showRubyChoice()
    g.showBadChoices()
    vt.computeBallot()
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
    c.computeKemenyRanking(Debug=True)
    print(c.computeKemenyRanking(isProbabilistic=True, seed=1,sampleSize=500, Debug=True))
    c.computeSlaterOrder(Debug=True)
    print(c.computeSlaterOrder(isProbabilistic=True, seed=1,sampleSize=500, Debug=True))

def testLinearVotingBallots():
    print("*==>> testing linear voting profiles ----*")
    lvp = RandomLinearVotingProfile(numberOfVoters=100,
                                    numberOfCandidates=10,
                                    WithPolls=True,
                                    partyRepartition=0.6,
                                    other=0.1,
                                    seed=None)
    lvp.save()
    lvp = LinearVotingProfile('templinearprofile')
    lvp.showLinearBallots()
    print(lvp.computeRankAnalysis())
    lvp.showRankAnalysisTable(Debug=True)
    print(lvp.computeBordaScores())
    print(lvp.computeBordaWinners())
    c = CondorcetDigraph(lvp)
    c.exportGraphViz()
    print(c.computeChordlessCircuits())
    lvp.save2PerfTab()
    t = PerformanceTableau('votingPerfTab')
    from outrankingDigraphs import BipolarOutrankingDigraph
    g = BipolarOutrankingDigraph(t)
    lvp.showHTMLVotingHeatmap()
    c.computeCopelandRanking(Debug=True)
    
def testInstantRunoffVoting():
    print('*==> test instant runoff voting ---*')
    lvp = RandomLinearVotingProfile(votersWeights=[5,3,2])
    lvp.save()
    lvp.showLinearBallots()
    print(lvp.computeRankAnalysis())
    print(lvp.computeBordaScores())
    print(lvp.computeBordaWinners())
    print(lvp.computeUninominalVotes(lvp.candidates,lvp.linearBallot))
    print(lvp.computeInstantRunoffWinner(Comments=True))

def testWeakRankings():
    print('*==> test weak Copeland and NetFlows rankings ---*')
    lvp = RandomLinearVotingProfile(numberOfCandidates=20,
                              numberOfVoters=1000,
                                    WithPolls=True,
                                    partyRepartition=0.5,
                                    other=0.1,
                                    seed=None)
    lvp.showRandomPolls()
    c = CondorcetDigraph(lvp)
    #c.recodeValuation()
    c.showRelationTable()
    print(c.computeCopelandRanking(Debug=False))
    print(c.computeNetFlowsRanking(Debug=False))
    print(c.computeTransitivityDegree())
    c.computeChordlessCircuits()
    c.showChordlessCircuits()
    c.recodeValuation()
    from transitiveDigraphs import WeakCopelandOrder, WeakNetFlowsOrder
    wc = WeakCopelandOrder(c)
    print('Weak Copeland ranking')
    wc.showRankingByChoosing()
    corr = c.computeRankingCorrelation(wc.copelandRanking)
    wc.showCorrelation(corr)
    wn = WeakNetFlowsOrder(c)
    print('Weak NetFloes ranking')
    wn.showRankingByChoosing()
    corr = c.computeRankingCorrelation(wc.copelandRanking)
    wn.showCorrelation(corr)
