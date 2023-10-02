/**********************************************
 *    SCATTER.EXE                             *
 *    CRP-CU CREDI 1990 (c)  R.Bisdorff       *
 **********************************************/
 #include "io.h"
 #include "fcntl.h"
 #include "stdio.h"
 #include "conio.h"
 #include "stdlib.h"
 #include "process.h"
 #include "alloc.h"
 #include "string.h"
 #include "ctype.h"

 #define MAXVAR 26
 #define MAXELEM 6000
 #define MAX_LABELS 1000
  struct variables
       {
       short l;
       short c;
       double *matrice;
       };
  struct variables  *variable;
  struct labels
       {
       short l;
       char *texte[MAX_LABELS];
       };
  struct labels label_file;

 void *open_font_file(char *font_file);
 void exec_load(char *s,short  l, short c);
 void exec_load_labels(char *s, short l);
 void paint_graph(short varx, short vary);
 struct variables *allocdyn(struct variables *resin, short n, short m);


main(argc,argv)
short argc;
char *argv[];

{
 short l,c;
 short varx, vary;
 char buffer[BUFSIZ];
 char ind = '\0';

 fprintf(stdout, "ÚÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄ¿\n");
 fprintf(stdout, "³ CRP-CU 1990  (c) R.Bisdorff  SCATTER.  ver. 1.1   ³\n");

 if(argc != 5)
   {
   fprintf(stderr, "³ Syntaxe:                                          ³\n");
   fprintf(stderr, "³ SCATTER data_labels donnes n1  n2                ³\n");
   fprintf(stderr, "³ n1: nbre de lignes  n2 : nbre de collonnes        ³\n");
   fprintf(stderr, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }
 l = atoi(argv[3]);
 c = atoi(argv[4]);
 fprintf(stdout, "³ Interrogation graphique de la matrice :\n");
 fprintf(stdout, "³    %s  (%d,%d)\n",argv[2],l,c);
 fprintf(stdout, "³ fichier des labels : %s\n ",argv[1]);
 exec_load_labels(argv[1],l);
 exec_load(argv[2],l,c);
  while ( ind != 'n')
       {
       fprintf(stdout, "³ axe des x (1 - %d) :",c);
       scanf("%d",&varx);
       fprintf(stdout, "³ axe des y (1 - %d) :",c);
       scanf("%d",&vary);
       if ((varx > 0) && (varx < c) && (vary > 0) && (vary < c))
	   {
	   paint_graph(varx,vary);
	   fprintf(stdout, "ÚÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄ¿\n");
	   fprintf(stdout, "³ CRP-CU CREDI 1990 R.Bisdorff  SCATTER  ver.1.1    ³\n");
	   }
       else
	   fprintf(stdout, "³ Numros d'axes incorrectes !!!                    ³\n");
       fprintf(stdout, "³ autre graphique (o/n)");
       scanf("%s",buffer);
       if ((buffer[0] == 'N')||(buffer[0]=='n'))
	  ind = 'n';
       }
 fprintf(stdout,           "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
 exit(0);
}



/*  chargement d'une matrice */
void exec_load(char *s, short lig, short col)

{
FILE *fp;
short n,m,i,j,c,ci;
char buffer[BUFSIZ];
char temp[25], dn, eol_fp;

/*   fichier contenant la matrice  charger */
if (strcmp(s,"con:") != 0)
    fp = fopen(s,"r");
else
    fp = stdin;

if (fp == NULL)
   {
   printf("³ Erreur d'ouverture du fichier %s !!!\n",s);
   fprintf(stdout,         "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   };
printf("³ Lecture de la matrice %s\n",s);


/*  nombre de lignes de la matrice */
n = lig;
if ( n < 1 )
   {
   printf("³ erreur de syntaxe : nombre de lignes incorrecte !!! \n");
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }

/*  nombre de colonnes de la matrice  */
m = col;
if ( m < 1 )
   {
   printf("³ erreur de syntaxe : nombre de colonnes incorrecte !!!\n");
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }

if ( n*m > MAXELEM )
   {
   printf("³ erreur de dimension : nombre d'lments trop lev !!!\n");
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }
/* allocation de la variable associe   */
variable = allocdyn(variable,n,m);

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
		*(variable->matrice + i*m + j++) = atof(temp);
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
	    printf("³ Erreur de lecteur en ligne %d \n",i+1);
	    fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
	    exit(1);
	    }
	 i++;
	 j = 0;
	 eol_fp = '\0';
	 }
       if ( (j == m) && (eol_fp != '\1'))
	  {
	  c--;        /* vrifier si la dernire ligne est compltement lue */
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
/*  dconnexion du fichier  */
if (i < n )
   {
   printf("³ Erreur :  le fichier est trop court !!! \n");
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }
if (fp != stdin)
   fclose(fp);
/* retour */
return;

}
/*  chargement des lables */
void exec_load_labels(char *s, short lig)

{
FILE *fp;
short n,m,i, t_len;
char buffer[BUFSIZ];

/*   fichier contenant les lables  charger */
if (strcmp(s,"con:") != 0)
    fp = fopen(s,"r");
else
    fp = stdin;

if (fp == NULL)
   {
   printf("³ Erreur d'ouverture du fichier des labels : %s !!!\n",s);
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   };
printf("³ Lecture du fichier des labels: %s \n",s);

/*  nombre de lignes de la matrice */
n = lig;
if ( n < 1 )
   {
   printf("³ nombre de lignes incorrecte !!! \n");
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }

/*  nombre de colonnes de la matrice  */
m = 1;

if ( n*m > MAX_LABELS )
   {
   printf("³ erreur de dimension : nombre de labels trop lev !!!\n");
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }
label_file.l = n;

/* lecture de la matrice */
i = 0;
while ( (fgets(buffer, BUFSIZ, fp) != 0)  && (i < n) )
      {
      t_len = strlen(buffer) +1;
      label_file.texte[i] =  malloc(t_len);
      strcpy(label_file.texte[i++],buffer);
      }
/*  dconnexion du fichier  */
if (i < n )
   {
   printf("³ Erreur :  le fichier est trop court !!! \n");
   fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
   exit(1);
   }
if (fp != stdin)
   fclose(fp);
/* retour */
return;

}

struct variables *allocdyn(struct variables *resin, short l, short c)
{
long n;

    resin = (struct variables *) malloc(sizeof(struct variables));
    if (resin == 0 )
       {
       printf("³  erreur d'allocation de mmoire !!");
       fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
       exit(1);
       }
    resin->l = l;
    resin->c = c;
    n = l * c;
    resin->matrice = (double *) calloc(n,sizeof(double));
    if (resin->matrice == 0 )
       {
       printf(" erreur d'allocation de mmoire !!");
       fprintf(stdout, "ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ\n");
       exit(1);
       }
    return(resin);
}

