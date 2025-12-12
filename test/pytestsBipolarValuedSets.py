#######################
# R. Bisdorff
# pytest functions for the bachetNumbers module
# ..$python3 -m pip install pytest  # installing the pytest package
########################

from bipolarValuedSets import *
    
def testBpvSet():
    print('==>> Testing bipolar valued sets implementation')
    X = RandomBpvSet(numberOfElements=3,elementNamePrefix='s',
                      undeterminateness=0.2,
                      valuationRange=(-10,10),
                      seed=1000,
                      Debug=False)
    
    #X.showMembershipCharacteristics(Normalized=False)
    X.showMembershipCharacteristics(Normalized=True,ndigits=2)
    Y = RandomBpvSet(numberOfElements=5,elementNamePrefix='s',
                      undeterminateness=0.2,
                      valuationRange=(-10,10),
                      seed=2000,
                      Debug=False)
    
    #Y.showMembershipCharacteristics(Normalized=False)
    Y.showMembershipCharacteristics(Normalized=True,ndigits=2)
    U = X&Y
    print('set conjunction')
    U.showMembershipCharacteristics()
    R = X|Y
    print('set union disjunction')
    R.showMembershipCharacteristics()
    S = X - Y
    print('set difference')
    S.showMembershipCharacteristics()
    T = X^Y
    print('set symmetric difference')
    T.showMembershipCharacteristics()
    
    
    


    
