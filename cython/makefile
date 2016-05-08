odg:
		cython -3 -X boundscheck=False cOutrankingDigraphs.pyx
		python3 csetupODG.py build_ext --inplace
so:
		cython -3 -X boundscheck=False cSortingDigraphs.pyx
		python3 csetupSO.py build_ext --inplace
bg:
		cython -3 -X boundscheck=False cBigOutrankingDigraphs.py
		python3 csetupBG.py build_ext --inplace
all:
		cython -3 -X boundscheck=False cOutrankingDigraphs.pyx
		python3 csetupODG.py build_ext --inplace
		cython -3 -X boundscheck=False cSortingDigraphs.pyx
		python3 csetupSO.py build_ext --inplace
		cython -3 -X boundscheck=False cBigOutrankingDigraphs.py
		python3 csetupBG.py build_ext --inplace
