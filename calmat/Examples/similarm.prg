rem "--------------------------" 
rem " analyse des diffÚrences  " 
rem " entre lignes du tableau  " 
rem "--------------------------" 
load similarm.prn a 23 23 
b = dist_fact(a * `a) 
tridiag b val_prlg.prn vec_prlg.prn 
load vec_prlg.prn c 23 23
d = b * c 
save d compolg.prn 
rem "-----------------------------" 
rem " analyse des diffÚrences     " 
rem " entre colonnes du tableau   " 
rem "-----------------------------" 
load similarm.prn a 23 23 
b = dist_fact(`a * a) 
tridiag b val_prcl.prn vec_prcl.prn 
load vec_prcl.prn c 23 23
d = b * c 
save d compocl.prn 
end 
