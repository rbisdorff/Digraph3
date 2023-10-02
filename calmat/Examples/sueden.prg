load sueden.prn a 207 25 
b = chi_deux(a) 
tridiag b val_prop.prn vec_prop.prn 
load vec_prop.prn c 25 25 
c = `c 
load val_prop.prn d 25 1 
compocor a c d compo.prn compabs.prn comprel.prn 
end 
