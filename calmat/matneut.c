/********************************************************
 *  CALMAT  ver 2.3    septembre 1989                   *
 *  source MATNEUT.C                                   *
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

/*    allouer une matrice unitaire     */
struct variables *exec_matint()

{
short nl,mc,i,j;
struct variables *res;

get_token();
if (*token != '(')
   {
   printf("erreur: parenthèse ( manquante !!!");
   serror();
   }

get_token();
if (token_type != NUMBER )
   {
   printf("erreur: erreur de dimension de la matrice unitaire !!!");
   serror();
   }
nl = atoi(token);

get_token();
if (*token != ',' )
   {
   printf("erreur: virgule absente !!!");
   serror();
   }

get_token();
if (token_type != NUMBER )
   {
   printf("erreur: erreur de dimension de la matrice unitaire !!!");
   serror();
   }
mc = atoi(token);

if (nl*mc > MAXELEM)
   {
   printf("erreur:  trop d'éléments !!!");
   serror();
   }


/*  initialiser la variable */
res = allocdyn(res,nl,mc);


/* calcul des valeurs centrées et réduites */

for (i = 0; i < nl; i++)
    {
    for (j=0; j< mc; j++)
	*(res->matrice+i*mc+j) = 0;
    *(res->matrice+i*mc+i) = 1;
    }


/*  retour  */
return(res);

}

/*    allouer une matrice zéro     */
struct variables *exec_matzero()

{
short nl,mc,i,j;
struct variables *res;

get_token();
if (*token != '(')
   {
   printf("erreur: parenthèse ( manquante !!!");
   serror();
   }

get_token();
if (token_type != NUMBER )
   {
   printf("erreur: erreur de dimension de la matrice unitaire !!!");
   serror();
   }
nl = atoi(token);

get_token();
if (*token != ',')
   {
   printf("erreur: virgule manquante !!!");
   serror();
   }

get_token();
if (token_type != NUMBER )
   {
   printf("erreur: erreur de dimension de la matrice unitaire !!!");
   serror();
   }
mc = atoi(token);

if (nl*mc > MAXELEM)
   {
   printf("erreur:  trop d'éléments !!!");
   serror();
   }

get_token();
if (*token != ')')
   {
   printf("erreur: parenthèse ) manquante !!!");
   serror();
   }

/*  initialiser la variable */
res = allocdyn(res,nl,mc);


/* calcul des valeurs centres et rduites */

for (i = 0; i < nl; i++)
    {
    for (j=0; j< mc; j++)
	*(res->matrice+i*mc+j) = 0;
    }


/*  retour  */
return(res);

}
