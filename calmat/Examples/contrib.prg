load contrib.dat a 10 23 
b = chi_deux(a) 
tridiag b val_prop.prn vec_prop.prn 
load vec_prop.prn c 23 23
c = `c 
load val_prop.prn d 23 1
compocor a c d compo.prn compabs.prn comprel.prn 
end 
