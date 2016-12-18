FLAG = --inplace

codg:
		cython -3 -X boundscheck=False cOutrankingDigraphs.pyx
bodg:
		python3 csetupODG.py build_ext ${FLAG}
cso:
		cython -3 -X boundscheck=False cSortingDigraphs.pyx
bso:
		python3 csetupSO.py build_ext ${FLAG}
cbg:
		cython -3 -X boundscheck=False cBigOutrankingDigraphs.py
bbg:
		python3 csetupBG.py build_ext ${FLAG}
call:
		cython -3 -X boundscheck=False cOutrankingDigraphs.pyx
		cython -3 -X boundscheck=False cSortingDigraphs.pyx
		cython -3 -X boundscheck=False cBigOutrankingDigraphs.py
inplace:
		python3 csetupODG.py build_ext ${FLAG}
		python3 csetupSO.py build_ext ${FLAG}
		python3 csetupBG.py build_ext ${FLAG}
install:
		sudo python3 csetupODG.py install
		sudo python3 csetupSO.py install
		sudo python3 csetupBG.py install
codgdev:
		cython -3 -X boundscheck=False cOutrankingDigraphsDev.pyx
bodgdev:
		python3 csetupODGDev.py build_ext ${FLAG}
csodev:
		cython -3 -X boundscheck=False cSortingDigraphsDev.pyx
bsodev:
		python3 csetupSODev.py build_ext ${FLAG}
cbgdev:
		cython -3 -X boundscheck=False cBigOutrankingDigraphsDev.pyx
bbgdev:
		python3 csetupBGDev.py build_ext ${FLAG}
calldev:
		cython -3 -X boundscheck=False cOutrankingDigraphsDev.pyx
		cython -3 -X boundscheck=False cSortingDigraphsDev.pyx
		cython -3 -X boundscheck=False cBigOutrankingDigraphsDev.pyx
inplacedev:
		python3 csetupODGDev.py build_ext ${FLAG}
		python3 csetupSODev.py build_ext ${FLAG}
		python3 csetupBGDev.py build_ext ${FLAG}
installdev:
		sudo python3 csetupODGDev.py install
		sudo python3 csetupSODev.py install
		sudo python3 csetupBGDev.py install

cBigOutrankingDigraphsTests:
		make install
		(cd test; nosetests3 -v noseTestsBigOutrankingDigraph.py)
verboseCBigOutrankingDigraphsTests:
		make install
		(cd test; nosetests3 -vs noseTestsBigOutrankingDigraph.py)
cBigOutrankingDigraphsDevTests:
		make installdev
		(cd test; nosetests3 -v noseTestsBigOutrankingDigraphDev.py)
verboseCBigOutrankingDigraphsDevTests:
		make installdev
		(cd test; nosetests3 -vs noseTestsBigOutrankingDigraphDev.py)


