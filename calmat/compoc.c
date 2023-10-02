/**********************************************************
 *  CALMAT  ver 2.0    sept 1989                          *
 *  source COMPOLG.C                                      *
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

short iswithe();
char get_token();
void serror();

/*    composantes principales     */
void exec_compo_cor_c()

{
short nl,mc,nv,mv,nval,mval,i,j,j1;
char var_o, var_v, var_val;
double ss;
double *sl,*sc;
double *c;
FILE *fp;

/*   la matrice des points colonnes supplémentaires  var_o nl x mc */
get_token();
var_o = toupper(*token) - 'A';
if (var_o > MAXVAR - 1 )
   {
   printf( "erreur de syntaxe !!" );
   serror();
   }
nl = variable[var_o]->l;
mc = variable[var_o]->c;
if ( nl==0 || mc==0 )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }


/*  les coordonnées propres des points lignes var_v nv x mv  */
get_token();
var_v = toupper(*token) - 'A';
if (var_v > MAXVAR - 1 )
   {
   printf( "erreur de syntaxe !!" );
   serror();
   }
nv = variable[var_v]->l;
mv = variable[var_v]->c;
if ( nv==0 || mv==0 )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }


/*  les valeurs propres var_val: nval x mval  */
get_token();
var_val = toupper(*token) - 'A';
if (var_val > MAXVAR - 1 )
   {
   printf( "erreur de syntaxe !!" );
   serror();
   }
nval = variable[var_val]->l;
mval = variable[var_val]->c;
if ( nval==0 || mval==0 )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }

/*  initialiser les totaux marginaux */
sl = (double *) calloc(nl,sizeof(double));
sc = (double *) calloc(mc,sizeof(double));
c = (double *) calloc(nl*nval,sizeof(double));

if ( sl == 0 || sc == 0 || c == 0)
   {
   printf("erreur de lecture des matrices !!!!");
   serror();
   }

/*  sommes des colonnes supplémentaires var_o  */
ss = 0;
for (j = 0; j < mc;j++)
    {
    *(sc+j) = 0;
    for (i=0; i < nl; i++)
       *(sc+j) += *(variable[var_o]->matrice+i*mc+j);
    ss += *(sc+j);
    }

/* calcul de la matrice des composantes */

for (j = 0; j < mc; j++)
    {
    for (j1 = 1; j1 < nval; j1++)
	{
	*(c+j*nval+j1) = 0;
	for (i = 0; (nv - nl + i) < nv; i++)
	    if ( *(variable[var_val]->matrice+j1*mval) != 0 )
	    *(c+j*nval+j1) += (1/sqrt(*(variable[var_val]->matrice+j1*mval) ) ) *
		    (*(variable[var_o]->matrice+i*mc+j) / *(sc+j)) *
		    (*(variable[var_v]->matrice+(nv-nl+i)*mv +j1-1));
	}
    }



/*  sauvegarde de la matrice des composantes  */
get_token();
fp = fopen(token,"wt");
if ( fp == NULL )
   {
   printf("Erreur d'ouverture du fichier des composantes principales !!");
   serror();
   }
printf("\n fichier des composantes principales (points lignes) :  %s ",token);
for ( j=0; j < mc ; j++)
   {
   for (j1 = 1; j1 < nval; j1++)
       fprintf(fp,"%1.14f  ",*(c+j*mc+j1));
   fprintf(fp,"\n");
   }
fclose(fp);


/*  désallocation  */
free(sl);
free(sc);
free(c);

/*  retour  */
return;

}
