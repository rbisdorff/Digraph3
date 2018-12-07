/************************************************************
 *   CALMAT  ver 2.3                                        *
 *   source : IFS.C                                         *
 ************************************************************/
#include <ctype.h>
#include <stdio.h>
#include <string.h>

#include "calmat.h"

extern struct programmes
       {
       char car[PROG_SIZE];
       } *prog;
//extern struct programmes *prog;      /* pointeur sur la source */
extern short cour;                   /* indice du caractre couranr */
extern char token[80];
extern char token_type;
extern char tok;
extern short ligne;

extern struct commands
       {
       char command[20];
       char tok;
       } com_table[];
extern struct functions
       {
       char function[20];
       char tok;
       } funct_table[];

extern struct variables
       {
       short l;
       short c;
       double *matrice;
       } *variable[MAXVAR];
//extern struct variables *variable[MAXVAR];


/* déclaration des fonctions */
char get_token();
struct variables *get_exp();
void serror(), desallocdyn();
short mat_comp();

void exec_if()

{
struct variables *expr_g;
struct variables *expr_d;
char op;
short cond;

expr_g = get_exp();
get_token();
if (!strchr("=<>",*token) )
   {
   printf("erreur: opérateur logique non valide !!");
   serror();
   }
op = *token;
expr_d = get_exp();
cond = mat_comp(expr_g, expr_d, op);
desallocdyn(expr_g);
desallocdyn(expr_d);
if (!cond)
   {
   do  {
       get_token();
       }  while (tok != ENDIF && tok != FINISHED);
   if (tok == FINISHED)
      {
      printf("erreur: IF sans ENDIF !!!");
      serror();
      }
   }
}


short mat_comp(expr_g, expr_d, op)
struct variables *expr_g;
struct variables *expr_d;
char op;

{
short i,j;
short cond, equal;

if ( (expr_g->l != expr_d->l) || (expr_g->c != expr_d->c))
   {
   printf("Erreur: dimension des matrices non identiques !!");
   serror();
   }
cond = 1;
equal = 1;
switch(op)
      {
      case '=':
	for( i =0; i < expr_g->l && cond != 0; i++)
	   for ( j = 0; j < expr_g->c && cond != 0; j++)
	       if ( *(expr_g->matrice+i*expr_g->c+j) != *(expr_d->matrice+i*expr_d->c+j) )
		  cond = 0;
	break;
      case '>':
	for( i =0; i < expr_g->l && cond != 0; i++)
	   for ( j = 0; j < expr_g->c && cond != 0; j++)
	       {
	       if ( *(expr_g->matrice+i*expr_g->c+j) < *(expr_d->matrice+i*expr_d->c+j) )
		  cond = 0;
	       if ( *(expr_g->matrice+i*expr_g->c+j) > *(expr_d->matrice+i*expr_d->c+j) )
		  equal = 0;
	       }
	if (equal != 0)
	   cond = 0;
	break;
      case '<':
	for( i =0; i < expr_g->l && cond != 0; i++)
	   for ( j = 0; j < expr_g->c && cond != 0; j++)
	       {
	       if ( *(expr_g->matrice+i*expr_g->c+j) > *(expr_d->matrice+i*expr_d->c+j) )
		  cond = 0;
	       if ( *(expr_g->matrice+i*expr_g->c+j) < *(expr_d->matrice+i*expr_d->c+j) )
		  equal = 0;
	       }
	if (equal != 0)
	   cond = 0;
break;
      }
return(cond);
}
