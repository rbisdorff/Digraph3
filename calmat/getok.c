/************************************************************
 *   CALMAT  ver 3.0                                        *
 *   recursive descent parser                               *
 *   source : GETOK.C                                      *
 ************************************************************/
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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
extern short param;
extern char *parv[NUM_PAR];

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
extern  short argc;
extern  char *argv[];

/* déclaration des fonctions */
char get_token();
char com_look_up();
char funct_look_up();
short isdelim();
short iswithe();
void putback(), serror();


/*  cette fonction détermine le prochain mot de la source  */
char get_token()

{
char *temp;
short i,k;

token_type = 0;
tok = 0;
temp = token ;

if ( prog->car[cour] == '\0' || prog->car[cour] ==  EOF)
   {
   *token = 0;
   tok = FINISHED;
   return(token_type = DELIMITER);
   }

while (iswithe(prog->car[cour]))
     ++cour;

if (prog->car[cour] == '\n')
   {
    ++cour;
    if (prog->car[cour] != EOF)
       {
       tok = EOL;
       *token = '\n';
       return (token_type = DELIMITER );
       }
    else
       {
       tok = FINISHED;
       return (token_type = DELIMITER );
       }
    };

if (strchr(":", prog->car[cour]) )
   {
   cour++;
   i=0;
   while (!isdelim(prog->car[cour])) temp[i++] = prog->car[cour++];
   temp[i] = '\0';
   return (token_type = LABEL);
   }


if (strchr("<>=+-*`~&^|(),", prog->car[cour]) )
   {
   i = 0;
   temp[i] = prog->car[cour];
   cour ++;
   i ++;
   temp[i] = 0;
   return (token_type = DELIMITER );
   };

if (prog->car[cour] == '"')
   {
   cour++;
   i=0;
   while (prog->car[cour]  != '"' && prog->car[cour] != '\n')
	 temp[i++] = prog->car[cour++];
   if ((prog->car[cour] == '\n' )&& (prog->car[cour-1] != '"'))
      printf("constante texte non fermée !!");
   temp[i] = 0;
   return (token_type = QUOTE);
   } ;

if (strchr("%", prog->car[cour]) )
   {
   cour++;
   if (!isdigit(prog->car[cour]))
      {
      printf("erreur:  paramêtre incorrecte !!!");
      serror();
      }
   i=atoi((prog->car+cour++));
   if (i >= param-1)
      temp[0] = '\0';
   else
      {
      k = 0;
      while (*(parv[i] + k) != '\0')
	    *temp++ = *(parv[i] + k++);
      *temp = '\0';
      }
   if ( isalpha(*(parv[i]))  )
      {
      token_type = STRING;
      }
   else
      {
      *temp = '\0';
      return (token_type = NUMBER);
      }
   }


if (isdigit(prog->car[cour]))
   {
   while (!isdelim(prog->car[cour])) *temp++ = prog->car[cour++];
   *temp = '\0';
   return (token_type = NUMBER);
   }
else
   {
   if (isalpha(prog->car[cour]) || prog->car[cour] == '.')
      {
      while (!isdelim(prog->car[cour])) *temp++ = prog->car[cour++];
      token_type = STRING;
      }
   else
      {
      cour++;
      return(token_type = STRING);
      }
   }
*temp = '\0';

if (token_type == STRING )
   {
   tok = com_look_up(token);
   if (tok)
      token_type = COMMAND;
   else
      {
      tok = funct_look_up(token);
      if (tok)
	 token_type = FUNCTION;
      else
	 token_type = VARIABLE;
      }
   }

return(token_type);

}


/*  recherche d'une commande dans la table des commandes */

char com_look_up(s)
char *s;

{
short i;
char *p;

p=s;
i=0;
while (p[i] != '\0')
   {
   p[i] = tolower(p[i]);
   i++;
   }
for ( i = 0; *com_table[i].command; i++ )
    if ( !strcmp(com_table[i].command, s)) return com_table[i].tok;
return 0;
}

/*  recherche d'une fonction dans la table des fonctions */

char funct_look_up(s)
char *s;

{
short i;
char *p;

p=s;
i=0;
while (p[i] != '\0')
   {
   p[i] = tolower(p[i]);
   i++;
   }
for ( i = 0; *funct_table[i].function; i++ )
    if ( !strcmp(funct_table[i].function, s)) return funct_table[i].tok;
return 0;
}

/*  voir si caractère particulier ? */
short isdelim(c)
char c;

{
if (strchr(" +-&~^*=`|(),%", c) || c == '\n' || c == '\r' || c == 0 || c == EOF)
   return 1;
else
   return 0;

}

/* voir si caractère egale blanc */
short iswithe(c)
char c;

{
if (c == ' ' || c == '\t' )
   return 1;
else
   return 0;

}

/* putback  */
void putback()

{
char *t;
short i;

t = token;
for (i=0; t[i] != '\0';i++) cour--;
}
