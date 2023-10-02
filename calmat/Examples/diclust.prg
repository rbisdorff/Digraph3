rem "diclust"
load diclust.txt a 10 10 
tridiag a val_prlg.prn vec_prlg.prn 
load vec_prlg.prn b 10 10 
c = a * b 
save c dires.prn 
end 
