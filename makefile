## makefile for digraphs module installation
## R Bisdorff May 2014
## version 3.3
########################

readme:
		echo -n " Digraph3 python3 modules' installer \n (c) R Bisdorff 2013-2014 University of Luxembourg\n Usage: \n ..> make install # installs in Python3, Python3.3 and Python3.4 (Linux, Mac OS)\n ..> make tests # runs the nose tests\n ..> make verbosetests # runs the verbose nose tests\n ..> make pTests # runs all available nose tests with GNU parallel\n\n Technical documentation available here:\n http://leopold-loewenheim.uni.lu/Digraph3/docSphinx/html/index.html \n"

sphinx:
		(cd docSphinx; \
		sphinx-build -E . html/ )

pydocs:
		cp arithmetics.py pyDoc/
		cp digraphsTools.py pyDoc/
		cp digraphs.py pyDoc/
		cp outrankingDigraphs.py pyDoc/
		cp perfTabs.py pyDoc/
		cp sortingDigraphs.py pyDoc/
		cp votingDigraphs.py pyDoc/
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
		parallel --gnu cp {}.py test/ ::: arithmetics digraphsTools digraphs outrankingDigraphs perfTabs sortingDigraphs votingDigraphs linearOrders weakOrders graphs randomNumbers randomDigraphs randomPerfTabs bigOutrankingDigraphs sparseOutrankingDigraphs xmcda iqagent
		(cd test; parallel --gnu -k nosetests3 -v ::: noseTests*.py )

tests:
		cp digraphsTools.py test/
		cp arithmetics.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsArithmetics.py)
		(cd test; nosetests3 -v noseTestsDigraph.py)
		(cd test; nosetests3 -v noseTestsOutrankingDigraph.py)
		(cd test; nosetests3 -v noseTestsPerfTab.py)
		(cd test; nosetests3 -v noseTestsRandomPerfTab.py)
		(cd test; nosetests3 -v noseTestsSortingDigraph.py)
		(cd test; nosetests3 -v noseTestsVotingDigraph.py)
		(cd test; nosetests3 -v noseTestsLinearOrder.py)
		(cd test; nosetests3 -v noseTestsWeakOrders.py)
		(cd test; nosetests3 -v noseTestsGraph.py)
		(cd test; nosetests3 -v noseTestsRandomNumbers.py)
		(cd test; nosetests3 -v noseTestsRandomDigraph.py)
#		(cd test; nosetests3 -v noseTestsBigOutrankingDigraph.py)
		(cd test; nosetests3 -v noseTestsSparseOutrankingDigraph.py)


verboseTests:
		cp digraphsTools.py test/
		cp arithmetics.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsArithmetics.py)
		(cd test; nosetests3 -vs noseTestsDigraph.py)
		(cd test; nosetests3 -vs noseTestsOutrankingDigraph.py)
		(cd test; nosetests3 -vs noseTestsPerfTab.py)
		(cd test; nosetests3 -vs noseTestsRandomPerfTab.py)
		(cd test; nosetests3 -vs noseTestsSortingDigraph.py)
		(cd test; nosetests3 -vs noseTestsVotingDigraph.py)
		(cd test; nosetests3 -vs noseTestsLinearOrder.py)
		(cd test; nosetests3 -vs noseTestsWeakOrders.py)
		(cd test; nosetests3 -vs noseTestsGraph.py)
		(cd test; nosetests3 -vs noseTestsRandomNumbers.py)
		(cd test; nosetests3 -vs noseTestsRandomDigraph.py)
		#(cd test; nosetests3 -vs noseTestsBigOutrankingDigraph.py)
		(cd test; nosetests3 -vs noseTestsSparseOutrankingDigraph.py)

digraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsDigraph.py)

verboseDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -vs noseTestsDigraph.py)

sparseOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -v noseTestsSparseOutrankingDigraph.py)

verboseSparseOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -vs noseTestsSparseOutrankingDigraph.py)

bigOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -v noseTestsBigOutrankingDigraph.py)

verboseBigOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -vs noseTestsBigOutrankingDigraph.py)

graphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsGraph.py)

verboseGraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsGraph.py)

perfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsPerfTab.py)

randomPerfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp randomPerfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsRandomPerfTab.py)

verbosePerfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsPerfTab.py)

verboseRandomPerfTabsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp randomPerfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp bigOutrankingDigraphs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -vs noseTestsRandomPerfTab.py)

outrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsOutrankingDigraph.py)

verboseOutrankingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsOutrankingDigraph.py)

sortingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsSortingDigraph.py)

verboseSortingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsSortingDigraph.py)

votingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp sparseOutrankingDigraphs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -v noseTestsVotingDigraph.py)

verboseVotingDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsVotingDigraph.py)

linearOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsLinearOrder.py)

verboseLinearOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -vs noseTestsLinearOrder.py)

weakOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -v noseTestsWeakOrders.py)

verboseWeakOrdersTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsWeakOrders.py)

randomDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		cp randomNumbers.py test/
		cp randomDigraphs.py test/
		cp randomPerfTabs.py test/
		cp xmcda.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -v noseTestsRandomDigraph.py)

verboseRandomDigraphsTests:
		cp digraphsTools.py test/
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
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
		(cd test; nosetests3 -vs noseTestsRandomDigraph.py)

randomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -v noseTestsRandomNumbers.py)

verboseRandomNumbersTests:
		cp digraphsTools.py test/
		cp randomNumbers.py test/
		cp iqagent.py test/
		(cd test; nosetests3 -vs noseTestsRandomNumbers.py)

arithmeticsTests:
		cp arithmetics.py test/
		(cd test; nosetests3 -v noseTestsArithmetics.py)
verboseArithmeticsTests:
		cp arithmetics.py test/
		(cd test; nosetests3 -vs noseTestsArithmetics.py)

install:
		sudo python3 setup.py install
#		sudo python3.3 setup.py install
		sudo python3.5 setup.py install
		sudo python3.6 setup.py install

installVenv:
		python3 setup.py install
#		python3.3 setup.py install
#		python3.4 setup.py install

#installPyPy:
#		pypy3 setup.py install
