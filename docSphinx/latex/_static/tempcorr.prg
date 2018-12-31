rem "*********************************"
rem "* factorisation de la distance  *"
rem "*********************************"
load tempcorr.prn a 7 7
b = (a * `a)
save b corr_lg.prn
tridiag b val_prlg.prn vec_prlg.prn
load vec_prlg.prn c 7 7
d = b * c
save d compolg.prn
