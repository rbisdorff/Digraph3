load agdtpl15a5.txt a 23 23 
b = dist_fact(a * `a) 
tridiag b val_prlg.txt vec_prlg.txt 
load vec_prlg.txt c 23 23
d = b * c 
save d compolg.txt 
load similarm.txt a 23 23 
b = dist_fact(`a * a) 
tridiag b val_prcl.txt vec_prcl.txt 
load vec_prcl.txt c 23 23
d = b * c 
save d compocl.txt 
end 
