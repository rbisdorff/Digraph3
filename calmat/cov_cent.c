/********************************************************
 *  CALMAT  ver 2.0    juin 1989                        *
 *  source COV_CENT.C                                   *
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
       };
extern struct variables  *variable[MAXVAR];
extern char token[80];
extern char token_type;
extern short ligne;

short iswithe();
char get_token();
void serror();
struct variables *allocdyn();

/*    diagonalisation  d'une matrice     */
struct variables *exec_chi_deux(resin)
struct variables *resin;

{
short nl,mc,i,j,j1;
double *sl,*sc;
struct variables *res;

nl = resin->l;
mc = resin->c;
if ( nl==0 || mc==0 )
   {
   printf("Erreur: matrice %s  non encore identifie !! \n",token);
   serror();
   }


/*  initialiser les variables */
sl = (double *) calloc(nl,sizeof(double));
sc = (double *) calloc(mc,sizeof(double));
res = allocdyn(res,mc,mc);
res->l = mc;
res->c = mc;

/*  sommes des lignes  */
for (i = 0; i < nl;i++)
    {
    *(sl+i) = 0;
    for (j=0; j < mc; j++)
       *(sl+i) += *(resin->matrice+i*mc+j);
    }

/*  sommes des colonnes  */
for (j = 0; j < mc;j++)
    {
    *(sc+j) = 0;
    for (i=0; i < nl; i++)
       *(sc+j) += *(resin->matrice+i*mc+j);
    }
/* calcul de la matrice de distances chi_deux */

for (j = 0; j < mc;j++)
    {
    for (j1=0; j1 < mc; j1++)
	{
	*(res->matrice+j*mc+j1) = 0;
	for (i=0; i< nl; i++)
	*(res->matrice+j*mc+j1) += (*(resin->matrice+i*mc+j) *
			*(resin->matrice+i*mc+j1)) /
			( *(sl+i) * sqrt(*(sc+j)) * sqrt(*(sc + j1)) );
	}
    }

/*  dsallocation  */
free(sl);
free(sc);

/*  retour  */
return(res);

}
