FLAG = --inplace
PYTHON = python3
PYTEST = ${PYTHON} -m pytest

inplace:
		${PYTHON} csetupRandPerfTabs.py build_ext ${FLAG}
		${PYTHON} csetupODGInteger.py build_ext ${FLAG}
		${PYTHON} csetupSOInteger.py build_ext ${FLAG}
		${PYTHON} csetupSparseInteger.py build_ext ${FLAG}
		${PYTHON} csetupNpDigraphs.py build_ext ${FLAG}
install:
		sudo -H ${PYTHON} csetupRandPerfTabs.py install
		sudo -H ${PYTHON} csetupODGInteger.py install
		sudo -H ${PYTHON} csetupSOInteger.py install
		sudo -H ${PYTHON} csetupSparseInteger.py install
		sudo -H ${PYTHON} csetup.NpDigraphspy install
installVenv:
		${PYTHON} csetupRandPerfTabs.py install
		${PYTHON} csetupODGInteger.py install
		${PYTHON} csetupSOInteger.py install
		${PYTHON} csetupSparseInteger.py install
		${PYTHON} csetupNpDigraphs.py install
testsSparse:
		(cd Test; ${PYTEST} -vs pytestsSparseIntegerOutrankingDigraphs.py)
testsInteger:
		(cd Test; ${PYTEST} -vs pytestsIntegerOutrankingDigraphs.py)
testsCorrelation:
		(cd Test; ${PYTEST} -vs pytestsVerifyFitness.py)
testsNpDigraphs:
		(cd Test; ${PYTEST} -vs pytestsNpDigraphs.py)

tests:
		(cd Test; ${PYTEST} -v pytestsSparseIntegerOutrankingDigraphs.py)
		(cd Test; ${PYTEST} -v pytestsIntegerOutrankingDigraphs.py)
		(cd Test; ${PYTEST} -v pytestsVerifyFitness.py)
		(cd Test; ${PYTEST} -v pytestsNpDigraphs.py)

verboseTests:
		(cd Test; ${PYTEST} -vs pytestsSparseIntegerOutrankingDigraphs.py)
		(cd Test; ${PYTEST} -vs pytestsIntegerOutrankingDigraphs.py)
		(cd Test; ${PYTEST} -vs pytestsVerifyFitness.py)
		(cd Test; ${PYTEST} -vs pytestsNpDigraphs.py)
		(cd Test; ${PYTEST} -vs pytestsNpDigraphs.py)


