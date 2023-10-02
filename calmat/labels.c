/************************************************************
 *   CALMAT  ver 2.3                                        *
 *   source : LABELS.C                                      *
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

extern struct labels
       {
       char name[LAB_LEN];
       short ptr;
       short ligne;
       } label_table[];
//extern struct labels label_table[];

/* déclaration des fonction */
char get_token();
void scan_labels();
void label_init();
void exec_goto();
short find_label();
void serror();

/*   édition du texte du programme et constitution de
     la table des labels */
void scan_labels()
{
short loc;

label_init();
loc = 0;
cour = 0;
ligne = 1;

printf("\n%d : ",ligne);
token_type = get_token();

while (tok != FINISHED)    /* \x1A (^Z) fin du fichier ASCII */
   {

   if ( tok == EOL )      /* EOL (\r) premier des deux caractères \r\n */
      {
      printf("\n");
      ligne++;
      printf("%d : ",ligne);
      }
   else
      printf("%s ",token);

   if ( token_type == LABEL )
      {
      strcpy(label_table[loc].name, token);
      label_table[loc].ptr = cour;
      label_table[loc++].ligne = ligne;
      }
   token_type = get_token();
   }
printf("%s \n",token);

cour = 0;     /* remise au début du texte pour le traitement proprement
		 dit  */
}

void label_init()    /* mise à zéro des lables */
{
short t;
for (t = 0; t < NUM_LAB; t++)
    label_table[t].name[0] = '\0';
}

void exec_goto()

{

get_token();
cour = find_label(token);
if (cour == -1 )
   {
   printf("Erreur: Branchement inexistant ou incorrect !!");
   serror();
   }
}

short find_label(s)
char *s;

{
short t;

for (t = 0; t < NUM_LAB; t++)
    if ( !strcmp(label_table[t].name, s))
       {
       ligne = label_table[t].ligne;
       return(label_table[t].ptr);
       }
return( -1 );  /* retour sans avoir trouver un branchement  */
}
