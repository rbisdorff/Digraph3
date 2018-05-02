rem ┌──────────────────────────────┐ 
rem │ analyse des corresspondances │ 
rem └──────────────────────────────┘ 
load testlm.prn a 63 6 
b = chi_deux(`a)
tridiag b val_prop.prn vec_prop.prn 
load vec_prop.prn c 63 5
c = `c 
load val_prop.prn d 5 1
compocor a c d compo.prn compabs.prn comprel.prn 
end 
