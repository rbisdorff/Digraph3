## makefile for digraphs module installation
## R Bisdorff Nov 2020
## version 3.9
########################
PYTHON=python3
PYTEST=pytest
SPHINX=sphinx-build
INSTALLDIR=/usr/local/bin
CC=gcc
CFLAGS=-Wall -O3

modules = arithmetics.py digraphs.py digraphsTools.py graphs.py linearOrders.py outrankingDigraphs.py performanceQuantiles.py perfTabs.py randomDigraphs.py randomNumbers.py randomPerfTabs.py sortingDigraphs.py sparseOutrankingDigraphs.py transitiveDigraphs.py votingProfiles.py xmcda.py

readme:
		echo -n " Digraph3 python3 modules' installer \n (c) R Bisdorff 2013-2014 University of Luxembourg\n Usage: \n ..> make install # installs in Python3+ (Linux, Mac OS)\n ..> make tests # runs the nose tests\n ..> make verbosetests # runs the verbose nose tests\n ..> make pTests # runs all available nose tests with GNU parallel\n\n Technical documentation available here:\n http://digraph3.readthedocs.io/en/latest/ or here:\n http://leopold-loewenheim.uni.lu/docDigraph3/ \n"
sphinx:
		(cd docSphinx; \
		${SPHINX} -Ea . html/ )

#sphinxLatex:
#		(cd docSphinx; \
#		${SPHINX} -E -a -b latex . latex/ )

sphinxLatexPDF:
		(cd docSphinx; \
		 make latexpdf; \
		cp _build/latex/*.pdf ./latex)

pydocs:
		for md in ${modules}; do \
		    cp $$md pyDoc/; \
		done
		(cd pyDoc; pydoc3 -w ./)

pTests:
		parallel --gnu cp {}.py test/ ::: arithmetics digraphsTools digraphs outrankingDigraphs perfTabs performanceQuantiles sortingDigraphs votingProfiles linearOrders transitiveDigraphs graphs randomNumbers randomDigraphs randomPerfTabs sparseOutrankingDigraphs xmcda
		(cd test; parallel --gnu -k ${PYTEST} -v ::: pytests*)

tests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytests*)

verboseTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytests*)

digraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsDigraphs.py)

verboseDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsDigraphs.py)

sparseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsSparseOutrankingDigraphs.py)

verboseSparseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsSparseOutrankingDigraphs.py)

graphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsGraphs.py)

verboseGraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsGraphs.py)

perfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsPerfTab.py)

randomPerfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsRandomPerfTab.py)

verbosePerfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsPerfTab.py)

verboseRandomPerfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsRandomPerfTab.py)

outrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsOutrankingDigraphs.py)

verboseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsOutrankingDigraphs.py)

sortingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsSortingDigraphs.py)

verboseSortingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsSortingDigraphs.py)

votingProfilesTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsVotingProfile.py)

verboseVotingProfilesTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsVotingProfile.py)

linearOrdersTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsLinearOrder.py)

verboseLinearOrdersTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsLinearOrder.py)

transitiveDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsTransitiveDigraphs.py)

verboseTransitiveDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsTransitiveDigraphs.py)

randomDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -v pytestsRandomDigraphs.py)

verboseRandomDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${PYTEST} -vs pytestsRandomDigraphs.py)

randomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		(cd test; ${PYTEST} -v pytestsRandomNumbers.py)

verboseRandomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		(cd test; ${PYTEST} -vs pytestsRandomNumbers.py)

arithmeticsTests:
		cp arithmetics.py test/
		(cd test; ${PYTEST} -v pytestsArithmetics.py)
verboseArithmeticsTests:
		cp arithmetics.py test/
		(cd test; ${PYTEST} -vs pytestsArithmetics.py)

cythonTests:
		(cd cython; make tests)

install:
		sudo ${PYTHON} setup.py install
		# uncomment or adapt makefile for specific python  versions
		#sudo python3.6 setup.py install
		#sudo python3.7 setup.py install
		#sudo python3.8 setup.py install

installVenv:
		${PYTHON} setup.py install

installPerrin:
		(cd perrinMIS; ${CC} ${CFLAGS} -o perrinMIS perrinMIS.c)
		sudo cp perrinMIS/perrinMIS ${INSTALLDIR}

installPerrinUser:
		(cd perrinMIS; ${CC} ${CFLAGS} -o perrinMIS perrinMIS.c)
		cp perrinMIS/perrinMIS ${HOME}/.bin
