FLAG = inplace

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
		sudo python3 csetupODG.py build_ext
		sudo python3 csetupSO.py build_ext
		sudo python3 csetupBG.py build_ext
