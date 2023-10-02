/************************************************************
 *   CALMAT  ver 1.0                                        *
 *   recursive descent parser                               *
 *   source : PARSER.C                                      *
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
       } com_table[];
extern struct functions
       {
       char  function[20];
       char  tok;
       } funct_table[];

extern char token[80];
extern char token_type;
extern char tok;

extern struct variables
       {
       short l;
       short c;
       double *matrice;
       } *variable[MAXVAR];
//extern struct variables *variable[MAXVAR];

void affectation();
struct variables *get_exp();
struct variables *level2();
struct variables *level3();
struct variables *level4();
struct variables *level5();
struct variables *level6();
struct variables *level7();
struct variables *primitive();
struct variables *arith();
struct variables *unary();
struct variables *mult_scal();

struct variables *exec_chi_deux();
struct variables *exec_dist_fact();
/*struct variables *exec_inv_sym();*/
struct variables *exec_cent_red();
struct variables *exec_matint();
struct variables *exec_matzero();
struct variables *exec_cprofil();

char get_token();
void serror(), putback(), desallocdyn();

/* affectation */
void affectation()

{
short var;
struct variables *res;

get_token();
if(!isalpha(*token))
  {
  printf("erreur de nom de variable !!\n");
  serror();
  }
var = toupper(*token) - 'A';
if (var > MAXVAR )
   {
   printf("erreur dans le nom de variable !!\n");
   serror();
   }
get_token();
if (*token != '=')
   {
   printf("erreur de syntaxe  !!");
   serror();
   }
res = get_exp();
if (variable[var] != NULL)
   {
   free(variable[var]->matrice);
   free(variable[var]);
   }
variable[var] = res;
}

/* recursive descent expression parser  */

struct variables *get_exp()

{
struct variables *resout;

get_token();
if (!*token)
   {
   printf("erreur:  pas d'expression trouvée !!");
   serror();
   }
resout = level2();
if (tok != EOL) putback();
return(resout);
}

/*  Addition ou soustraction */
struct variables *level2()

{
char op;
struct variables *hold;
struct variables *resout;

resout = level3();
while ((op = *token) == '+' || op == '-' || op == '|' || op == '&')
      {
      get_token();
      hold = level3();
      resout = arith(op, resout, hold);
      }
return(resout);
}

/*  mutiplication */
struct variables *level3()

{
struct variables *hold;
struct variables *resout;
char op;

resout = level5();
while ( (op = *token)  == '*' || op == '^')
      {
      get_token();
      hold = level5();
      resout = arith(op,resout, hold);
      }
return(resout);
}

/*  transposition */
struct variables *level5()

{
char op;
struct variables *resout;

op = 0;
if ((token_type ==  DELIMITER) && ((op =*token) == '`' || (op == '~')) )
   {
   op = *token;
   get_token();
   }
resout = level6();
if (op == '`' || op == '|' || op == '~')
   resout =  unary(op, resout);
return(resout);
}

/*   apell de fonctions   */
struct variables *level6()
{
struct variables *resout;
short function;

if (token_type  == FUNCTION)
   {
   function = tok;
   switch(function)
     {
     case CHI_DEUX:
       get_token();
       resout = level7();
       resout = exec_chi_deux(resout);
       break;
     case DIST_FACT:
       get_token();
       resout = level7();
       resout = exec_dist_fact(resout);
       break;
     /*case INV_SYM:
       get_token();
       resout = level7();
       resout = exec_inv_sym(resout);
       break; */
     case CENT_RED:
       get_token();
       resout = level7();
       resout = exec_cent_red(resout);
       break;
     case MATINT:
       resout = exec_matint();
       break;
     case MATZERO:
       resout = exec_matzero();
       break;
     case CPROFIL:
       get_token();
       resout = level7();
       resout = exec_cprofil(resout);
       break;
     }

   }
else
   resout = level7();

return(resout);
}

struct variables *level7()

{
struct variables *resout;
if ((*token == '(') && (token_type == DELIMITER))
   {
   get_token();
   resout = level2();
   if (*token != ')')
      {
      printf("parenthèses non fermées !!");
      serror();
      }
   get_token();
   }
else

   resout = primitive();
return(resout);
}

/* trouver valeurs d'une matrice */
struct variables *primitive()

{
char var;
struct variables *result;
double scalaire;

switch(token_type)
    {
    case VARIABLE:
     if (!isalpha(*token))
        {
        printf("pas de nom de variable !!");
        serror();
        }
     var = toupper(*token) -'A';
     if (var > MAXVAR )
        {
        printf("pas de nom de variable !!");
        serror();
        }
     if (variable[var] == NULL)
        {
        printf("erreur: variable non initialisée");
        serror();
        };
     get_token();
     result = variable[var];
     break;
    case NUMBER:
     scalaire = atof(token);
     result = get_exp();
     result = mult_scal(scalaire,result);
     get_token();
     break;
    default:
     printf("erreur de syntaxe dans l'expression");
     serror();
     break;
    }
    return(result);
}
