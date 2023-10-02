/********************************************************
 *  CALMAT  ver 1.0    aout 1988                        *
 *  source DIST_FACT.C                                  *
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

/*    préparartion d'u tableau de distances    */
struct variables *exec_dist_fact(resin)
struct variables *resin;

{
short nl,mc,i,j;
double *sl,*sc,ss;
struct variables  *res;

nl = resin->l;
mc = resin->c;
if ( nl==0 || mc==0 )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }


/*  initialiser les variables */
sl = (double *) calloc(nl,sizeof(double));
sc = (double *) calloc(mc,sizeof(double));
res = allocdyn(res,nl,mc);
res->l = nl;
res->c = mc;


/*  sommes des lignes  */
ss = 0;
for (i = 0; i < nl;i++)
    {
    *(sl+i) = 0;
    for (j=0; j < mc; j++)
       *(sl+i) += *(resin->matrice+i*mc+j) / mc;
    ss += *(sl+i) / nl;
    }

/*  sommes des colonnes  */
for (j = 0; j < mc;j++)
    {
    *(sc+j) = 0;
    for (i=0; i < nl; i++)
       *(sc+j) += *(resin->matrice+i*mc+j) / mc;
    }
/* calcul de la matrice de distances  */

for (i = 0; i < nl; i++)
    for (j=0; j < mc; j++)
	*(res->matrice+i*mc+j) = -(0.5) * (*(resin->matrice+i*mc+j) -( *(sl+i)
			+ *(sc+j)) + ss);

/*  désallocation  */
free(sl);
free(sc);

/*  retour  */
return(res);

}
