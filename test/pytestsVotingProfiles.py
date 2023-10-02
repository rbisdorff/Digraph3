#######################
# R. Bisdorff
# pytest functions for the votingProfiles module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from digraphs import *
from votingProfiles import *

def testVotingProfiles():
    print('*==>> testing voting profiles ----*')
    vt = VotingProfile('../testvotingprofile')
    print(vt.candidates)
    print(vt.voters)
    print(vt.ballot)
    vt.showAll()
    vt.save('tempVprofile')
    g = MajorityMarginsDigraph(vt,IntegerValuation=False)
    g.showRelationTable()
    g.showStatistics()
    vt1 = VotingProfile('tempVprofile')
    print(vt1.candidates)
    print(vt1.voters)
    print(vt1.ballot)
    g1 = MajorityMarginsDigraph(vt1,IntegerValuation=True)
    g1.showRelationTable()
    g1.showStatistics()
    g2 = MajorityMarginsDigraph('tempVprofile')
    g2.showStatistics()        
    g = MajorityMarginsDigraph(vt)
    g.showRelationTable()

def testRandomApprovalVotingProfiles():
    print('*==>> testing approval voting profiles ----*')
    v = RandomBipolarApprovalVotingProfile(numberOfVoters=50,
                                           numberOfCandidates=10,
                                           approvalProbability=0.25,
                                           disapprovalProbability=0.25,
                                           seed=None,DivisivePolitics=True,
                                           WithPolls=True,Debug=True)
    print(v)
    v.showLinearBallots()
    v.showApprovalResults()
    v.showDisapprovalResults()
    v.showNetApprovalScores()
    v.showHTMLVotingHeatmap(rankingRule='NetFlows',Transposed=True)
    m = MajorityMarginsDigraph(v)
    print(m)
    m.showRelationTable()
    m.showBestChoiceRecommendation()
    m.showRelationMap()

def testRandomVotingProfiles():
    print('*==>> testing random voting profiles ----*')
    v = RandomVotingProfile()
    c = MajorityMarginsDigraph(v)
    c.showAll()
    v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    c = MajorityMarginsDigraph(v)   
    c.showRelationTable()

def testKohlerRanking():
    print("*==>> testing Kohler's Ranking Rule ----*")
    v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    v.save('testprofile')
    v.showAll()
    c = MajorityMarginsDigraph(v)
    c.save('testcondorcet')
    c.showRelationTable()
    print(c.computeKohlerRanking())

def testArrowRaynaudRanking():
    print("*==>> testing Arrow&Raynaud's Ranking Rule ----*")
    v = RandomVotingProfile(hasRandomWeights=True,maxWeight=4,Debug=True)
    v.save('testprofile')
    v.showAll()
    c = MajorityMarginsDigraph(v)
    c.save('testcondorcet')
    c.showRelationTable()
    print(c.computeArrowRaynaudRanking())

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
    c = MajorityMarginsDigraph(lvp)
    c.exportGraphViz()
    print(c.computeChordlessCircuits())
    lvp.save2PerfTab()
    t = PerformanceTableau('votingPerfTab')
    from outrankingDigraphs import BipolarOutrankingDigraph
    g = BipolarOutrankingDigraph(t)
    lvp.showHTMLVotingHeatmap()
    print(c.computeCopelandRanking())
    
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
    c = MajorityMarginsDigraph(lvp)
    #c.recodeValuation()
    c.showRelationTable()
    print(c.computeCopelandRanking())
    print(c.computeNetFlowsRanking())
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

def testPreorderVotingProfile():
    print('*==> test Preorder Voting profiles ---*')
    from votingProfiles import RandomPrerankedVotingProfile
    pv = RandomPrerankedVotingProfile(numberOfVoters=5,
                                     numberOfCandidates=8,
                                     votersIdPrefix='a',
                                     candidatesIdPrefix='b',
                                     votersWeights=[1,2,3,4,5],
                                     seed=1)
    print(pv)
    pv.showPrerankedBallots()
    pv.save()
    

