/********************************************************
 *  CALMAT  ver 2.0    juin 1989                        *
 *  source INV_SYM.C                                    *
 ********************************************************/
#include "stdio.h"
#include "math.h"
#include "alloc.h"
#include "ctype.h"
#include "stdlib.h"
#include "string.h"

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
struct variables *allocdyn(struct variables *resin, short l, short c);

/*    inversion  d'une matrice symtrique    */
struct variables *exec_inv_sym(struct variables *resin)

{
short nl, n1, mc, i, j, k, i1;
struct variables *res;
double x, x1;

nl = resin->l;
mc = resin->c;

if ( nl==0 || mc==0 )
   {
   printf("Erreur: matrice %s  non encore identifie !! \n",token);
   serror();
   }
if ( nl != mc )
   {
   printf("Erreur: matrice %s  non carre !! \n",token);
   serror();
   }


/*  initialiser les variables */
res = allocdyn(res,mc,mc);

n1 = nl - 1;

/*  transfrer les valeurs de la matrice initaile  */
for (i = 0; i < nl; i++)
    for (j = 0; j <=i; j++)
	*(res->matrice+j*mc+i) = *(resin->matrice+j*mc+i);


if ( nl == 1)
   {
   *(res->matrice) = 1 / *(res->matrice);
   }

else
   {

   /* factorisation de choleski */

   x = sqrt(*(res->matrice));
   for (i = 0; i < nl;i++)
       *(res->matrice+i*mc) = *(res->matrice+i) / x;
   if ( n1 != 1)
      {
      for (i = 1; i < n1; i++)
	  {
	  i1 = i-1;
	  x = 0;
	  for (k = 0; k <= i1; k++)
	      x += *(res->matrice+i*mc+k) * *(res->matrice+i*mc+k);
	  x = sqrt(*(res->matrice+i*mc+i) - x);
	  *(res->matrice+i*mc+i) = x;
	  for (j=i+1; j<nl; j++)
	      {
	      x1 = 0;
	      for (k = 0; k < i1; k++)
		  x1 += *(res->matrice+i*mc+k) * *(res->matrice+j*mc+k);
	      *(res->matrice+j*mc+i) = *(res->matrice+i*mc+j) / x -  x1 / x;
	      }
	  }
      }
   x = 0;
   for (k = 0; k<nl; k++)
       x += *(res->matrice+(nl-1)*mc+k) * *(res->matrice+(nl-1)*mc+k) ;
   *(res->matrice+(nl-1)*mc+(mc-1)) = sqrt(*(res->matrice+(nl-1)*mc+(mc-1))  - x);

   /*  inversion de la matrice triangulaire  */
   *(res->matrice)  = 1 / *(res->matrice);
   for ( i = 1; i < nl; i++)
       {
       i1 = i - 1;
       *(res->matrice+i*mc+i)  = 1 / *(res->matrice+i*mc+i);
       for ( j = 0 ; j < i1; j++)
	   {
	   x = 0;
	   for ( k = j; k < i1; k++)
	       x += *(res->matrice+i*mc+k) * *(res->matrice+k*mc+j);
	   *(res->matrice+i*mc+j) = -(x) * *(res->matrice+i*mc+i);
	   }
       }
    /*  inverse de la matrice initiale dans la moiti infreure */
    for ( i = 0; i <nl; i++)
	{
	for (j = 0; j < mc; j++)
	    {
	    x = 0;
	    for (k = i; k <nl; k++)
		x += *(res->matrice+k*mc+i) * *(res->matrice+k*mc+j);
	    *(res->matrice+j*mc+i) = x;
	    }
	}
   }


/*  retour  */
return(res);

}
