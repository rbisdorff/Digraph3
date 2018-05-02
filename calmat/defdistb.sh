#!/bin/bash
#########  generator for distance matrices
echo '**************************************************'
echo "   Rédaction de la procédure $1.prg "
echo "   de la factorisation de la distance $1.prn "
echo "   RB April 2008 (1994) "
echo '**************************************************"'
echo 'rem "*********************************"' > $1.prg
echo 'rem "* factorisation de la distance  *"' >> $1.prg
echo 'rem "*********************************"' >> $1.prg
echo "load $1.prn a $2 $3" >> $1.prg
echo 'b = dist_fact(a)' >> $1.prg
echo 'tridiag b val_prlg.prn vec_prlg.prn' >> $1.prg
echo "load vec_prlg.prn c $2 $2" >> $1.prg
echo 'd = b * c' >> $1.prg
echo 'save d compolg.prn' >> $1.prg

