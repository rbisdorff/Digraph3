## makefile for digraphs module installation
## R Bisdorff May 2014
## version 3.3
########################
.PHONY:	readme sphinx


readme:
		echo " Digraph3 python3 modules' installer \n (c) R Bisdorff 2013-2014 University of Luxembourg\n Usage: \n ..> make install # installs in Python3, Python3.3 and Python3.4 (Linux, Mac OS)\n ..> make tests # runs the nose tests\n ..> make verbosetests # runs the verbose nose tests\n ..> make pTests # runs all available nose tests with GNU parallel\n\n Technical documentation available here:\n http://leopold-loewenheim.uni.lu/Digraph3/docSphinx/html/index.html \n"

sphinx:
		(cd docSphinx; \
		sphinx-build -E . html/ )

pTests:
		parallel --gnu cp {}.py test/ ::: digraphs perfTabs sortingDigraphs votingDigraphs linearOrders weakOrders graphs
		(cd test; parallel --gnu -k nosetests3 -v ::: noseTests*.py )

tests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsDigraph.py)
		(cd test; nosetests3 -v noseTestsOutrankingDigraph.py)
		(cd test; nosetests3 -v noseTestsPerfTab.py)
		(cd test; nosetests3 -v noseTestsSortingDigraph.py)
		(cd test; nosetests3 -v noseTestsVotingDigraph.py)
		(cd test; nosetests3 -v noseTestsLinearOrder.py)
		(cd test; nosetests3 -v noseTestsWeakOrders.py)
		(cd test; nosetests3 -v noseTestsGraph.py)

verboseTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsDigraph.py)
		(cd test; nosetests3 -vs noseTestsOutrankingDigraph.py)
		(cd test; nosetests3 -vs noseTestsPerfTab.py)
		(cd test; nosetests3 -vs noseTestsSortingDigraph.py)
		(cd test; nosetests3 -vs noseTestsVotingDigraph.py)
		(cd test; nosetests3 -vs noseTestsLinearOrder.py)
		(cd test; nosetests3 -vs noseTestsWeakOrders.py)
		(cd test; nosetests3 -vs noseTestsGraph.py)

digraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsDigraph.py)

verboseDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsDigraph.py)

graphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsGraph.py)

verboseGraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsGraph.py)

perfTabsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsPerfTab.py)

verbosePerfTabsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsPerfTab.py)

outrankingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsOutrankingDigraph.py)

verboseOutrankingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsOutrankingDigraph.py)

sortingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsSortingDigraph.py)

verboseSortingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsSortingDigraph.py)

votingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsVotingDigraph.py)

verboseVotingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsVotingDigraph.py)

linearOrdersTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsLinearOrder.py)

verboseLinearOrdersTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsLinearOrder.py)

weakOrdersTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -v noseTestsWeakOrders.py)

verboseWeakOrdersTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		cp weakOrders.py test/
		cp graphs.py test/
		(cd test; nosetests3 -vs noseTestsWeakOrders.py)

install:
		sudo python3 setup.py install
		sudo python3.3 setup.py install
		sudo python3.4 setup.py install

