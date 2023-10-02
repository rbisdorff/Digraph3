rem CALMAT 4.0  1990
rem CRP-CU CREDI R.Bisdorff
rem Analyse des corresspondances
rem corr.prg %1 %2 %3
rem %1 : fichier des données
rem dimensions : %2 x %3   
rem 
     load %1 a %2 %3
     rem "Calcul des distances de chi_deux"
     b = chi_deux(a)
     rem "Calcul des valeurs et vecteurs propres"
     tridiag b val_prop.prn vec_prop.prn
     load vec_prop.prn c %3 %3
     c = `c
     load val_prop.prn d %3 1
     rem "Calcul des nouvelles coordonnées dans la base propre"
     compocor a c d compo.prn compabs.prn comprel.prn
     end
