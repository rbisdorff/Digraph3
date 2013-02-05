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
		cd docSphinx; \
		sphinx-build -E . html/

tests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		(cd test; nosetests -v noseTestsDigraph.py)
		(cd test; nosetests -v noseTestsOutrankingDigraph.py)
		(cd test; nosetests -v noseTestsPerfTab.py)
		(cd test; nosetests -v noseTestsSortingDigraph.py)
		(cd test; nosetests -v noseTestsVotingDigraph.py)
		(cd test; nosetests -v noseTestsLinearOrder.py)

verboseTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		(cd test; nosetests -vs noseTestsDigraph.py)
		(cd test; nosetests -vs noseTestsOutrankingDigraph.py)
		(cd test; nosetests -vs noseTestsPerfTab.py)
		(cd test; nosetests -vs noseTestsSortingDigraph.py)
		(cd test; nosetests -vs noseTestsVotingDigraph.py)
		(cd test; nosetests -vs noseTestsLinearOrder.py)

digraphsTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		(cd test; nosetests -v noseTestsDigraph.py)

verboseDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		(cd test; nosetests -vs noseTestsDigraph.py)

perfTabsTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		(cd test; nosetests -v noseTestsPerfTab.py)

verbosePerfTabsTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		(cd test; nosetests -vs noseTestsPerfTab.py)

outrankingDigraphsTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		(cd test; nosetests -v noseTestsOutrankingDigraph.py)

verboseOutrankingDigraphsTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp perfTabs.py test/
		(cd test; nosetests -vs noseTestsOutrankingDigraph.py)

sortingDigraphsTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		(cd test; nosetests -v noseTestsSortingDigraph.py)

verboseSortingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		(cd test; nosetests -vs noseTestsSortingDigraph.py)

votingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		(cd test; nosetests -v noseTestsVotingDigraph.py)

verboseVotingDigraphsTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		(cd test; nosetests -vs noseTestsVotingDigraph.py)

linearOrdersTests:
		cp digraphs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		(cd test; nosetests -v noseTestsLinearOrder.py)

verboseLinearOrdersTests:
		cp digraphs.py test/
		cp perfTabs.py test/
		cp outrankingDigraphs.py test/
		cp sortingDigraphs.py test/
		cp votingDigraphs.py test/
		cp linearOrders.py test/
		(cd test; nosetests -vs noseTestsLinearOrder.py)

2to3:		
		cp  digraphs.py py3/digraphs.py
		cp  perfTabs.py py3/perfTabs.py
		cp  outrankingDigraphs.py py3/outrankingDigraphs.py
		cp  votingDigraphs.py py3/votingDigraphs.py
		cp  sortingDigraphs.py py3/sortingDigraphs.py
		cp  linearOrders.py py3/linearOrders.py
		(cd py3; 2to3 -f all -w digraphs.py)
		(cd py3; 2to3 -f all -w perfTabs.py)
		(cd py3; 2to3 -f all -w outrankingDigraphs.py)
		(cd py3; 2to3 -f all -w votingDigraphs.py)
		(cd py3; 2to3 -f all -w sortingDigraphs.py)
		(cd py3; 2to3 -f all -w linearOrders.py)

install:
		sudo python setup.py install
#		sudo /opt/local/bin/python setup.py install
#		sudo /usr/bin/python setup.py install

install3:
		(cd py3; sudo python3 setup.py install)

