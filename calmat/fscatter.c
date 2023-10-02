/**********************************************
 *    FSCATTER.C                               *
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

 #include "calmat.h"

  struct variables
       {
       short l;
       short c;
       double *matrice;
       };

  struct data_labels
       {
       short l;
       char *texte[MAXLABELS];
       };
  struct data_labels label_file;
  extern char token[80];
  extern char token_type;
  extern struct variables *variable[MAXVAR];

  short iswithe();
  char get_token();
  void serror();
  void *open_font_file(char *font_file);
  void exec_load_labels(char *s, short l);
  void exec_free_labels(short l);
  void paint_graph(short var, short varx, short vary);
  struct variables *allocdyn(struct variables *resin, short n, short m);
  void exec_scatter();

void exec_scatter()

{
 short l,c,var;
 short varx, vary;
 char buffer[BUFSIZ];
 char ind = '\0';

 fprintf(stdout, " CRP-CU 1990  (c) R.Bisdorff  SCATTER.  ver. 1.1   \n");

 get_token();
 fprintf(stdout, " Interrogation graphique de la matrice : %s \n",token);
 var = toupper(*token) - 'A';
 if (var > MAXVAR - 1 )
    {
     printf( "erreur de syntaxe !!" );
     serror();
    }
 if (variable[var] == NULL) 
    {
    printf("Erreur: matrice %s  non encore identifie !! \n",token);
    serror();
    }
     
  l = variable[var]->l;
  c = variable[var]->c;
  fprintf(stdout, " dimension: (%d,%d)\n",l,c);

  get_token();

 fprintf(stdout, "fichier des labels : %s\n ",token);
 exec_load_labels(token,l);
 while ( ind != 'n')
       {
       fprintf(stdout, " axe des x (1 - %d) :",c);
       scanf("%d",&varx);
       fprintf(stdout, " axe des y (1 - %d) :",c);
       scanf("%d",&vary);
       if ((varx > 0) && (varx <= c) && (vary > 0) && (vary <= c))
	   {
	   paint_graph(var,--varx,--vary);
	   fprintf(stdout, "CRP-CU CREDI 1990 R.Bisdorff  SCATTER  ver.1.1    ³\n");
	   }
       else
	   fprintf(stdout, "Numros d'axes incorrectes !!!                    ³\n");
       fprintf(stdout, "autre graphique (o/n)");
       scanf("%s",buffer);
       if ((buffer[0] == 'N')||(buffer[0]=='n'))
	  ind = 'n';
       }
 exec_free_labels(l);
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
   printf("Erreur d'ouverture du fichier des labels : %s !!!\n",s);
   serror();
   };
printf("Lecture du fichier des labels: %s \n",s);

/*  nombre de lignes de la matrice */
n = lig;
if ( n < 1 )
   {
   printf("nombre de lignes incorrecte !!! \n");
   serror();
   }

/*  nombre de colonnes de la matrice  */
m = 1;

if ( n*m > MAXLABELS )
   {
   printf("erreur de dimension : nombre de labels trop lev !!!\n");
   serror();
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
   printf("Erreur :  le fichier est trop court !!! \n");
   serror();
   }
if (fp != stdin)
   fclose(fp);
/* retour */
return;

}

void exec_free_labels(short lig)
{
 short i;

 for(i = 0; i < lig; i++)
    free(label_file.texte[i]);
 return;
}

void *open_font_file(char *font_file)
{
 int handle;
 int fsize;
 void *fontp;
 handle = open(font_file, O_RDONLY | O_BINARY );
 if (handle == -1)
    {
     printf("unable to open font file %s \n",font_file);
     exit(1);
    }
 fsize = filelength(handle);
 fontp = malloc(fsize);
 if (fontp == NULL)
    {
     printf("allocation error for font file \n");
     exit(1);
    }
 if (read(handle, fontp, fsize) != fsize)
    {
     printf("unable to read font file %s !!\n",font_file);
     exit(1);

    }
 close(handle);
 return(fontp);
}

#include "graphics.h"

void paint_graph(short var, short varx, short vary)

{
 void  *litt_fontp;
 int errorcode;
 int graphdriver;
 int graphmode;
 int mx,my,offx,offy;
 int color, maxcolor;

 /***  i nitialisations ***/
 litt_fontp = open_font_file("d:\\tc\\bgi\\LITT.CHR");

  if (registerfarbgifont(litt_fontp) != SMALL_FONT)
    {
    printf("unable to register font file 'LITT.CHR'\n");
    exit(1);
    }
 graphdriver = DETECT;
 initgraph(&graphdriver,&graphmode,"d:\\tc\\bgi");
 errorcode = graphresult();
 if (errorcode != grOk)
    {
    printf("graphics error: %s\n",grapherrormsg(errorcode));
    exit(1);
    }
 maxcolor = getmaxcolor();
 
 settextstyle(SMALL_FONT, HORIZ_DIR, 4);
 outtextxy( 5, 5 , "SCATTER  CRP-CU CREDI  1990 R.BISDORFF");
 /*******  dessins des points   **********/
 {
 int i,n,m,x,y;
 double maxx, maxy, minx, miny;
 n = variable[var]->l;
 m = variable[var]->c;
 maxx = minx = *(variable[var]->matrice+varx);
 maxy = miny = *(variable[var]->matrice+vary);
 mx = getmaxx();
 offx = mx/10;
 mx -= offx;
 my = getmaxy();
 offy = my/10;
 my -= offy;
 for ( i = 0; i < n; i++)
     {
     if (*(variable[var]->matrice+i*m+varx)>maxx)
	     maxx =*(variable[var]->matrice+i*m+varx);
     if (*(variable[var]->matrice+i*m+varx)<minx) minx =*(variable[var]->matrice+i*m+varx);
     if (*(variable[var]->matrice+i*m+vary)>maxy) maxy =*(variable[var]->matrice+i*m+vary);
     if (*(variable[var]->matrice+i*m+vary)<miny) miny =*(variable[var]->matrice+i*m+vary);
     }

 settextstyle(SMALL_FONT, HORIZ_DIR, 4);
 settextjustify(CENTER_TEXT, CENTER_TEXT);
 if ((maxx - minx) == 0)
    {
    outtextxy(mx/2,my/2, "Valeurs toutes identiques sur l'axe des x !!");
    getch();
    closegraph();
    return;
    }
 if ((maxy - miny) == 0)
    {
    outtextxy(mx/2,my/2, "Valeurs toutes identiques sur l'axe des y !!");
    getch();
    closegraph();
    return;
    }
 for ( i = 0; i < n; i++)
     {                                         
     x = (*(variable[var]->matrice+i*m+varx)-minx)/(maxx-minx)*mx;
     y = (*(variable[var]->matrice+i*m+vary)-miny)/(maxy-miny)*my;
     outtextxy(x+offx/2,y+offy/2,label_file.texte[i]);
     }
 }
 /********  dessin des axes  ************/
 {
 char axe_t[10];
 char axe_no[5];
 short num_x,num_y;

 setlinestyle(DOTTED_LINE,0,NORM_WIDTH);
 line((mx+offx)/2,offy/2,(mx+offx)/2,my+offy/2);
 line(offx/2,(my+offy)/2,mx+offx/2,(my+offy)/2);

 settextstyle(SMALL_FONT, HORIZ_DIR, 4);
 strcpy(axe_t,"axe : ");
 num_x = varx + 1;
 itoa(num_x,axe_no,10);
 strcat(axe_t,axe_no);
 outtextxy( mx+offx/2, (my+offy)/2-5 , axe_t);

 settextstyle(SMALL_FONT, VERT_DIR, 4);
 strcpy(axe_t,"axe:");
 num_y = vary + 1;
 itoa(num_y,axe_no,10);
 strcat(axe_t,axe_no);
 outtextxy(( mx+offx)/2-8,20, axe_t);
 }
 /*******   arrt sur l'image *************/
 getch();
 /*******   retour au mode texte **********/
 closegraph();
 return;
 }  /********  fin paint graph ************/
