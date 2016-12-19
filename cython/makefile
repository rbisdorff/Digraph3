FLAG = --inplace

codg:
		cython -3 -X boundscheck=True cIntegerOutrankingDigraphs.pyx
bodg:
		python3 csetupODGInteger.py build_ext ${FLAG}
cso:
		cython -3 -X boundscheck=True cIntegerSortingDigraphs.pyx
bso:
		python3 csetupSOInteger.py build_ext ${FLAG}
cbg:
		cython -3 -X boundscheck=True cBigIntegerOutrankingDigraphs.py
bbg:
		python3 csetupBGInteger.py build_ext ${FLAG}
call:
		cython -3 -X boundscheck=True cIntegerOutrankingDigraphs.pyx
		cython -3 -X boundscheck=True cIntegerSortingDigraphs.pyx
		cython -3 -X boundscheck=True cBigIntegerOutrankingDigraphs.pyx
inplace:
		python3 csetupRandPerfTabs.py build_ext ${FLAG}
		python3 csetupODGInteger.py build_ext ${FLAG}
		python3 csetupSOInteger.py build_ext ${FLAG}
		python3 csetupBGInteger.py build_ext ${FLAG}
install:
		sudo python3.5 csetupRandPerfTabs.py install
		sudo python3.5 csetupODGInteger.py install
		sudo python3.5 csetupSOInteger.py install
		sudo python3.5 csetupBGInteger.py install
installVenv:
		python3 csetupRandPerfTabs.py install
		python3 csetupODGInteger.py install
		python3 csetupSOInteger.py install
		python3 csetupBGInteger.py install
test:
		python3 testCythonInteger.py

