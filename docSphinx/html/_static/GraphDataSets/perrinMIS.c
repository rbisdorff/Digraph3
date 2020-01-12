/* -------------------------------------- *
 * Generating MIS set of Cn with the      *
 * Perrin sequence algorithm.             *
 * Temporary files used.                  *
 * even versus odd order optimized.       *
 * RB May 2006                            *
 * Current revision $Revision: 1.4 $      *
 * i686 compilation flags :               *       
 * gcc -s -march=pentium4 -mfpmath=sse    *
 * -fomit-frame-pointer -ffast-math -O3   *
 * -------------------------------------- */

#include <stdio.h>
#include <sys/time.h>

#define MAX_ORDER 50
#define SMALL_ORDER 20
#define ch_True  '1'
#define ch_False '0'


/* ---  Perrin sequence ---*/
unsigned long  Perrin(unsigned long orderIn){

     unsigned long a, a0, a1, a2;
     unsigned long n;

     a0 = 3;
     a1 = 0;
     a2 = 2;

     if (orderIn == 0) return a0;
     else if (orderIn == 1) return a1;
     else if (orderIn == 2) return a2;
     else{
       a = a0 + a1;
       for (n = 3; n < orderIn; n++){
	 a0 = a1;
	 a1 = a2;
	 a2 = a;
	 a = a0 + a1;
       }
       return a;
     }
}

/* ---  Perrin sequence algorithm for MIS extraction  ---*/
main() {
  
  /* time access structure  */
  struct timeval before,after,lapsed;
  struct timezone tz;
  double diff;

  FILE *fi, *fo, *fo1;
  char buf, testinit,testfinal;
  char cur0dat[15], cur1dat[15], cur2dat[15];
  unsigned long mis ,i, ml;
  unsigned long n, order, evenorder, r;
  unsigned long v[MAX_ORDER];
  unsigned long Perrin(unsigned long) ;


/* Init Data */
  printf("* -------------------------------------- *\n");
  printf("* Generating MIS set of Cn with the      *\n");
  printf("* Perrin sequence algorithm.             *\n");
  printf("* Temporary files used.                  *\n"); 
  printf("* even versus odd order optimized.       *\n");
  printf("* RB December 2006                       *\n");
  printf("* Current revision $Revision: 1.4 $       \n");       
  printf("* -------------------------------------- *\n");

  printf("Input cycle order ? ");
  scanf("%d", &order);
  
  if ((order < 5) || (order > MAX_ORDER)){  /* computation limits */
    printf("usage: ./perrinMIS order ( 4 < order < 51)\n");
    exit(1);
  }
  


  /*times(&before);*/
  gettimeofday(&before,&tz);

  /* first three initial MIS sets */ 
  fo = fopen("p2.dat","w");
  putc(ch_True,fo);
  putc(ch_False,fo);
  putc(0x0A,fo);
  putc(ch_False,fo);
  putc(ch_True,fo);
  putc(0x0A,fo);
  fclose(fo);

  fo = fopen("p3.dat","w");
  putc(ch_True,fo);
  putc(ch_False,fo);
  putc(ch_False,fo);
  putc(0x0A,fo);
  putc(ch_False,fo);
  putc(ch_True,fo);
  putc(ch_False,fo);
  putc(0x0A,fo);
  putc(ch_False,fo);
  putc(ch_False,fo);
  putc(ch_True,fo);
  putc(0x0A,fo);
  fclose(fo);

  fo = fopen("p4.dat","w");
  putc(ch_True,fo);
  putc(ch_False,fo);
  putc(ch_True,fo);
  putc(ch_False,fo);
  putc(0x0A,fo);
  putc(ch_False,fo);
  putc(ch_True,fo);
  putc(ch_False,fo);
  putc(ch_True,fo);
  putc(0x0A,fo);
  fclose(fo);

    
  /* init algo pour n = 4 and order 5 */

  strcpy(cur0dat,"p2.dat"); /* misset C2 */
  strcpy(cur1dat,"p3.dat"); /* misset C3 */
  strcpy(cur2dat,"p4.dat"); /* misset C4 */ 

  n = 4;

  r = order % 2;  
  if (r == 0){   /* even order with order/2 double steps */
    evenorder = order;
  }
  else {
    evenorder = order -1; /* odd order with (order-1)/2 double steps 
			     plus a single step. */
  }
  while (n < evenorder){      

    n += 1;

    /* compute cur.dat */
    fi = fopen(cur0dat,"r");
    fo = fopen("cur.dat","w");
    if (fi == NULL) {
	printf("\n error in reading file %s", cur0dat);
      }
    for (mis = 0; mis < Perrin(n-3); mis++){      
	testinit = getc(fi);
	putc(testinit,fo);
	for (i = 1; i < n-4; i++){
	  putc(getc(fi),fo);
	}
	testfinal = getc(fi);
	putc(testfinal,fo);
	if (testinit == ch_True){
	  putc(ch_True,fo);
	  putc(ch_False,fo);
	  putc(ch_False,fo);
	}
	else if (testfinal == ch_True){
	  putc(ch_False,fo);
	  putc(ch_False,fo);
	  putc(ch_True,fo);
	}
	else {
	  putc(ch_False,fo);
	  putc(ch_True,fo);
	  putc(ch_False,fo);
	};
	putc(getc(fi),fo);
    }	 
    fclose(fi);

    /* compute cur.dat and curd.dat */
    fi = fopen(cur1dat,"r");
    fo1 = fopen("curd.dat","w");
    for (mis = 0; mis < Perrin(n-2); mis++){
	testinit = getc(fi);
	putc(testinit,fo);
	putc(testinit,fo1);
	for (i = 1; i < n-3; i++){
	  buf = getc(fi);
	  putc(buf,fo);
	  putc(buf,fo1);
	}
	testfinal = getc(fi);
	putc(testfinal,fo);
	putc(testfinal,fo1);
	if (testfinal == ch_True){
	  putc(ch_False,fo);
	  putc(ch_True,fo);
	  putc(ch_False,fo1);
	  putc(ch_False,fo1);
	  putc(ch_True,fo1);
	  }
	else if (testinit == ch_True){
	  putc(ch_True,fo);
	  putc(ch_False,fo);
	  putc(ch_True,fo1);
	  putc(ch_False,fo1);
	  putc(ch_False,fo1);
	}
	else {
	  putc(ch_True,fo);
	  putc(ch_False,fo);
	  putc(ch_False,fo1);
	  putc(ch_True,fo1);
	  putc(ch_False,fo1);
	}
	buf = getc(fi);
	putc(buf,fo);
	putc(buf,fo1);
    }
      
    fclose(fi);
    fclose(fo);

    /* compute curd.dat */

    n += 1;

    fi = fopen(cur2dat,"r");
    for (mis = 0; mis < Perrin(n-2); mis++){
	for (i = 0; i < n-3; i++){
	  putc(getc(fi),fo1);
	}
	testfinal = getc(fi);
	putc(testfinal,fo1);
	if (testfinal == ch_True){
	  putc(ch_False,fo1);
	  putc(ch_True,fo1);
	  }
	else {
	  putc(ch_True,fo1);
	  putc(ch_False,fo1);
	}
	putc(getc(fi),fo1);
    }      
    fclose(fi);
    fclose(fo1);

    /* propagate recursive results */

    /* cur2.dat -->> cur0.dat */
    strcpy(cur0dat,"cur0.dat");
    fi = fopen(cur2dat,"r"); 
    fo = fopen(cur0dat,"w");
    for (mis=0; mis < Perrin(n-2); mis++){
	for (i=0; i<n-2; i++){
	    putc(getc(fi),fo);
	}
	putc(getc(fi),fo);
    }
    fclose(fi);
    fclose(fo);

    /* cur.dat --> cur1.dat */
    strcpy(cur1dat,"cur1.dat");
    fi = fopen("cur.dat","r"); 
    fo = fopen(cur1dat,"w");
    for (mis=0; mis < Perrin(n-1); mis++){
	for (i=0; i<n-1; i++){
	    putc(getc(fi),fo);
	}
	putc(getc(fi),fo);
    }
    fclose(fi);
    fclose(fo);
    
    /* curd.dat -- > cur2.dat  */
    strcpy(cur2dat,"cur2.dat");
    fi = fopen("curd.dat","r");
    fo = fopen(cur2dat,"w");
    for (mis=0; mis < Perrin(n); mis++){
	for (i=0; i<n; i++){
	    putc(getc(fi),fo);
	}        
	  putc(getc(fi),fo);
     }
     fclose(fo);

  }

  if (r != 0){   /* odd order need a supplemntatry single step */
        
    n += 1;

    /* compute MIS_0 */
    fo = fopen("cur2.dat","w");
    fi = fopen(cur0dat,"r");
    if (fi == NULL) {
	printf("\n error in reading file %s", cur0dat);
    }
    for (mis = 0; mis < Perrin(n-3); mis++){      
      testinit = getc(fi);
      putc(testinit,fo);
      for (i = 1; i < n-4; i++){
	putc(getc(fi),fo);
      }
      testfinal = getc(fi);
      putc(testfinal,fo);
      if (testinit == ch_True){
	putc(ch_True,fo);
	putc(ch_False,fo);
	putc(ch_False,fo);
      }
      else if (testfinal == ch_True){
	putc(ch_False,fo);
	putc(ch_False,fo);
	putc(ch_True,fo);
      }
      else {
	putc(ch_False,fo);
	putc(ch_True,fo);
	putc(ch_False,fo);
      };
	putc(getc(fi),fo);
      }	 
      fclose(fi);

      /* compute MIS_1 */
      fi = fopen(cur1dat,"r");
      for (mis = 0; mis < Perrin(n-2); mis++){
	for (i = 0; i < n-3; i++){
	  putc(getc(fi),fo);
	}
	testfinal = getc(fi);
	putc(testfinal,fo);
	if (testfinal == ch_True){
	  putc(ch_False,fo);
	  putc(ch_True,fo);
	}
	else {
	  putc(ch_True,fo);
	  putc(ch_False,fo);
	}
	putc(getc(fi),fo);
      }     
      fclose(fi);
      fclose(fo);

  }
  /* print results */
  
  gettimeofday(&after,&tz);

  for (i=0;i<order+1;i++){
    v[i] = 0;
  }

  printf("* ---- Results -----*\n");
  fi = fopen("cur2.dat","r");
  fo = fopen("res.py","w");
  fputs("misset = set([\n",fo);
  for (mis=0; mis < Perrin(order); mis++){
    fputs("frozenset([\n",fo);
    if (order < SMALL_ORDER){
    printf("mis %d : ", mis+1);
    }
    ml = 0;
    for (i=0; i<order; i++){
      testinit = getc(fi);
      if (testinit == ch_True){
	ml += 1;
	fprintf(fo,"'1',");
      }
      else {
	fprintf(fo,"'0',");
      }
      if (order < SMALL_ORDER) {
	if (testinit== ch_True){
	  printf("%d",1);}
	else {
	  printf("%d",0);}
      }
    }
    fprintf(fo,"\n");
    v[ml] += 1;
    fputs("]),\n",fo);
    if (order < SMALL_ORDER) {printf("\n");}
    if (getc(fi) != 0x0A) {
      printf("error reading results in cur.dat !");
    }
  }
  fputs("])\n",fo);
  fclose(fo);
  fclose(fi);
  
  printf("Cardinalities:\n");
  ml = 0;
  for (i=0; i < order+1; i++){
    if (order < SMALL_ORDER){
      printf("%d : %d\n", i,v[i]);    
       }
    else {
      if (v[i] > 0){
	printf("%d : %d\n", i,v[i]);
    }
    }
    ml += v[i];
    }
  printf("Total: %d\n",ml);

  if (before.tv_usec > after.tv_usec) { 
     after.tv_usec += 1000000; 
     after.tv_sec--; 
  }
  diff = (after.tv_usec - before.tv_usec)/1000; 
  lapsed.tv_sec  = after.tv_sec  - before.tv_sec; 
  printf("execution time: %d sec. and ",lapsed.tv_sec);
  printf("%.f millisec.\n",diff);

}

/* ----------------------------------- *
 * Log record for changes:
 * $Log: perrinMIS.c,v $
 * Revision 1.4  2006/12/28 09:56:12  bisi
 * Added XML storage procedure with xsl stylesheet and DTD.
 *
 * Revision 1.3  2006/12/26 15:17:40  bisi
 * Adding version number to perrinMIS binary execution trace.
 *
 * Revision 1.2  2006/12/26 15:10:35  bisi
 * Debugging perrinMIS.c: writeng 01 intermediate files ao.
 *
 *-------------------------------------*/
