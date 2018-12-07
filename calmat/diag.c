/********************************************************
 *  CALMAT  ver 1.0    aout 1988                        *
 *  source DIAG.C                                       *
 ********************************************************/
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#include "calmat.h"

#define MAX_ITER  100
#define MAX_PRECISION 1e-10

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

/*    diagonalisation  d'une matrice     */
void exec_tridiag()

{
short nl,mc,i,j;
short i2,m,m1,l,k,is,ij,jk,ijk;
char var;
double ab,b,bp,c,ep,h,q,t,u,v,ix,x,xp,trace;
double *s,*d;
double *w;
FILE *fp;

get_token();
var = toupper(*token) - 'A';
if (var > MAXVAR - 1 )
   {
   printf( "erreur de syntaxe !!" );
   serror();
   }
nl = variable[var]->l;
mc = variable[var]->c;
if ( nl==0 || mc==0 )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }
if ( nl != mc )
   {
   printf("Erreur: matrice %s non carrée !! \n",token);
   serror();
   }


/*  initialiser les variables */
s = (double *) calloc(mc+1,sizeof(double));
d = (double *) calloc(mc+1,sizeof(double));
w = (double *) calloc((mc+1)*(mc+1),sizeof(double));

/* déplacer la matrice sur w  */
trace = 0;
for (i = 0; i < mc;i++)
    {
    trace += *(variable[var]->matrice+i*mc+i);
    for (j=0; j < mc; j++)
       *(w+(i+1)*mc+(j+1)) = *(variable[var]->matrice+i*mc+j);
    }

if ( mc == 1)
   {
   printf("matrice à 1 élément !!!");
   goto suite_1a;
   }
else
   {
   printf("\n !!! tridiagonalisation !!!!");
   }

for (i2 = 2; i2 <= mc; i2++)
    {
    b = 0; c = 0; i = mc - i2 + 2; k = i - 1;
    if ( k < 2 )
       goto suite_1;
    for ( l = 1; l <= k; l++)
       c = c + fabs(*(w+i*mc+l));
    if ( c != 0 )
       goto suite_2 ;

    suite_1:
     *(s+i) = *(w+i*mc+k);
     goto suite_3;

    suite_2:
     for (l =1; l<=k; l++)
	 {
	 x = *(w+i*mc+l) / c;
	 *(w+i*mc+l) = x;
	 b = b + x * x;
	 }
    xp = *(w+i*mc+k);
    ix = 1;
    if ( xp < 0)
       ix = -1;
    q = - sqrt(b) * ix;
    *(s+i) = c * q;
    b = b - xp*q;
    *(w+i*mc+k) = xp - q;
    xp = 0;
    for ( m = 1; m <=k; m++)
	{
	*(w+m*mc+i) = *(w+i*mc+m)/b/c;
	q = 0;
	for ( l = 1; l <= m; l++)
	    q = q + *(w+m*mc+l) * *(w+i*mc+l);
	m1 = m + 1;
	if ( k < m1)
	   goto suite_4;
	for ( l = m1; l <= k; l++)
	    q = q + *(w+l*mc+m) * *(w+i*mc+l);
	suite_4:
	*(s+m) = q / b;
	xp = xp + *(s+m) * *(w+i*mc+m);
	}
    bp = xp * 0.5/b;
    for (m = 1; m <= k; m++)
	{
	xp = *(w+i*mc+m);
	q = *(s+m) - bp*xp;
	*(s+m) = q;
	for (l= 1; l<=m; l++)
	    *(w+m*mc+l) = *(w+m*mc+l) - (xp * *(s+l) + q * *(w+i*mc+l));
	}
    for ( l=1; l <=k; l++)
	*(w+i*mc+l) = *(w+i*mc+l) * c;
    suite_3:
    *(d+i) = b;
    }
suite_1a:
*(s+1) = 0;
*(d+1) = 0;
for ( i = 1; i <= mc; i++)
    {
    k = i - 1;
    if (*(d+i) == 0)
       goto suite_5;
    for ( m = 1; m <= k; m++ )
	{
	q = 0;
	for (l = 1; l <= k; l++)
	    q = q + *(w+i*mc+l) * *(w+l*mc+m);
	for (l = 1; l <= k; l++)
	*(w+l*mc+m) = *(w+l*mc+m) - q * *(w+l*mc+i);
	}
    suite_5:
    *(d+i) = *(w+i*mc+i);
    *(w+i*mc+i) =1;
    if ( k >= 1)
       {
       for ( m=1; m <=k; m++)
	   {
	   *(w+i*mc+m) = 0;
	   *(w+m*mc+i) = 0;
	   }
       }
    }
/*   diagonalisation   */
if (mc == 1)
   return;
printf("\n !!!! diagonalisation !!!!");
for (i = 2; i <= mc; i++)
    *(s+i-1) = *(s+i);
*(s+mc) = 0;
for (k = 1; k <= mc; k++)
    {
    m = 0;
    printf("\nvaleur propre : %d \n",k);
    suite_9:
    for ( j = k; j <= mc ; j++)
	{
	   if (j==mc)
	      goto suite_6;
	   ab = fabs(*(s+j));
	   ep = MAX_PRECISION * (fabs(*(d+j)) + fabs(*(d+j+1)));
	   if ( ab < ep )
	      goto suite_6;
	}
    suite_6:
    is = 1;
    h = *(d+k);
    if (j == k)
       goto suite_7;
    printf("itération : %d ",m);
    if (m > MAX_ITER)
	{
	printf("Nombre maximal d'itérations prévues !!!");
	serror();
	}
    m++;
    q = ( *(d+k+1) - h) * 0.5 / *(s+k);
    t = sqrt(q*q+1);
    if (q < 0 )
       is = -1;
    q = *(d+j) - h + *(s+k)/(q + t*is);
    u = 1; v= 1;
    h = 0;
    jk = j-k;
    for (ijk = 1; ijk <= jk; ijk++)
	{
	i = j - ijk;
	xp = u * *(s+i);
	b = v * *(s+i);
	if ( fabs(xp) >= fabs(q) )
	   {
	   u = xp/q;
	   t = sqrt(u*u+1);
	   *(s+i+1) = q * t;
	   v = 1/t;
	   u *= v;
	   }
	else
	   {
	   v = q/xp;
	   t = sqrt(1 + v*v);
	   *(s+i+1) = t * xp;
	   u = 1/t;
	   v *= u;
	   }
	q = *(d+i+1) - h;
	t = (*(d+i) -q)*u + 2*v*b;
	h = u*t;
	*(d+i+1) = q+h;
	q = v*t-b;
	for (l = 1; l <= mc; l++)
	    {
	    xp = *(w+l*mc+i+1);
	    *(w+l*mc+i+1) = *(w+l*mc+i) * u + v *xp;
	    *(w+l*mc+i) = v * *(w+l*mc+i) - u*xp;
	    }
	}
    *(d+k) -= h;
    *(s+k) = q;
    *(s+j) = 0;
    goto suite_9;
    suite_7:;
    }
for (ij = 2; ij <= mc; ij++)
    {
    i = ij -1;
    l = i;
    h = *(d+i);
    for ( m = ij; m <= mc; m ++)
	{
	if ( *(d+m) >= h)
	   {
	   l = m;
	   h = *(d+m);
	   }
	}
    if ( l != i)
       {
       *(d+l) = *(d+i);
       *(d+i) = h;
       for (m = 1; m <= mc; m++)
	   {
	   h = *(w+m*mc+i);
	   *(w+m*mc+i) = *(w+m*mc+l);
	   *(w+m*mc+l) = h;
	   }
       }
    }

/*  procédures de sauvegarde  */
get_token();

fp = fopen(token,"wt");
if ( fp == NULL )
   {
   printf("\n!!!! Erreur d'ouverture du fichier des valeurs propres !!");
   serror();
   }
printf("\n %d  valeurs propres sur %s ", mc, token);
for (i = 1; i <= mc; i++)
   if (trace < 0)
      { 
      fprintf(fp,"%1.14g  %1.3g \n",*(d+i), *(d+i)/(trace-*(d+1))); 
      }
   else
      {
      fprintf(fp,"%1.14g  %1.3g \n",*(d+i), *(d+i)/trace);
      }
fclose(fp);

get_token();
fp = fopen(token,"w");
if ( fp == NULL )
   {
   printf("\n!!! Erreur d'ouverture du fichier des vecteurs propres !!");
   serror();
   }
printf("\n %d  vecteurs propres sur %s ", mc, token);
for ( i=1; i <= mc ; i++)
   {
   for (j=1; j <= mc; j++)
       fprintf(fp,"%1.14g  ",*(w+i*mc+j));
   fprintf(fp,"\n");
   }
fclose(fp);

/*  désallocation  */
free(s);
free(d);
free(w);

/*  retour  */
return;

}
