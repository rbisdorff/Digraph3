#######################
# R. Bisdorff
# pytest functions for the pairings module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from pairings import *
from random import randint
from votingProfiles import RandomLinearVotingProfile

def testFairInterGroupPairing():
    k = 6
    lvA = RandomLinearVotingProfile(numberOfVoters=k,numberOfCandidates=k,
                                      votersIdPrefix='a',
                                      candidatesIdPrefix='b',seed=1)
    lvB = RandomLinearVotingProfile(numberOfVoters=k,numberOfCandidates=k,
                                      votersIdPrefix='b',
                                        candidatesIdPrefix='a',seed=2)
    lvA.showLinearBallots()
    lvB.showLinearBallots()
    fp = FairestInterGroupPairing(lvA,lvB,Debug=False)
    fp.showFairestPairing(rank=1,WithIndividualCorrelations=True)
    fp.isStableMatching(fp.pairings[0][0],Comments=True,Debug=False)
    g1 = fp.computeGaleShapleyMatching()
    fp.isStableMatching(g1,Comments=True,Debug=False)
    fp.showMatchingFairness(g1,WithIndividualCorrelations=True)
    g2 = fp.computeGaleShapleyMatching(Reverse=True)
    fp.isStableMatching(g2,Comments=True,Debug=False)
    fp.showMatchingFairness(g2,WithIndividualCorrelations=True)
    fp.exportPairingGraphViz('testbipartiteGraph')

def testGaleShapleyMatchings():
    seed1 = randint(0,99)
    seed2 = randint(100,199)
    k = 7
    lvA = RandomLinearVotingProfile(numberOfVoters=k,numberOfCandidates=k,
                                      votersIdPrefix='a',
                                      candidatesIdPrefix='b',seed=seed1)
    lvB = RandomLinearVotingProfile(numberOfVoters=k,numberOfCandidates=k,
                                      votersIdPrefix='b',
                                        candidatesIdPrefix='a',seed=seed2)
    lvA.showLinearBallots()
    lvB.showLinearBallots()
    gs = FairestGaleShapleyMatching(lvA,lvB,Comments=True)
    gs.exportGraphViz('galeShapley')

def testFairnessEnhancedAPMatching():    
    from votingProfiles import RandomLinearVotingProfile,RandomBipolarApprovalVotingProfile
    from random import randint
    seed1 = randint(0,99)
    seed2 = randint(100,199)
    order = 20
    apA = RandomBipolarApprovalVotingProfile(numberOfVoters=order,
                                    numberOfCandidates=order,
                                    votersIdPrefix='a',
                                    candidatesIdPrefix='b',
                                    approvalProbability=0.3,
                                    disapprovalProbability=0.3,
                                    seed=seed1)
    apB = RandomBipolarApprovalVotingProfile(numberOfVoters=order,
                                    numberOfCandidates=order,
                                    votersIdPrefix='b',
                                    approvalProbability=0.3,
                                    disapprovalProbability=0.3,
                                    candidatesIdPrefix='a',seed=seed2)
    print('seeds:', apA.seed,apB.seed)
    em = FairnessEnhancedInterGroupMatching(apA,apB,initialMatching=None,
                                  seed=None,
                                  maxIterations=2*order,
                                  Comments=True,Debug=False)
    em.showMatchingFairness(em.matching)

def testFairnessEnhancedPrerankedMatching():    
    from votingProfiles import RandomLinearVotingProfile,\
         RandomBipolarApprovalVotingProfile,\
         RandomPrerankedVotingProfile
    from random import randint
    seed1 = randint(0,99)
    seed2 = randint(100,199)
    order = 20
    apA = RandomPrerankedVotingProfile(numberOfVoters=order,
                                    numberOfCandidates=order,
                                    votersIdPrefix='a',
                                    candidatesIdPrefix='b',
                                    lengthProbability=0.3,
                                    seed=seed1)
    apB = RandomPrerankedVotingProfile(numberOfVoters=order,
                                    numberOfCandidates=order,
                                    votersIdPrefix='b',
                                    candidatesIdPrefix='a',
                                    lengthProbability=0.3,
                                    seed=seed2)
    print('seeds:', apA.seed,apB.seed)
    em = FairnessEnhancedInterGroupMatching(apA,apB,initialMatching=None,
                                  seed=None,
                                  maxIterations=2*order,
                                  Comments=True,Debug=False)
    em.showMatchingFairness(em.matching)

def testFairnessEnhancedIntraGroupMatching():
    from votingProfiles import RandomBipolarApprovalVotingProfile
    rigvp = RandomBipolarApprovalVotingProfile(numberOfVoters=16,
                                               votersIdPrefix='p',
                                               IntraGroup=True,Debug=False)
    
    print('seed:',rigvp.seed)
    fgm = FairnessEnhancedIntraGroupMatching(intraVp=rigvp,seed=None,
                                             initialMatching=None,
                                             Comments=True,Debug=False)
    fgm = FairnessEnhancedIntraGroupMatching(intraVp=rigvp,seed=None,
                                             initialMatching='bestBachet',
                                             fitnessScores='Bachet',
                                             Comments=True,Debug=False)

def testBestCopelandBachetInterGroupMatching():
    from votingProfiles import RandomBipolarApprovalVotingProfile
    order = 6
    from random import randint
    seed1 = randint(0,99)
    seed2 = randint(100,199)
    vpA = RandomBipolarApprovalVotingProfile(numberOfVoters=order,
                                    numberOfCandidates=order,
                                    votersIdPrefix='a',
                                    candidatesIdPrefix='b',
                                    approvalProbability=0.3,
                                    disapprovalProbability=0.3,
                                    seed=seed1,Debug=False)
    vpA.showBipolarApprovals()
    vpB = RandomBipolarApprovalVotingProfile(numberOfVoters=order,
                                    numberOfCandidates=order,
                                    votersIdPrefix='b',
                                    candidatesIdPrefix='a',
                                    approvalProbability=0.3,
                                    disapprovalProbability=0.3,
                                    seed=seed2,Debug=False)
    vpB.showBipolarApprovals()
    print('seeds:',seed1,seed2)
    cop = BestCopelandInterGroupMatching(vpA,vpB,
                                        Comments=True,Debug=False)
    cop.showMatchingFairness(WithIndividualCorrelations=True)
    bac = BestBachetInterGroupMatching(vpA,vpB,
                                        Comments=True,Debug=False)
    bac.showMatchingFairness(WithIndividualCorrelations=True)
    
def testBestCopelandBachetIntraGroupMatching():
    from votingProfiles import RandomBipolarApprovalVotingProfile
    from random import randint
    seed1 = randint(0,99)    
    vpG = RandomBipolarApprovalVotingProfile(numberOfVoters=12,
                                               votersIdPrefix='p',
                                               IntraGroup=True,
                                             seed=seed1)
    vpG.showBipolarApprovals()
    print('seed:',vpG.seed)
    cop = BestCopelandIntraGroupMatching(vpG,
                                        Comments=True,Debug=False)
    cop.showMatchingFairness(WithIndividualCorrelations=True)
    bac = BestBachetIntraGroupMatching(vpG,
                                        Comments=True,Debug=False)
    bac.showMatchingFairness(WithIndividualCorrelations=True)
