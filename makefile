## makefile for digraphs module installation
## R Bisdorff (c) 2023-2025
## version 3.13.2
########################
# use PYTHON parameter for selecting a
# specific Python environment as follows:
# ..$ make install PYTHON=python3.9
########################
PYTHON=python3
PYTEST=${PYTHON} -m pytest
SPHINX=${PYTHON} -m sphinx
INSTALLDIR=/usr/local/bin
BUILDDIR=_build
TESTDIR=test/results
JOBS=""

CC=gcc
CFLAGS=-Wall -O3

modules = arithmetics.py bachetNumbers.py digraphs.py digraphsTools.py graphs.py linearOrders.py mpOutrankingDigraphs.py outrankingDigraphs.py pairings.py performanceQuantiles.py perfTabs.py randomDigraphs.py randomNumbers.py randomPerfTabs.py ratingDigraphs.py sortingDigraphs.py sparseOutrankingDigraphs.py transitiveDigraphs.py dynamicProgramming.py votingProfiles.py xmcda.py

readme:
		echo -n " Digraph3 python3 modules' installer \n (c) R Bisdorff 2013-2022 Emeritus University of Luxembourg\n Usage: \n ..$$ make install      # installs with sudo in Python3+ (Linux, Mac OS)\n ..$$ make installVenv  # installs in a user's virtual python environment\n ..$$ make tests        # runs a series of pytests \n ..$$ make verbosetests # runs the verbose pytests\n ..$$ make pTests       # runs all available pytests with GNU parallel\n\n Technical documentation available here:\n http://digraph3.readthedocs.io/en/latest/ \n"

# make sphinx html documentation
#sphinx:
#		(cd docSphinx; \
#		${SPHINX} -Ea . $(BUILDDIR)/html )
#		# use PYTHON parameter for selecting a
#		# specific Python environment like:
#		# ..$ make sphinx PYTHON=python3.9

# make sphinx html documentation
sphinx:
		(cd docSphinx; \
		${SPHINX} -b html -d _build/doctrees   . $(BUILDDIR)/html; \
		echo "The html files are in /docSphinx/_build/html.")

sphinxLatexPDF:
		(cd docSphinx; \
		${SPHINX} -b latex -d _build/doctrees   . ${BUILDDIR}/latex; \
		echo "Running LaTeX files through pdflatex..."; \
		${MAKE} -C ${BUILDDIR}/latex all-pdf; \
		cp ${BUILDDIR}/latex/digraph3*.pdf ${BUILDDIR}/html/_static; \
		cp ${BUILDDIR}/latex/digraph3*.pdf _static;\
		echo "The PDF files are in /docSphinx/_static";\
		echo "              and in /docSphinx/_build/html/_static")

# make sphinx ebook
# sphinxEpub:
# 		(cd docSphinx; \
# 		${SPHINX} -b epub -d _build/doctrees   . $(BUILDDIR)/epub)

# make automatic module documentation
pydocs:
		for md in ${modules}; do \
		    cp $$md pyDoc/; \
		done
		(cd pyDoc; pydoc3 -w ./; rm *.py)

pTests:
		parallel --gnu cp {}.py ${TESTDIR} ::: arithmetics digraphsTools digraphs outrankingDigraphs perfTabs performanceQuantiles sortingDigraphs votingProfiles linearOrders transitiveDigraphs graphs pairings randomNumbers randomDigraphs randomPerfTabs ratingDigraphs sparseOutrankingDigraphs xmcda
		(cd ${TESTDIR}; parallel --gnu -k ${PYTEST} -v ::: ../pytests*; rm tmp*)

tests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd test/results; ${PYTEST} ${JOBS} -v ../pytests*; rm tmp*)

verboseTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytests*; rm tmp*)

digraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsDigraphs.py)

verboseDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsDigraphs.py)

sparseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsSparseOutrankingDigraphs.py)

verboseSparseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsSparseOutrankingDigraphs.py)

graphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsGraphs.py)

verboseGraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsGraphs.py)

perfTabsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsPerfTabs.py)

randomPerfTabsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsRandomPerfTabs.py)

verbosePerfTabsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsPerfTabs.py)

verboseRandomPerfTabsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsRandomPerfTabs.py)

outrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsOutrankingDigraphs.py)

verboseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsOutrankingDigraphs.py)

sortingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsSortingDigraphs.py)

verboseSortingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsSortingDigraphs.py)
ratingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsRatingDigraphs.py)

verboseRatingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsRatingDigraphs.py)

votingProfilesTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsVotingProfiles.py)

verboseVotingProfilesTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsVotingProfiles.py)

pairingsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsPairings.py)

verbosePairingsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsPairings.py)
linearOrdersTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsLinearOrders.py)

verboseLinearOrdersTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsLinearOrders.py)

transitiveDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsTransitiveDigraphs.py)

verboseTransitiveDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsTransitiveDigraphs.py)

randomDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsRandomDigraphs.py)

verboseRandomDigraphsTests:
		for md in ${modules}; do \
		    cp $$md ${TESTDIR}/; \
		done
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsRandomDigraphs.py)

randomNumbersTests:
		cp digraphsTools.py ${TESTDIR}/
		cp randomNumbers.py ${TESTDIR}/
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsRandomNumbers.py)

verboseRandomNumbersTests:
		cp digraphsTools.py ${TESTDIR}/
		cp randomNumbers.py ${TESTDIR}/
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsRandomNumbers.py)

arithmeticsTests:
		cp arithmetics.py ${TESTDIR}/
		(cd ${TESTDIR}; ${PYTEST} -v ../pytestsArithmetics.py)
verboseArithmeticsTests:
		cp arithmetics.py ${TESTDIR}/
		(cd ${TESTDIR}; ${PYTEST} -vs ../pytestsArithmetics.py)
mpTests:
		(cd ${TESTDIR}; ${PYTHON} ../../mpOutrankingDigraphs.py) 

cythonTests:
		(cd cython; make tests)

verboseCythonTests:
		(cd cython; make verboseTests)

install:
		sudo ${PYTHON} setup.py install

installVenv:
		${PYTHON} setup.py install	

installPip:
		# sudo ${PYTHON} setup.py install
		# deprecated since python3.10.4
		# Warning: requires python3.10+
		# For a system wide installation
		#      sudo make installPip
		${PYTHON} -m pip -v install --upgrade --src = .	

installPerrin:
		(cd perrinMIS; ${CC} ${CFLAGS} -o perrinMIS perrinMIS.c)
		sudo cp perrinMIS/perrinMIS ${INSTALLDIR}

installPerrinUser:
		(cd perrinMIS; ${CC} ${CFLAGS} -o perrinMIS perrinMIS.c)
		cp perrinMIS/perrinMIS ${HOME}/.bin
