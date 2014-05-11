## makefile for digraphs module installation
## R Bisdorff May 2011
########################
.PHONY:	readme sphinx


readme:
		echo " digraphs python module installer $Revision: 1.39 $ \n R Bisdorff May 2011 University of Luxembourg\n usage: \n ..$ make docHTML # generates the html documentation\n ..$ make docPDF # generates the PDF document\n ..$ make tests # runs the nose tests\n ..$ make verbosetests # runs the verbose nose tests\n ..$ make install # installs on Ubuntu\n ..$ make 2to3 # converts py2 sources to py3 versions (see py3/*)\n ..$ make install3 # install Python 3 version"


docHTML:
		rm doc/*.html
		cd doc ;\
		hyperlatex digraphsdoc.tex ; \
		./sedpngs ; \
		ln -s digraphsdoc.html index.html

docPDF:
		(cd doc; latex digraphsdoc.tex)
		cd doc; \
                makeindex digraphsdoc.idx; \
		latex digraphsdoc.tex ; \
		latex digraphsdoc.tex ; \
		dvipdf digraphsdoc.dvi

sphinx:
		(cd docSphinx; \
		sphinx-build -E . html/ )

pTests:
		parallel cp {}.py test/ ::: digraphs perfTabs sortingDigraphs votingDigraphs linearOrders weakOrders graphs
		(cd test; parallel -k nosetests3 -v noseTests{}.py ::: Digraph OutrankingDigraph PerfTab SortingDigraph VotingDigraph LinearOrder WeakOrders Graph )

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

