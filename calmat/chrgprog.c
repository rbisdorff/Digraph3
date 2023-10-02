/*************************************************************
 *  projet CAMAT  fonction de chargement du programme source *
 *  source : CHRGPROG.C                                      *
 *************************************************************/
#include <stdio.h>


/* #define TEST  */
#include "calmat.h"

#ifndef TEST
extern struct programmes
       {
       char car[PROG_SIZE];
       }programme;
#endif


#if defined(TEST)
struct programmes
       {
       char car[PROG_SIZE];
       };
short load_program();

main(argc,argv)
short argc;
char *argv[];

{
struct programmes p_buf;
short i;

if(argc != 2)
  {
  printf("erreurs arguments\n");
  serror();
  }
/*
if( !(p_buf = (struct programmes *) calloc(PROG_SIZE,sizeof(char))))
  {
  printf("erreur allocation mémoire\n");
  serror();
  }
  */
printf("%s ",argv[1]);
if (!load_program(&p_buf, argv[1]))
   {
   printf("erreur chargement\n");
   serror();
   }
printf("la source: %s \n",argv[1]);
for ( i=0; p_buf.car[i] != '\0' && i < PROG_SIZE; i++)
    printf("%c",p_buf.car[i]);

exit(0);
}
#endif

/*  routine de chargement d'un programme */
short load_program(p, fname)
struct programmes *p;
char *fname;

{
FILE *fp;
short i;

printf("Nom du programme : %s \n",fname);
fp =
fopen(fname, "rb");
if ( fp == NULL)
   return 0;

i = 0;
do
  {
  p->car[i] = getc(fp);
  i++;
  } while (!feof(fp) && i < PROG_SIZE);

p->car[i-1] = '\0';
fclose(fp);
return(1);
}
