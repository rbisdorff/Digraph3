/**********************************************
 *    SCATTER.EXE                             *
 *    CRP-CU  1990 R.Bisdorff                 *
 **********************************************/
/*  paintgraph   */

 #include "graphics.h"
 #include "io.h"
 #include "fcntl.h"
 #include "stdio.h"
 #include "conio.h"
 #include "stdlib.h"
 #include "process.h"
 #include "alloc.h"
 #include "string.h"

 #define MAXVAR 26
 #define MAXELEM 6000
 #define MAX_LABELS 1000
 extern struct variables
       {
       short l;
       short c;
       double *matrice;
       };
 extern  struct variables  *variable;
 extern  struct labels
       {
       short l;
       char *texte[MAX_LABELS];
       };
  extern struct labels label_file;

 void *open_font_file(char *font_file);
 void exec_load(char *s,short  l, short c);
 void exec_load_labels(char *s, short l);
 void paint_graph(short varx, short vary);
 struct variables *allocdyn(struct variables *resin, short n, short m);

 void paint_graph(short varx, short vary)
 {  /*********   dbut paint graph ***********/
 void  *litt_fontp;

 int errorcode;
 int graphdriver;
 int graphmode;
 int mx,my,offx,offy;
 int color, maxcolor;

 /***   nitialisations ***/
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
 n = variable->l;
 m = variable->c;
 maxx = minx = *(variable->matrice+varx);
 maxy = miny = *(variable->matrice+vary);
 mx = getmaxx();
 offx = mx/10;
 mx -= offx;
 my = getmaxy();
 offy = my/10;
 my -= offy;
 for ( i = 0; i < n; i++)
     {
     if (*(variable->matrice+i*m+varx)>maxx) maxx =*(variable->matrice+i*m+varx);
     if (*(variable->matrice+i*m+varx)<minx) minx =*(variable->matrice+i*m+varx);
     if (*(variable->matrice+i*m+vary)>maxy) maxy =*(variable->matrice+i*m+vary);
     if (*(variable->matrice+i*m+vary)<miny) miny =*(variable->matrice+i*m+vary);
     }
 settextstyle(SMALL_FONT, HORIZ_DIR, 4);
 settextjustify(CENTER_TEXT, CENTER_TEXT);
 for ( i = 0; i < n; i++)
     {                                         
     x = (*(variable->matrice+i*m+varx)-minx)/(maxx-minx)*mx;
     y = (*(variable->matrice+i*m+vary)-miny)/(maxy-miny)*my;
     outtextxy(x+offx/2,y+offy/2,label_file.texte[i]);
     }
 }
 /********  dessin des axes  ************/
 {
 char axe_t[10];
 char axe_no[5];

 setlinestyle(DOTTED_LINE,0,NORM_WIDTH);
 line((mx+offx)/2,offy/2,(mx+offx)/2,my+offy/2);
 line(offx/2,(my+offy)/2,mx+offx/2,(my+offy)/2);

 settextstyle(SMALL_FONT, HORIZ_DIR, 4);
 strcpy(axe_t,"axe : ");
 itoa(varx,axe_no,10);
 strcat(axe_t,axe_no);
 outtextxy( mx+offx/2, (my+offy)/2-5 , axe_t);

 settextstyle(SMALL_FONT, VERT_DIR, 4);
 strcpy(axe_t,"axe:");
 itoa(vary,axe_no,10);
 strcat(axe_t,axe_no);
 outtextxy(( mx+offx)/2-8,20, axe_t);
 }
 /*******   arrt sur l'image *************/
 getch();
 /*******   retour au mode texte **********/
 closegraph();
 return;
 }  /********  fin paint graph ************/
