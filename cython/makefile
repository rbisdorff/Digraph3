FLAG = --inplace
PYTHON = python3
NOSETESTS = nosetests3

inplace:
		${PYTHON} csetupRandPerfTabs.py build_ext ${FLAG}
		${PYTHON} csetupODGInteger.py build_ext ${FLAG}
		${PYTHON} csetupSOInteger.py build_ext ${FLAG}
		${PYTHON} csetupSparseInteger.py build_ext ${FLAG}
install:
		sudo -H ${PYTHON} csetupRandPerfTabs.py install
		sudo -H ${PYTHON} csetupODGInteger.py install
		sudo -H ${PYTHON} csetupSOInteger.py install
		sudo -H ${PYTHON} csetupSparseInteger.py install
installVenv:
		${PYTHON} csetupRandPerfTabs.py install
		${PYTHON} csetupODGInteger.py install
		${PYTHON} csetupSOInteger.py install
		${PYTHON} csetupSparseInteger.py install
testsSparse:
		(cd Test; ${NOSETESTS} -vs noseTestsSparseIntegerOutrankingDigraph.py)
testsInteger:
		(cd Test; ${NOSETESTS} -vs noseTestsIntegerOutrankingDigraph.py)
testsCorrelation:
		(cd Test; ${NOSETESTS} -vs noseTestsVerifyFitness.py)

tests:
		(cd Test; ${NOSETESTS} -v noseTestsSparseIntegerOutrankingDigraph.py)
		(cd Test; ${NOSETESTS} -v noseTestsIntegerOutrankingDigraph.py)
		(cd Test; ${NOSETESTS} -v noseTestsVerifyFitness.py)

verboseTests:
		(cd Test; ${NOSETESTS} -vs noseTestsSparseIntegerOutrankingDigraph.py)
		(cd Test; ${NOSETESTS} -vs noseTestsIntegerOutrankingDigraph.py)
		(cd Test; ${NOSETESTS} -vs noseTestsVerifyFitness.py)


