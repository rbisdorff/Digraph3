/********************************************************
 *  CALMAT  ver 1.0    aout 1988                        *
 *  source LOADMAT.C                                    *
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

/*  chargement d'une matrice */
void exec_load()

{
FILE *fp;
short n,m,i,j,c,ci;
char var;
char buffer[BUFSIZ];
char temp[25], dn, eol_fp;

/*   fichier contenant la matrice à charger */
get_token();
if (strcmp(token,"con:") != 0)
    fp = fopen(token,"r");
else
    fp = stdin;

if (fp == NULL)
   {
   printf("Erreur d'ouverture du fichier %s à charger!!!\n",token);
   serror();
   };
printf("\n\nLecture de la matrice %s\n",token);

/*   identificateur de la variable */
get_token();
var = toupper(*token) - 'A';

/*  nombre de lignes de la matrice */
get_token();
if (token_type != NUMBER)
   {
   printf("erreur de syntaxe : load <fichier> <variable> n m  \n");
   serror();
   }
n = atoi(token);
if ( n < 1 )
   {
   printf("erreur de syntaxe : nombre de lignes incorrect !!! \n");
   serror();
   }

/*  nombre de colonnes de la matrice  */
get_token();
if (token_type != NUMBER)
   {
   printf("erreur de syntaxe : load <fichier> <variable> n m \n");
   serror();
   }
m= atoi(token);
if ( m < 1 )
   {
   printf("erreur de syntaxe : nombre de colonnes incorrect !!!\n");
   serror();
   }

if ( n*m > MAXELEM )
   {
   printf("erreur de dimension : nombre d'éléments trop élevé !!!\n");
   serror();
   }
/* allocation de la variable associée   */
variable[var] = allocdyn(variable[var],n,m);

/* lecture de la matrice */
i = 0;
j = 0;
dn = '\0';
eol_fp = '\0';
while ( (fgets(buffer, BUFSIZ, fp) != 0)  && (i < n) )
      {
      for (c = 0; (c < BUFSIZ) && (*(buffer+c) != '\0') && (j < m); c++)
	  {
	  if ( strchr("+-.0123456789eE",*(buffer+c)) )
	     {
	     if (dn == '\0')
		{
		dn = '\1';
		ci = 0;
		}
	     *(temp + ci++) = *(buffer+c);
	     }
	   else
	     {
	     if  (dn == '\1')
		{
		*(temp+ci) = '\0';
		*(variable[var]->matrice + i*m + j++) = atof(temp);
		dn = '\0';
		}
	     if (*(buffer+c) == '\n')
		eol_fp = '\1';

	     }
	  }
      if (eol_fp == '\1')
	 {
	 if ( j < m)
	    {
	    printf("Erreur de lecteur en ligne %d \n",i+1);
	    serror();
	    }
	 i++;
	 j = 0;
	 eol_fp = '\0';
	 }
       if ( (j == m) && (eol_fp != '\1'))
	  {
	  c--;        /* vérifier si la dernière ligne est complètement lue */
	  while ((c < BUFSIZ-1) && (*(buffer+c) != '\n'))  c++;
	  while (c == BUFSIZ -1)
	       {
	       if (fgets(buffer, BUFSIZ, fp) != 0)
		  {
		  for (c=0; c < BUFSIZ-1 && *(buffer+c) != '\n'; c++);
		  }
	       }
	  i++;
	  j = 0 ;
	  }
      }
/*  déconnexion du fichier  */
if (i < n )
   {
   printf("Erreur :  le fichier est trop court !!! \n");
   serror();
   }
if (fp != stdin)
   fclose(fp);
/* retour */
return;

}

/****************************************************/
/*    affichage d'une matrice     */
void exec_print()

{
short n,m,i,j;
char var;

get_token();
var = toupper(*token) - 'A';
if (var > MAXVAR - 1 )
   {
   printf( "erreur de syntaxe !!" );
   serror();
   }
if ( variable[var] == NULL )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }

n = variable[var]->l;
m = variable[var]->c;

printf("\nvariable-matrice:  %s[%d, %d] \n",token,n,m);

for (i=0; i<n; i=i+1)
    {
    printf("ligne %d \n",i);
    for (j=0; j<m; j=j+1)
	printf("element(%d, %d) : %f \n",i,j,*(variable[var]->matrice+i*m+j));
    printf("\n");
    }
}

/* sauvegarde d'une matrice    */
void exec_save()

{
short n,m,i,j;
char var;
FILE *fp;

get_token();
var = toupper(*token) - 'A';
if (var > MAXVAR - 1 )
   {
   printf( "erreur de syntaxe !!" );
   serror();
   }
if ( variable[var] == NULL )
   {
   printf("Erreur: matrice %s  non encore identifiée !! \n",token);
   serror();
   }
n = variable[var]->l;
m = variable[var]->c;
printf("\nsauvegarde de la variable-matrice %s[%d, %d]\n",token,n,m);
get_token();
printf("            sur le fichier %s  !!\n",token);
if (strcmp(token,"con:") == 0)
   fp = stdout;
else
     fp = fopen(token,"w");
if (fp == NULL)
   {
   printf("erreur d'ouverture du fichier %s !!!\n",token);
   exit(1);
   }

for (i=0; i<n; i++)
    {
    for (j=0; j<m; j++)
	fprintf(fp,"%f  ",*(variable[var]->matrice+i*m+j));
    fprintf(fp,"\n");
    }
if (fp != stdout)
   fclose(fp);
}
