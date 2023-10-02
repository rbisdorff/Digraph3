     rem ┌──────────────────────────────┐
     rem │ CALMAT 3.0 LAUMIE R.Bisdorff │
     rem │ analyse des corresspondances │
     rem │ corr.prg source n1 n2 n3     │
     rem │ source : fichier des données │
     rem │ dimensions : n1 x n2         │
     rem │ n3: nombre d'axes projetées  │
     rem └──────────────────────────────┘
     load %1.prn a %2 %3
     rem Calcul des distances de chi_deux
     b = chi_deux(a)
     tridiag b val_prop.prn vec_prop.prn
     load vec_prop.prn c %3 %3
     d = b * c
     save d compcol.prn
     c = `c
     load val_prop.prn d %3 1
     rem Calcul des nouvelles coordonnées
     compocor a c d compo.prn compabs.prn comprel.prn
     end
