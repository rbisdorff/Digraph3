##########################
# install all cythonized modules inplace with
# ...$python3 setup.py buid_ext --inplace
# (c) R. Bisdorff 2024
#####################
FLAG = --inplace
PYTHON = python3
PYTEST = ${PYTHON} -m pytest

inplace:
		${PYTHON} setup.py build_ext ${FLAG}
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


