/********************************************************
 *  CALMAT  ver 1.0    aout 1988                        *
 *  source COMPO.C                                      *
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
void exec_compo_cor()

{
short nl,mc,nv,mv,nval,mval,i,j,j1;
char var_o, var_v, var_val;
double ss,contabs, contrel, contrel_d, inertie, inertie_cum;
double *sl,*sc;
double *c;
FILE *fp;

/*   la matrice originale   */
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


/*  les vecteurs propres   */
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


/*  les valeurs propres   */
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

/*  affichage des valeurs propres */
inertie =0;
for (j1 = 1; j1 <nval; j1++)
    inertie += *(variable[var_val]->matrice+j1*mval);
printf("\n  Inertie expliquée\n");
for (j1=1; j1 < nval; j1++)
    {
    inertie_cum = 0;
    for (j=1; j <= j1; j++)
	inertie_cum += *(variable[var_val]->matrice+j*mval);
    printf("  axe %d :  %1.3f  %1.3f \n",j1, *(variable[var_val]->matrice+j1*mval)/inertie ,
	    inertie_cum/inertie );
    }

/*  initialiser les variables */
sl = (double *) calloc(nl,sizeof(double));
sc = (double *) calloc(mc,sizeof(double));
c = (double *) calloc((nl+mc)*nv,sizeof(double));

if ( sl == 0 || sc == 0 || c == 0)
   {
   printf("erreur de lecture des matrices !!!!");
   serror();
   }

/*  sommes des lignes  */
ss = 0;
for (i = 0; i < nl;i++)
    {
    *(sl+i) = 0;
    for (j=0; j < mc; j++)
       *(sl+i) += *(variable[var_o]->matrice+i*mc+j);
    ss += *(sl+i);
    }

/*  sommes des colonnes  */
for (j = 0; j < mc;j++)
    {
    *(sc+j) = 0;
    for (i=0; i < nl; i++)
       *(sc+j) += *(variable[var_o]->matrice+i*mc+j);
    }

/* calcul de la matrice des composantes */

for (j = 0; j < mc;j++)
    {
    for (j1 = 0; j1 < nval; j1++)
    if (*(variable[var_val]->matrice+j1*mval) != 0 )
    *(c+j*mc+j1) = sqrt(*(variable[var_val]->matrice+j1*mval)) *
		   sqrt( ss / *(sc+j)) * *(variable[var_v]->matrice+j1*mv+j);
    }

for (i = 0+mc; i < nl+mc;i++)
    {
    for (j1 = 0; j1 < nval; j1++)
	{
	*(c+i*mc+j1) = 0;
	for (j = 0; j < mc; j++)
	    if ( *(variable[var_val]->matrice+j1*mval) != 0 )
	    *(c+i*nval+j1) += (1/sqrt(*(variable[var_val]->matrice+j1*mval) ) ) *
		    (*(variable[var_o]->matrice+(i-mc)*mc+j) / *(sl+(i-mc))) *
		    *(c + j*mc +j1);
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
printf("\n fichier des composantes principales:  %s ",token);
for ( j=0; j < nl+mc ; j++)
   {
   for (j1 = 1; j1 < nval; j1++)
       fprintf(fp,"%1.14f  ",*(c+j*mc+j1));
   fprintf(fp,"\n");
   }
fclose(fp);

/* calcul des contributions absolues */

get_token();
fp = fopen(token,"wt");
if ( fp == NULL )
   {
   printf("\n!!! Erreur d'ouverture du fichier des contributions absolues !!");
   serror();
   }
printf("\n  matrice des contributions absolues  %s ",token);
for (j = 0; j < mc;j++)
    {
    for (j1 = 1; j1 < nval; j1++)
	{
	if ( *(variable[var_val]->matrice+j1*mval) != 0)
	contabs = (*(sc+j) / ss) * (*(c+j*mc+j1) * *(c+j*mc+j1)) /
			      *(variable[var_val]->matrice+j1*mval) ;
	else contabs =0;
	fprintf(fp,"%1.4f  ",contabs);
	}
    fprintf(fp,"\n");
    }

for (i = 0; i < nl; i++)
    {
    for (j1 = 1; j1 < nval; j1++)
	{
	if (*(variable[var_val]->matrice+j1*mval) != 0 )
	   contabs = (*(sl+i) / ss) * (*(c+(i+mc)*mc+j1) * *(c+(i+mc)*mc+j1)) /
			      *(variable[var_val]->matrice+j1*mval) ;
	else
	   contabs = 0;
	fprintf(fp,"%1.4f  ",contabs);
	}
    fprintf(fp,"\n");
    }
fclose(fp);

/* calcul des contributions relatives */
get_token();
fp = fopen(token,"wt");
if ( fp == NULL )
   {
   printf("\n !!!! Erreur d'ouverture du fichier des contributions relatives !!");
   serror();
   }
printf("\n  matrice des contributions relatives %s ",token);
for (j = 0; j < mc;j++)
    {
    contrel_d = 0;
    for ( i=0; i< nl; i++)
	contrel_d += (ss / *(sl+i)) * (*(variable[var_o]->matrice+i*mc+j)/ *(sc+j) - *(sl+i)/ss)
			* (*(variable[var_o]->matrice+i*mc+j)/ *(sc+j) - *(sl+i)/ss);
    for (j1 = 1; j1 < nval; j1++)
	{
	contrel =  (*(c+j*mc+j1) * *(c+j*mc+j1)) / contrel_d;
	fprintf(fp,"%1.4f  ",contrel);
	}
    fprintf(fp,"\n");
    }

for (i = 0; i < nl;i++)
    {
    contrel_d = 0;
    for ( j=0 ; j < mc; j++)
	contrel_d += (ss / *(sc+j)) * (*(variable[var_o]->matrice+i*mc+j)/ *(sl+i) - *(sc+j)/ss) *
	    (*(variable[var_o]->matrice+i*mc+j)/ *(sl+i) - *(sc+j)/ss);
    for (j1 = 1; j1 < nval; j1++)
	{
	contrel =  (*(c+(i+mc)*mc+j1) * *(c+(i+mc)*mc+j1)) / contrel_d;
	fprintf(fp,"%1.4f  ",contrel);
	}
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
