rem " points lignes supplémentaires %1 : nbre de val.prop.colonnes"
rem "                               %2 :  %1 -1"
rem "                               %3 :  nbre de lignes supplémentaires"
load val_prop.prn d %1 1
load compo.prn a %1 %2
load supp.prn b %3 %1
composupp b a d compsupp.prn
end
