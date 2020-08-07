rem "****************************"
rem "* analyse des différences  *"
rem "* entre lignes du tableau  *"
rem "****************************"
load tempcorr.prn a 7 7
b = dist_fact(a * `a)
save b corr_lg.prn
tridiag b val_prlg.prn vec_prlg.prn
load vec_prlg.prn c 7 7
d = b * c
save d compolg.prn
rem "****************************"
rem "* analyse des différences  *"
rem "* entre colonnes du tabl.  *"
rem "****************************"
load tempcorr.prn a 7 7
b = dist_fact(`a * a)
tridiag b val_prcl.prn vec_prcl.prn
load vec_prcl.prn c 7 7
d = b * c
save d compocl.prn
end
