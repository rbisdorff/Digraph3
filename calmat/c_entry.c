/*************************************************************
 * LAUMIE 1990   R.B.  septembre                             *
 * INTERPRETE DE CALCULS MATRICIELS  CALMAT version 4.0 Unix *
 * SOURCE : C_ENTRY_C                                        *
 *************************************************************/

#include <stdio.h>
#include <setjmp.h>
#include <math.h>
#include <ctype.h>
#include <stdlib.h>

#include "calmat.h"

jmp_buf e_buf; /* environnement pour long jump on error */

struct programmes
       {
       char car[PROG_SIZE];
       }programme; /* texte du programme */

struct programmes *prog; /* pointeur sur l'expression à analyser */
short cour; /* indice du caractère courant */
short ligne_cour;   /* indice du début de la ligne courante */
short param; /*nombre de paramètres */
char *parv[NUM_PAR];  /* valeurs des paramètres */

struct variables
       {
       short l; /* nombre de lignes */
       short c; /* nombre de colonnes */
       double *matrice;  /* matrice associée à la variable */
       } *variable[MAXVAR];
//struct variables *variable[MAXVAR];       /* MAXVAR variables sont prévues  */

struct commands
   {
   char command[20];
   char tok;
   } com_table[] =
        {
	"load", LOAD,
        "save", SAVE,
        "print", PRINT,
	"tridiag", TRIDIAG,
	"compocor", COMPO_COR,
	"composupp",COMPO_L_SUPP,
	"compocsupp", COMPO_C_SUPP,
	"goto",GOTO,
	"rem",REMARK,
	"end", END,
	"if",IF,
	"endif",ENDIF,
	"while",WHILE,
	"endwhile",ENDWHILE,
	"", END  /* fin de la table des commandes */
        };
struct functions
   {
   char function[20];
   char tok;
   } funct_table[] =
        {
	"chi_deux", CHI_DEUX,
	"dist_fact", DIST_FACT,
	"inv_sym",INV_SYM,
	"cent_red",CENT_RED,
	"matint",MATINT,
	"matzero",MATZERO,
	"cprofil", CPROFIL,
	"", END  /* fin de la table des fonctions */
        };

struct labels
       {
       char name[LAB_LEN];
       short ptr;
       short ligne;
       } label_table[NUM_LAB];

struct while_stack
       {
       short element;
       short ligne;
       } wh_stack[NUM_WHILE];
short wh_top;

char token[80];
char token_type, tok;
short ligne;


/**********************************/
void exec_remark(), exec_load(), exec_save(), exec_print(),
     exec_input(), exec_tridiag(), exec_compo_cor_lg(),
     exec_compo_cor(),exec_compo_cor_c(), exec_goto(), exec_if(), exec_while(),
     exec_endwhile();
extern void putback(), affectation();
short load_program();
void scan_labels();
char get_token();

/**********************************/
int main(argc, argv)
short argc;
char *argv[];


{
short i;

printf("\n  CALMAT  interprète de calculs matriciels      ");
printf("\n       version 5.0 UTF8 gcc Linux              ");
printf("\n        Université du Luxembourg               ");
printf("\n  (c) R.Bisdorff 2008 $Revision: 1.5 $\n\n");

if(argc < 2)
   {
   printf("\n   Le mode d'emploi de l'interprète est illustré dans");
   printf("\n          le texte d'aide calmat.hlp !!                  ");
   printf("\n      Pour consulter ce texte entrez la commande: ");
   printf("\n           ...$less calmat.hlp \n\n\n"); 
   exit(1);
   }
/* transfert des paramètres  */
param = argc;
for ( i = 1; i <= param && i < NUM_PAR; i++)
    parv[i-1] = argv[i];



/* chargement de la source dans la mémoire */

if (!load_program(&programme,parv[0]))
   {
   printf(" erreur de chargement de la source à traiter \n");
   exit(3);
   }

/* initialisation de la sortie par erreur */
if (setjmp(e_buf)) exit(1);

/* initialisation de la table des labels */
prog = &programme;
scan_labels();

/* initialisation de la pile des while */
wh_top = 0;

/* début du traitement */
ligne = 1;
ligne_cour = cour;
do
   {
   token_type = get_token();
   if (tok == EOL )
      {
      ligne++;
      ligne_cour = cour;
      }
   if (token_type == VARIABLE )
      {
      putback();
      affectation();
      ligne++;
      }
   else
      {
      switch(tok)
	{
	case REMARK:
	  exec_remark();
	  break;
        case LOAD:
	  exec_load();
          break;
	case SAVE:
          exec_save();
          break;
        case PRINT:
          exec_print();
          break;
	case TRIDIAG:
	  exec_tridiag();
	  break;
	case COMPO_COR:
	  exec_compo_cor();
	  break;
	case COMPO_L_SUPP:
	  exec_compo_cor_lg();
	  break;
	case COMPO_C_SUPP:
	  exec_compo_cor_c();
          break;
	case GOTO:
	  exec_goto();
	  break;
	case IF:
	  exec_if();
	  break;
	case WHILE:
	  exec_while();
	  break;
	case ENDWHILE:
	  exec_endwhile();
	  break;
	case END:
	  printf("\nfin de la source !!!\n  à la ligne:%d \n",ligne);
          exit(0);
          break;
        }
      }
   } while (tok != FINISHED);
return(0);
}

/* routine de sortie par erreur */
void serror()
{
printf("\n  -------->>>  %d : ",ligne);
cour = ligne_cour;
get_token();
while (tok != EOL )  
  {
  printf("%s ",token);
  get_token();
  }     

printf("\n\n   (la syntaxe est documentée dans le fichier CALMAT.HLP)\n");
longjmp(e_buf,1);
}

/* routine d'impression d'un commentaire */
void exec_remark()
{
get_token();
if (token_type == QUOTE)
  printf("\n%s",token);

while (tok != EOL)
  {
  get_token();
  }
ligne++;
}

