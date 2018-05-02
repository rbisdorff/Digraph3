/**********************************************
 *    SCATTER.EXE                             *
 *    LERIA  89 R.Bisdorff                    *
 **********************************************/
 #include "io.h"
 #include "fcntl.h"
 #include "stdio.h"
 #include "conio.h"
 #include "stdlib.h"
 #include "process.h"
 #include "alloc.h"
 #include "string.h"

 /* open font file */
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
