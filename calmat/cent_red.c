/********************************************************
 *  CALMAT  ver 2.0    juin 1989                        *
 *  source CENT_RED.C                                   *
 ********************************************************/
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#include "calmat.h"

extern struct variables
       {
       short l;
       short c;
       double *matrice;
       } *variable[MAXVAR];
//extern struct variables  *variable[MAXVAR];
extern char token[80];
extern char token_type;
extern short ligne;

short iswithe();
char get_token();
void serror();
struct variables *allocdyn();

/*    centrer et réduire un tableau     */

struct variables *exec_cent_red(resin)
struct variables *resin;

{
short nl,mc,i,j;
double *moy_cl,*var_cl;
struct variables *res;

nl = resin->l;
mc = resin->c;
if ( nl==0 || mc==0 )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }


/*  initialiser les variables */
moy_cl = (double *) calloc(mc,sizeof(double));
var_cl = (double *) calloc(mc,sizeof(double));
res = allocdyn(res,nl,mc);


/*  sommes des moyennes par colonne  */
for (j = 0; j < mc;j++)
    {
    *(moy_cl+j) = 0;
    for (i=0; i < nl; i++)
       *(moy_cl+j) += *(resin->matrice+i*mc+j) / nl;
    }
/* calcul des écarts_types sur les colonnes */

for (j = 0; j < mc;j++)
    {
    *(var_cl+j) = 0;
    for (i=0; i< nl; i++)
	*(var_cl+j) += (*(resin->matrice+i*mc+j) - *(moy_cl+j)) *
		       (*(resin->matrice+i*mc+j) - *(moy_cl+j)) / nl;
    *(var_cl+j) = sqrt(*(var_cl+j));
    }

/* calcul des valeurs centrées et réduites */

for (j = 0; j < mc;j++)
    {
    for (i=0; i< nl; i++)
	*(res->matrice+i*mc+j) =
	       (*(resin->matrice+i*mc+j) - *(moy_cl+j)) / *(var_cl+j);
    }

/*  désallocation  */
free(moy_cl);
free(var_cl);

/*  retour  */
return(res);

}
