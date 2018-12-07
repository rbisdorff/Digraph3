/********************************************************
 *  CALMAT  ver 2.0    juin 1989                        *
 *  source PROFIL.C                                   *
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

struct variables *exec_cprofil(resin)
struct variables *resin;

{
short nl,mc,i,j;
double *som_cl;
struct variables *res;

nl = resin->l;
mc = resin->c;
if ( nl==0 || mc==0 )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }


/*  initialiser les variables */
som_cl = (double *) calloc(mc,sizeof(double));
res = allocdyn(res,nl,mc);


/*  sommes  par colonne  */
for (j = 0; j < mc;j++)
    {
    *(som_cl+j) = 0;
    for (i=0; i < nl; i++)
       *(som_cl+j) += *(resin->matrice+i*mc+j);
    }

/* calcul des profils par colonne */

for (j = 0; j < mc;j++)
    {
    for (i=0; i< nl; i++)
	*(res->matrice+i*mc+j) =
	       (*(resin->matrice+i*mc+j) / *(som_cl+j));
    }

/*  désallocation  */
free(som_cl);

/*  retour  */
return(res);

}
