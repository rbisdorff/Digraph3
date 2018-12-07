/************************************************************
 *   CALMAT  ver 2.3                                        *
 *   source : WHILE.C                                       *
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
extern short cour;                   /* indice du caractère courant */
extern char token[80];
extern char token_type;
extern char tok;
extern short ligne;

extern struct variables
       {
       short l;
       short c;
       double *matrice;
       } *variable[MAXVAR];
//extern struct variables *variable[MAXVAR];

extern struct while_stack
	{
	short element;
	short ligne;
	} wh_stack[NUM_WHILE];
extern short wh_top;

/* déclaration des fonctions */
char get_token();
struct variables *get_exp();
void serror(), putback(), desallocdyn();
short mat_comp();
void push_while();
short pop_while();


void exec_while()

{
struct variables *expr_g;
struct variables *expr_d;
char op;
short cond;

putback();
push_while(cour);
get_token();

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
       }  while (tok != ENDWHILE && tok != FINISHED);
   if (tok == FINISHED)
      {
      printf("erreur: WHILE sans ENDWHILE !!!");
      serror();
      }
   wh_top--;
   }
}


void push_while(p)
short p;

{
if (wh_top < NUM_WHILE -1)
   {
   wh_stack[wh_top].ligne = ligne;
   wh_stack[wh_top++].element = p;
   }
else
   {
   printf("Erreur:  while_stack overflow !!!");
   serror();
   }
}

short pop_while()

{
if (--wh_top >= 0)
   {
   ligne = wh_stack[wh_top].ligne;
   return(wh_stack[wh_top].element);
   }
else
   {
   printf("Erreur:  ENDWHILE sans WHILE !!!");
   serror();
   }
}

void exec_endwhile()

{

cour = pop_while();

}
