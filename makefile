## makefile for digraphs module installation
## R Bisdorff July 2018
## version 3.7
########################
PYTHON=python3
NOSETESTS=nosetests
SPHINX=sphinx-build
INSTALLDIR=/usr/local/bin

readme:
		echo -n " Digraph3 python3 modules' installer \n (c) R Bisdorff 2013-2014 University of Luxembourg\n Usage: \n ..> make install # installs in Python3, Python3.3 and Python3.4 (Linux, Mac OS)\n ..> make tests # runs the nose tests\n ..> make verbosetests # runs the verbose nose tests\n ..> make pTests # runs all available nose tests with GNU parallel\n\n Technical documentation available here:\n http://digraph3.readthedocs.io/en/latest/ or here:\n http://leopold-loewenheim.uni.lu/docDigraph3/ \n"
sphinx:
		(cd docSphinx; \
		${SPHINX} -E . html/ )

pydocs:
		cp arithmetics.py pyDoc/
		cp digraphsTools.py pyDoc/
		cp digraphs.py pyDoc/
		cp outrankingDigraphs.py pyDoc/
		cp perfTabs.py pyDoc/
		cp performanceQuantiles.py pyDoc/
		cp sortingDigraphs.py pyDoc/
		cp votingProfiles.py pyDoc/
		cp linearOrders.py pyDoc/
		cp weakOrders.py pyDoc/
		cp graphs.py pyDoc/
		cp randomNumbers.py pyDoc/
		cp randomDigraphs.py pyDoc/
		cp randomPerfTabs.py pyDoc/
		cp bigOutrankingDigraphs.py pyDoc/
		cp sparseOutrankingDigraphs.py pyDoc/
		cp xmcda.py pyDoc/
		cp iqagent.py test/
		(cd pyDoc; pydoc3 -w ./)

pTests:
		parallel --gnu cp {}.py test/ ::: arithmetics digraphsTools digraphs outrankingDigraphs perfTabs performanceQuantiles sortingDigraphs votingProfiles linearOrders weakOrders graphs randomNumbers randomDigraphs randomPerfTabs bigOutrankingDigraphs sparseOutrankingDigraphs xmcda iqagent
		(cd test; parallel --gnu -k ${NOSETESTS} -v ::: noseTests*.py )

tests:
		cp digraphsTools.py test/
		cp arithmetics.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsArithmetics.py)
		(cd test; ${NOSETESTS} -v noseTestsDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsOutrankingDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsPerfTab.py)
		(cd test; ${NOSETESTS} -v noseTestsRandomPerfTab.py)
		(cd test; ${NOSETESTS} -v noseTestsSortingDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsVotingProfile.py)
		(cd test; ${NOSETESTS} -v noseTestsLinearOrder.py)
		(cd test; ${NOSETESTS} -v noseTestsWeakOrders.py)
		(cd test; ${NOSETESTS} -v noseTestsGraph.py)
		(cd test; ${NOSETESTS} -v noseTestsRandomNumbers.py)
		(cd test; ${NOSETESTS} -v noseTestsRandomDigraph.py)
#		(cd test; ${NOSETESTS} -v noseTestsBigOutrankingDigraph.py)
		(cd test; ${NOSETESTS} -v noseTestsSparseOutrankingDigraph.py)


verboseTests:
		cp digraphsTools.py test/
		cp arithmetics.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsArithmetics.py)
		(cd test; ${NOSETESTS} -vs noseTestsDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsOutrankingDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsPerfTab.py)
		(cd test; ${NOSETESTS} -vs noseTestsRandomPerfTab.py)
		(cd test; ${NOSETESTS} -vs noseTestsSortingDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsVotingProfile.py)
		(cd test; ${NOSETESTS} -vs noseTestsLinearOrder.py)
		(cd test; ${NOSETESTS} -vs noseTestsWeakOrders.py)
		(cd test; ${NOSETESTS} -vs noseTestsGraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsRandomNumbers.py)
		(cd test; ${NOSETESTS} -vs noseTestsRandomDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsBigOutrankingDigraph.py)
		(cd test; ${NOSETESTS} -vs noseTestsSparseOutrankingDigraph.py)

digraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsDigraph.py)

verboseDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsDigraph.py)

sparseOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsSparseOutrankingDigraph.py)

verboseSparseOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsSparseOutrankingDigraph.py)

bigOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsBigOutrankingDigraph.py)

verboseBigOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsBigOutrankingDigraph.py)

graphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/		
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsGraph.py)

verboseGraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsGraph.py)

perfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsPerfTab.py)

randomPerfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp randomPerfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsRandomPerfTab.py)

verbosePerfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsPerfTab.py)

verboseRandomPerfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp randomPerfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsRandomPerfTab.py)

outrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsOutrankingDigraph.py)

verboseOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsOutrankingDigraph.py)

sortingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsSortingDigraph.py)

verboseSortingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsSortingDigraph.py)

votingProfilesTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsVotingProfile.py)

verboseVotingProfilesTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsVotingProfile.py)

linearOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsLinearOrder.py)

verboseLinearOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsLinearOrder.py)

weakOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsWeakOrders.py)

verboseWeakOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsWeakOrders.py)

randomDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsRandomDigraph.py)

verboseRandomDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp performanceQuantiles.py test/
		cp sortingDigraphs.py test/
		cp votingProfiles.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsRandomDigraph.py)

randomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -v noseTestsRandomNumbers.py)

verboseRandomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		cp iqagent.py test/
		(cd test; ${NOSETESTS} -vs noseTestsRandomNumbers.py)

arithmeticsTests:
		cp arithmetics.py test/
		(cd test; ${NOSETESTS} -v noseTestsArithmetics.py)
verboseArithmeticsTests:
		cp arithmetics.py test/
		(cd test; ${NOSETESTS} -vs noseTestsArithmetics.py)

install:
		sudo ${PYTHON} setup.py install
		sudo cp perrinMIS.c ./build
		(cd build; gcc -Wall -O4 -o perrinMIS perrinMIS.c)
		sudo cp build/perrinMIS ${INSTALLDIR}
		#sudo python3.7 setup.py install

installVenv:
		${PYTHON} setup.py install
