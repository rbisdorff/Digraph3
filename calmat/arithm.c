/************************************************************
 *   CALMAT  ver 1.0                                        *
 *   recursive descent parser                               *
 *   source : ARITHM.C                                      *
 ************************************************************/

#include <math.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>

#include "calmat.h"

extern struct programmes
       {
       char car[PROG_SIZE];
       } *prog;
//extern struct programmes *prog;
extern short cour;
extern struct commands
       {
       char  command[20];
       char  tok;
       } table[];

extern char token[80];
extern char token_type;
extern char tok;
extern short varint;

extern struct variables
       {
       short l;
       short c;
       double *matrice;
       } *variable[MAXVAR];
//extern struct variables *variable[MAXVAR];
void serror();
struct variables *allocdyn();
void desallocdyn( );
double *dmax();
double *dmin();


/*  les fonctions arithmétiques sur les matrices  */

struct variables *arith( op, result, hold)
char op;
struct variables *result;
struct variables *hold;

{
short i,j,k;
struct variables *res;

switch(op)
   {
   case '+':
    printf(" En train de calculer une addition sur %d fois %d termes\n",result->l,result->c);
    if (!(result->l == hold->l && result->c == hold->c))
       {
       printf("Erreur de dimension des matrices !!\n");
       serror();
       }
    res = allocdyn(res,result->l,result->c);
    for(i=0; i<result->l; i=i+1)
       for(j=0; j < result->c; j=j+1)
	  *(res->matrice+i*res->c + j) = *(result->matrice+i*res->c + j) + *(hold->matrice+i*hold->c+j);
    desallocdyn(hold);
    break;

   case '-':
    if (!(result->l == hold->l && result->c == hold->c))
       {
       printf("Erreur de dimension des matrices !!\n");
       serror();
       }
    res = allocdyn(res,result->l,result->c);
    for(i=0; i<result->l; i=i+1)
       for(j=0; j < result->c; j=j+1)
	  *(res->matrice+i*res->c +j) = *(result->matrice+i*result->c +j) - *(hold->matrice+i*hold->c +j);
    desallocdyn(hold);
    break;

   case '|':    /* union ensembliste */
    if (!(result->l == hold->l && result->c == hold->c))
       {
       printf("Erreur de dimension des matrices !!\n");
       serror();
       }
    res = allocdyn(res,result->l,result->c);
    for(i=0; i<result->l; i=i+1)
       for(j=0; j < result->c; j++)
	  *(res->matrice+i*res->c +j) =
	      *dmax((result->matrice+i*result->c +j),(hold->matrice+i*hold->c +j));
    desallocdyn(hold);
    break;

   case '&':    /* intersection ensembliste */
    if (!(result->l == hold->l && result->c == hold->c))
       {
       printf("Erreur de dimension des matrices !!\n");
       serror();
       }
    res = allocdyn(res,result->l,result->c);
    for(i=0; i<result->l; i=i+1)
       for(j=0; j < result->c; j=j+1)
	  *(res->matrice+i*res->c +j) =
	      *dmin((result->matrice+i*result->c +j),(hold->matrice+i*hold->c +j));
    desallocdyn(hold);
    break;

   case '^': /* multiplication booléenne */
    if (!(result->c == hold->l))
       {
       printf("Erreur de dimension des matrices !!\n");
       serror();
       }
    res = allocdyn(res,result->l,hold->c);
    if (res->matrice == 0 )
       {
       printf(" erreur d'allocation de mémoire !!");
       serror();
       }
    for(i=0; i<result->l; i=i+1)
       for(j=0; j < hold->c; j=j+1)
          {
	  *(res->matrice+i*res->c +j) = 0;
          for (k=0; k<result->c;k++)
	      *(res->matrice+i*res->c +j) = *dmax( (res->matrice+i*res->c +j),
		   dmin( (result->matrice+i*result->c +k), (hold->matrice+k*hold->c +j) ) );
	  }
    desallocdyn(hold);
    break;

   case '*':  /* multiplication matricielle réelle */
    if (!(result->c == hold->l))
       {
       printf("Erreur de dimension des matrices !!\n");
       serror();
       }
    res = allocdyn(res,result->l,hold->c);
    if (res->matrice == 0 )
       {
       printf(" erreur d'allocation de mémoire !!");
       serror();
       }
    for(i=0; i<result->l; i=i+1)
       for(j=0; j < hold->c; j=j+1)
          {
	  *(res->matrice+i*res->c +j) = 0;
	  for (k=0; k<result->c ; k++)
	      *(res->matrice+i*res->c +j) = *(res->matrice+i*res->c +j)
		   + (*(result->matrice+i*result->c +k) * *(hold->matrice+k*hold->c +j));
	  }
    desallocdyn(hold);
    break;

   }
return(res);

}

/* transposition et complémentation  */
struct variables *unary( op, result)
char op;
struct variables *result;
{
short i,j;
struct variables *res;


switch(op)
   {
   case '`':
     res = allocdyn(res,result->c,result->l);
     for(i=0; i<result->c; i=i+1)
        for(j=0; j < result->l; j=j+1)
	   *(res->matrice+i*res->c +j) = *(result->matrice+j*result->c +i);
     desallocdyn(result);
     break;

   case '~': /* complémentation booléenne   */
     res = allocdyn(res,result->l,result->c);
     for(i=0; i <res->l; i++)
	for(j=0; j < result->c; j++)
	   if (*(result->matrice+i*result->c +j) > 0)
	    *(res->matrice+i*res->c +j) = 0;
	   else
	    *(res->matrice+i*res->c +j) = 1;
     desallocdyn(result);
     break;

   }

return(res);
}

struct variables *allocdyn(resin, l, c)
struct variables *resin;
short l;
short c;

{
long n;

    resin = (struct variables *) malloc(sizeof(struct variables));
    if (resin == 0 )
       {
       printf(" erreur d'allocation de mémoire !!");
       serror();
       }
    resin->l = l;
    resin->c = c;
    n = l * c;
    resin->matrice = (double *) calloc(n,sizeof(double));
    if (resin->matrice == 0 )
       {
       printf(" erreur d'allocation de mémoire !!");
       serror();
       }
    return(resin);
}

void desallocdyn(hold)
struct variables *hold;

{
short i;
for (i=0; variable[i] != hold && i < MAXVAR; i ++);
if (i == MAXVAR)
   {
   free(hold->matrice);
   free(hold);
   }
}

double *dmax( a, b)
double *a;
double *b;
 {
 if ( *a > *b )
    return a;
 else return b;
 }

double *dmin(a, b)
double *a;
double *b;
 {
 if ( *a < *b )
    return a;
 else return b;
 }

 struct variables *mult_scal(scalaire, result)
double scalaire;
struct variables *result;

{
short i,j;
struct variables *res;
res = allocdyn(res,result->c,result->l);
for(i=0; i<result->c; i=i+1)
   for(j=0; j < result->l; j=j+1)
     *(res->matrice+i*res->c +j) =
	 *(result->matrice+i*result->c +j) * scalaire;
desallocdyn(result);
return(res);
}
