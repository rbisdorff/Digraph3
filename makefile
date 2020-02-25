## makefile for digraphs module installation
## R Bisdorff July 2018
## version 3.7
########################
PYTHON=python3
NOSETESTS=nosetests
SPHINX=sphinx-build
INSTALLDIR=/usr/local/bin
CC=gcc
CFLAGS=-Wall -O3

modules = arithmetics.py digraphs.py digraphsTools.py graphs.py linearOrders.py outrankingDigraphs.py performanceQuantiles.py perfTabs.py randomDigraphs.py randomNumbers.py randomPerfTabs.py sortingDigraphs.py sparseOutrankingDigraphs.py transitiveDigraphs.py votingProfiles.py xmcda.py

readme:
		echo -n " Digraph3 python3 modules' installer \n (c) R Bisdorff 2013-2014 University of Luxembourg\n Usage: \n ..> make install # installs in Python3, Python3.3 and Python3.4 (Linux, Mac OS)\n ..> make tests # runs the nose tests\n ..> make verbosetests # runs the verbose nose tests\n ..> make pTests # runs all available nose tests with GNU parallel\n\n Technical documentation available here:\n http://digraph3.readthedocs.io/en/latest/ or here:\n http://leopold-loewenheim.uni.lu/docDigraph3/ \n"
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
		(cd test; parallel --gnu -k ${NOSETESTS} -v ::: noseTests*.py )

tests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsArithmetics.py)
		(cd test; ${NOSETESTS} -v noseTestsDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsOutrankingDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsPerfTab.py)
		(cd test; ${NOSETESTS} -v noseTestsRandomPerfTab.py)
		(cd test; ${NOSETESTS} -v noseTestsSortingDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsVotingProfile.py)
		(cd test; ${NOSETESTS} -v noseTestsLinearOrder.py)
		(cd test; ${NOSETESTS} -v noseTestsTransitiveDigraphs.py)
		(cd test; ${NOSETESTS} -v noseTestsGraph.py)
		(cd test; ${NOSETESTS} -v noseTestsRandomNumbers.py)
		(cd test; ${NOSETESTS} -v noseTestsRandomDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsSparseOutrankingDigraph.py)


verboseTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsArithmetics.py)
		(cd test; ${NOSETESTS} -vs noseTestsDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsOutrankingDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsPerfTab.py)
		(cd test; ${NOSETESTS} -vs noseTestsRandomPerfTab.py)
		(cd test; ${NOSETESTS} -vs noseTestsSortingDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsVotingProfile.py)
		(cd test; ${NOSETESTS} -vs noseTestsLinearOrder.py)
		(cd test; ${NOSETESTS} -vs noseTestsTransitiveDigraphs.py)
		(cd test; ${NOSETESTS} -vs noseTestsGraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsRandomNumbers.py)
		(cd test; ${NOSETESTS} -vs noseTestsRandomDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsSparseOutrankingDigraph.py)

digraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsDigraph.py)

verboseDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsDigraph.py)

sparseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsSparseOutrankingDigraph.py)

verboseSparseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsSparseOutrankingDigraph.py)

graphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsGraph.py)

verboseGraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsGraph.py)

perfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsPerfTab.py)

randomPerfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsRandomPerfTab.py)

verbosePerfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsPerfTab.py)

verboseRandomPerfTabsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsRandomPerfTab.py)

outrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsOutrankingDigraph.py)

verboseOutrankingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsOutrankingDigraph.py)

sortingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsSortingDigraph.py)

verboseSortingDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsSortingDigraph.py)

votingProfilesTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsVotingProfile.py)

verboseVotingProfilesTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsVotingProfile.py)

linearOrdersTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsLinearOrder.py)

verboseLinearOrdersTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsLinearOrder.py)

transitiveDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsTransitiveDigraphs.py)

verboseTransitiveDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsTransitiveDigraphs.py)

randomDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -v noseTestsRandomDigraph.py)

verboseRandomDigraphsTests:
		for md in ${modules}; do \
		    cp $$md test/; \
		done
		(cd test; ${NOSETESTS} -vs noseTestsRandomDigraph.py)

randomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		(cd test; ${NOSETESTS} -v noseTestsRandomNumbers.py)

verboseRandomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		(cd test; ${NOSETESTS} -vs noseTestsRandomNumbers.py)

arithmeticsTests:
		cp arithmetics.py test/
		(cd test; ${NOSETESTS} -v noseTestsArithmetics.py)
verboseArithmeticsTests:
		cp arithmetics.py test/
		(cd test; ${NOSETESTS} -vs noseTestsArithmetics.py)

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
