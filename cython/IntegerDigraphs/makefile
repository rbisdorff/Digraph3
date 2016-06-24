FLAG = --inplace

codg:
		cython -3 -X boundscheck=False cIntegerOutrankingDigraphs.pyx
bodg:
		python3 csetupODGInteger.py build_ext ${FLAG}
cso:
		cython -3 -X boundscheck=False cIntegerSortingDigraphs.pyx
bso:
		python3 csetupSOInteger.py build_ext ${FLAG}
cbg:
		cython -3 -X boundscheck=False cBigIntegerOutrankingDigraphs.py
bbg:
		python3 csetupBGInteger.py build_ext ${FLAG}
call:
		cython -3 -X boundscheck=False cIntegerOutrankingDigraphs.pyx
		cython -3 -X boundscheck=False cIntegerSortingDigraphs.pyx
		cython -3 -X boundscheck=False cBigIntegerOutrankingDigraphs.pyx
inplace:
		python3 csetupRandPerfTabs.py build_ext ${FLAG}
		python3 csetupODGInteger.py build_ext ${FLAG}
		python3 csetupSOInteger.py build_ext ${FLAG}
		python3 csetupBGInteger.py build_ext ${FLAG}
installVenv:
		python3 csetupRandPerfTabs.py install
		python3 csetupODGInteger.py install
		python3 csetupSOInteger.py install
		python3 csetupBGInteger.py install

