FLAG = --inplace
PYTHON = python3
NOSETESTS = nosetests3

codg:
		cython -3 -X boundscheck=True cIntegerOutrankingDigraphs.pyx
bodg:
		${PYTHON} csetupODGInteger.py build_ext ${FLAG}
cso:
		cython -3 -X boundscheck=True cIntegerSortingDigraphs.pyx
bso:
		${PYTHON} csetupSOInteger.py build_ext ${FLAG}
cbg:
		cython -3 -X boundscheck=True cBigIntegerOutrankingDigraphs.py
bbg:
		${PYTHON} csetupBGInteger.py build_ext ${FLAG}
call:
		cython -3 -X boundscheck=True cIntegerOutrankingDigraphs.pyx
		cython -3 -X boundscheck=True cIntegerSortingDigraphs.pyx
		cython -3 -X boundscheck=True cBigIntegerOutrankingDigraphs.pyx
inplace:
		${PYTHON} csetupRandPerfTabs.py build_ext ${FLAG}
		${PYTHON} csetupODGInteger.py build_ext ${FLAG}
		${PYTHON} csetupSOInteger.py build_ext ${FLAG}
		${PYTHON} csetupBGInteger.py build_ext ${FLAG}
install:
		sudo ${PYTHON} csetupRandPerfTabs.py install
		sudo ${PYTHON} csetupODGInteger.py install
		sudo ${PYTHON} csetupSOInteger.py install
		sudo ${PYTHON} csetupBGInteger.py install
installVenv:
		${PYTHON} csetupRandPerfTabs.py install
		${PYTHON} csetupODGInteger.py install
		${PYTHON} csetupSOInteger.py install
		${PYTHON} csetupBGInteger.py install

testsBig:
		(cd Test; ${NOSETESTS} -vs noseTestsBigIntegerOutrankingDigraph.py)
testsInteger:
		(cd Test; ${NOSETESTS} -vs noseTestsIntegerOutrankingDigraph.py)
testsCorrelation:
		(cd Test; ${NOSETESTS} -vs noseTestsVerifyFitness.py)

tests:
		(cd Test; ${NOSETESTS} -vs noseTestsBigIntegerOutrankingDigraph.py)
		(cd Test; ${NOSETESTS} -vs noseTestsIntegerOutrankingDigraph.py)
		(cd Test; ${NOSETESTS} -vs noseTestsVerifyFitness.py)


