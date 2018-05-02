rem " ┌─────────────────────────┐ "
rem " │ analyse des différences │ "
rem " │ entre lignes du tableau │ "
rem " └─────────────────────────┘ "
load sechs.prn a 6 6 
b = dist_fact(a * `a) 
tridiag b val_prlg.prn vec_prlg.prn 
load vec_prlg.prn c 6 6 
d = b * c 
save d compolg.prn 
rem "┌─────────────────────────┐ "
rem "│ analyse des différences │ "
rem "│ entre colonnes du tabl. │ "
rem "└─────────────────────────┘ "
load sechs.prn a 6 6 
b = dist_fact(`a * a) 
tridiag b val_prcl.prn vec_prcl.prn 
load vec_prlg.prn c 6 6 
d = b * c 
save d compocl.prn 
end 
