#########################################################################
#  cora  V3.11  26th Nov 92                Centre de Recherche Public   #
#                                           - Centre Universitaire -    #
#  This S function performs               162a, Avenue de la Faiencerie #
#  a correspondence analysis                    L-1511 Luxembourg       #
#  of a two-way contingency                   Tel: (+352) 47 02 61      #
#  table and provides the                     Fax: (+352) 47 02 64      #
#  result as an S object                                                #
#                                             IABD Project - CREDI      #
#                                             --------------------      #
#                                                                       #
#                                           N. Beaumont - R. Bisdorff   #
#                                             F. Fehlen - B. Perbal     #
#########################################################################

coraPersp = function(X) {
    #x = read.csv(fileName)
    #nrow = dim(x)[1]
    #ncol = dim(x)[2]
    #if (is.null(tot)) {i = 2}
    #else {i = 3}
    #X = as.matrix(x[,i:ncol])
    #rownames(X) = x[,1]
    corData = cora(X)
    par(mfrow= c(2,2))
    plcora(corData,axis1=1,axis2=2)
    plcora(corData,axis1=2,axis2=3)
    plcora(corData,axis1=1,axis2=3)
    plinert(corData)
 }

cora.integrity <- function(cont.tab, sup.row, sup.col, warn=T)
{
    message <- setup.language(c("eng", "fr", "ger"), c(
      "row",
      "column",
      "supl. row",
      "supl. column",
      "'cont.tab' is not a matrix",
      "'cont.tab' and 'sup.row' haven't the same number of columns",
      "'cont.tab' and 'sup.col' haven't the same number of rows",
      "ligne",
      "colonne",
      "ligne supl.",
      "colonne supl.",
      "'cont.tab' n'est pas une matrice",
      "'cont.tab' et 'sup.row' n'ont pas le meme nombre de colonnes",
      "'cont.tab' et 'sup.col' n'ont pas le meme nombre de lignes",

      "",
      "",
      "",
      "",
      "",
      "",
      ""), warn)
  
  if (!is.matrix(cont.tab)) stop(message[5])

  tdn <- dimnames(cont.tab)
  if (is.null(tdn)) tdn <- list()
  if (length(tdn[[1]]) == 0) tdn[[1]] <- paste(message[1], 1:nrow(cont.tab))
  if (length(tdn[[2]]) == 0) tdn[[2]] <- paste(message[2], 1:ncol(cont.tab))

  if (!is.null(sup.row))
    {
      if (!is.matrix(sup.row)) sup.row <- t(as.matrix(sup.row))
      if (ncol(cont.tab) != ncol(sup.row)) stop(message[6])
      rdn <- dimnames(sup.row)
      if (length(rdn[[1]]) == 0) rdn[[1]] <- paste(message[3], 1:nrow(sup.row))
      if (length(rdn[[2]]) == 0) rdn[[2]] <- tdn[[2]]
      dimnames(sup.row) <- rdn
    }

  if (!is.null(sup.col))
    {
      if (!is.matrix(sup.col)) sup.col <- as.matrix(sup.col)
      if (nrow(cont.tab) != nrow(sup.col)) stop(message[7])
      cdn <- dimnames(sup.col)
      if (length(cdn[[1]]) == 0) cdn[[1]] <- tdn[[1]]
      if (length(cdn[[2]]) == 0) cdn[[2]] <- paste(message[4], 1:ncol(sup.col))
      dimnames(sup.col) <- cdn
    }

  list(tdn=tdn, sup.row=sup.row, sup.col=sup.col)
}

cora <- function(cont.tab, sup.row=NULL, sup.col=NULL)
{  
  x <- cora.integrity(cont.tab, sup.row, sup.col)
  dimnames(cont.tab) <- x$tdn
  sup.row <- x$sup.row
  sup.col <- x$sup.col


#Analysis on 'cont.tab'

  tab.dim <- dim(cont.tab)
  axes.nb <- min(tab.dim) - 1
  tab.sum <- sum(cont.tab)
  pi <- apply(cont.tab, 1, sum)
  pj <- apply(cont.tab, 2, sum)
  row.mass <- pi / tab.sum
  col.mass <- pj / tab.sum
  tab.exp <- outer(row.mass, col.mass)
  cont.tab <- ((cont.tab / tab.sum) - tab.exp) / sqrt(tab.exp)

  tab.svd <- svd(cont.tab)

  svalues <- tab.svd$d[1:axes.nb]
  cora.val <- matrix(0.0, nrow=axes.nb, ncol=2)
  cora.val[,1] <- svalues^2
  cora.val[,2] <- cora.val[,1] / sum(cora.val[,1])

  dimnames(cora.val) <- c(list(paste("Axis", 1:axes.nb)),
                          list(c("inertia", "percent")))

  row.ac <- as.matrix(tab.svd$u[, 1:axes.nb] / sqrt(row.mass))
  col.ac <- as.matrix(tab.svd$v[, 1:axes.nb] / sqrt(col.mass))

  cora.data <- array(0.0, dim=c(sum(tab.dim), axes.nb, 3))

  dimnames(cora.data)[3] <- list(c("coord", "relcont", "abscont"))
  dimnames(cora.data)[2] <- list(paste("Axis", 1:axes.nb))
  dimnames(cora.data)[1] <- list(c(dimnames(cont.tab)[[2]],
                                   dimnames(cont.tab)[[1]]))

  row.c <- t(svalues * t(row.ac))
  col.c <- t(svalues * t(col.ac))

  cora.data[1:tab.dim[2],,1]                  <- col.c
  cora.data[(tab.dim[2] + 1):sum(tab.dim),,1] <- row.c

  cora.data[1:tab.dim[2],,3]                  <- col.mass * col.ac^2
  cora.data[(tab.dim[2] + 1):sum(tab.dim),,3] <- row.mass * row.ac^2

  cora.data[1:tab.dim[2],,2] <-
      (col.c^2) * col.mass / apply(cont.tab^2, 2, sum)
  cora.data[(tab.dim[2] + 1):sum(tab.dim),,2] <-
      (row.c^2) * row.mass / apply(cont.tab^2, 1, sum)

  data.name <- c(cont.tab=deparse(substitute(cont.tab)))

#Supplementary rows

  if (is.null(sup.row)) cora.sup.row <- NULL
  else
    {
      cora.sup.row <- array(0.0, dim=c(nrow(sup.row), axes.nb, 2))
      dimnames(cora.sup.row)[3] <- list(c("coord", "cont"))
      dimnames(cora.sup.row)[2] <- list(paste("Axis", 1:axes.nb))
      dimnames(cora.sup.row)[1] <- list(dimnames(sup.row)[[1]])

      pip <- apply(sup.row, 1, sum)
      sup.row.c <- (sup.row / pip) %*% col.ac
      cora.sup.row[,,1] <- sup.row.c
      cora.sup.row[,,2] <- cora.cos.sqr(sup.row, pip, pj, tab.sum,
                                        sup.row.c, axes.nb)

      data.name <- c(data.name, sup.row=deparse(substitute(sup.row)))
    }


#Supplementary cols

  if (is.null(sup.col)) cora.sup.col <- NULL
  else
    {
      cora.sup.col <- array(0.0, dim=c(ncol(sup.col), axes.nb, 2))
      dimnames(cora.sup.col)[3] <- list(c("coord", "cont"))
      dimnames(cora.sup.col)[2] <- list(paste("Axis", 1:axes.nb))
      dimnames(cora.sup.col)[1] <- list(dimnames(sup.col)[[2]])

      pip <- apply(sup.col, 2, sum)
      sup.col.c <- (t(sup.col) / pip) %*% row.ac
      cora.sup.col[,,1] <- sup.col.c
      cora.sup.col[,,2] <- cora.cos.sqr(t(sup.col), pip, pi, tab.sum,
                                        sup.col.c, axes.nb)

      data.name <- c(data.name, sup.col=deparse(substitute(sup.col)))
    }

  list(data=cora.data,
       suprow=cora.sup.row,
       supcol=cora.sup.col,
       inert=cora.val,
       tabdim=tab.dim,
       data.name=data.name)
}

cora.cos.sqr <- function(sup.x, pi, pj, tab.sum, sup.x.c, axes.nb)
{
  ni <- nrow(sup.x)
  nj <- ncol(sup.x)
  project <- matrix(pj / tab.sum, byrow=T, ncol=nj, nrow=ni)
  z <- sup.x / pi - project
  di <- apply(z * z / project, 1, sum)
  cont <- (sup.x.c ^ 2) / di
  cont
}

# Misc. data  V3.0  6th Oct 1992          Centre de Recherche Public   #
#                                          - Centre Universitaire -    #
# - Language support                     162a, Avenue de la Faiencerie #
# - Unit support                               L-1511 Luxembourg       #
#                                            Tel: (+352) 47 02 61      #
#                                            Fax: (+352) 47 02 64      #
#                                                                      #
#                                            IABD Project - CREDI      #
#                                            --------------------      #
#                                                                      #
#                                          N. Beaumont - R. Bisdorff   #
#                                            F. Fehlen - B. Perbal     #



lang.warn <- c(
    "No language option found. To select a language, use the S-PLUS\n",
    "function options() with the language argument set to a particular\n",
    "language. (e.g. options(language=\"eng\")). Typical language abbr.\n",
    "are \"eng\", \"fr\" or \"ger\".\n")

unit.warn <- c(
    "No unit option found. To select a unit, use the S-PLUS function\n",
    "options() with the unit argument set to a known unit: \"pt\", \"inch\",\n",
    "\"cm\" or \"mm\". (e.g. options(unit=\"cm\"))\n")


# Misc. functions  V3.1  20th Nov 1992    Centre de Recherche Public   #
#                                          - Centre Universitaire -    #
# - Language support                     162a, Avenue de la Faiencerie #
# - Unit support                               L-1511 Luxembourg       #
#                                            Tel: (+352) 47 02 61      #
#                                            Fax: (+352) 47 02 64      #
#                                                                      #
#                                            IABD Project - CREDI      #
#                                            --------------------      #
#                                        #
#N. Beaumont - R. Bisdorff   #
#                                            F. Fehlen - B. Perbal     #


setup.language <- function(lang.abbr, lang.msg, warn=T)
{
  lang.current <- options()$language

  if (is.null(lang.current))
    {
      if (warn) option.warning(lang.warn)
      lang.i <- 1
    }
  else
    {
      lang.i <- match(lang.current, lang.abbr)
      if (is.na(lang.i)) lang.i <- 1
    }

  lang.msg.nb <- length(lang.msg) %/% length(lang.abbr)

  lang.msg[(lang.i - 1) * lang.msg.nb + (1:lang.msg.nb)]
}
  
unit.convert <- function(unit.dest, warn=T)
{
  unit.name <- c("pt", "inch", "cm", "mm")
  unit.def  <- c(1.0, 72.0, 28.3464567, 2.83464567)

  unit.current <- options()$unit

  if (is.null(unit.current))
    {
      if (warn) option.warning(unit.warn)
      unit.sr.i <- 1
    }
  else
    {
      unit.sr.i <- match(unit.current, unit.name)
      if (is.na(unit.sr.i)) unit.sr.i <- 1
    }

  unit.dt.i <- match(unit.dest, unit.name)
  if (is.na(unit.dt.i)) unit.dt.i <- 1

  unit.def[unit.sr.i] / unit.def[unit.dt.i]
}

option.warning <- function(warn)
{
  cat(warn, sep="")
}



#plcora  V4.1 1th Octobre 1993           Centre de Recherche Public   #
#                                          - Centre Universitaire -    #
# This S function plots                  162a, Avenue de la Faiencerie #
# the result of 'cora'                         L-1511 Luxembourg       #
# on the standard device                     Tel: (+352) 47 02 61      #
#                                            Fax: (+352) 47 02 64      #
# modified by ff                                                       #
#                                            IABD Project - FRONT      #
#                                            --------------------      #
#     update of                                                        #
#  V4.0 1th July 1993                        R. Bisdorff - F. Fehlen   #
#                                                  E.Jacquemart       #


plcora.exit <- function(old.par, old.opt, ps, old.ps.opt)
{
  par(old.par)
  par(new=F)
  options(old.opt)
  if (ps)
    {
      dev.off()
      ps.options(old.ps.opt)
    }
}

plcora <- function (x,
                    axis1    = 1,
                    axis2    = 2,
                    rmin     = 0.5,
                    cmin     = 0.5,
                    mthd     = "persp",
                    magnify  = 1.0,
                    zoom,
                    xmax, xmin,
                    ymax, ymin,
                    ps       = F,
                    warn     = T,
                    file     = "",
                    flipx    = F,
                    flipy    = F,
                    main     = "")
{
  message <- setup.language(c("eng", "fr", "ger"), c(
      "contribution",
      "The label size is proportional to the quality of the representation in the plane",
      "The label size is proportional to the quality of the representation on the horizontal axis",
      "The label size is proportional to the contribution to the horizontal axis",
      "Numbers are measuring the quality of the representation on the horizontal axis\n= squared cosine of the angle between the point and the horizontal axis * 1000",
      "Numbers are measuring the contribution of the point to the inertia of the horizontal axis\n= absolute contribution * 1000",
      "(=sum of relative contribution for all axes)",
      "(=sum of the absolute contribution for all line- resp. column-points)",

      "contribution:",
      "La taille du texte est proportionnelle a la qualite de la representation dans le plan",
      "La taille du texte est proportionnelle a la qualite de la representation sur l'axe horizontal",
      "La taille du texte est proportionnelle a la contribution a l'axe horizontal",
      "Les chiffres mesurent la qualite de la representation sur l'axe horizontal\n= cosinus carre de l'angle du point sur l'axe horizontal * 1000",
      "Les chiffres mesurent la contribution du point a l'inertie de l'axe horizontal\n= la contribution absolue * 1000",
      "(=somme des contributions relatives pour tous les axes)",
      "(=somme des contributions relatives pour tous les points lignes , resp. points-colonnes)",

      "",
      "",
      "",
      "",
      "",
      "",
      "",
      ""), warn)

  ps.opt <- NULL

  if (ps)
    {
      ps.opt <- ps.options()
      ps.options(horizontal=T, region=c(16,16,578,824),
                 setfont=ps.setfont.latin1)
      postscript(file=file)
    }

  #old.opt <- options()
  #old.par <- par ()

  #on.exit(plcora.exit(old.par, old.opt, ps, ps.opt))

  #options(warn = -1)
  #par(oma=c(1,0,3,0))

 
  # mirror-option
     if (flipx == T)
        x$data[,axis1,1]<-x$data[,axis1,1]*(-1)
     if (flipy == T)
        x$data[,axis2,1]<-x$data[,axis2,1]*(-1)


  if (missing(xmax))  xmax <- max(x$data[,axis1,1])
  if (missing(xmin))  xmin <- min(x$data[,axis1,1])                   
  if (missing(ymax))  ymax <- max(x$data[,axis2,1])
  if (missing(ymin))  ymin <- min(x$data[,axis2,1])

  if (!missing(zoom))
    { 
      xmin <- zoom[1]
      xmax <- zoom[2]
      ymin <- zoom[3]
      ymax <- zoom[4]
     }
  
  plot(x$data[,axis1,1],
       x$data[,axis2,1],
       pch=" ",
       xlim=c(xmin, xmax),
       ylim=c(ymin, ymax),
       xlab=paste(message[1],"\n",(dimnames(x$data)[[2]][axis1]),
                  " ",
                  round(x$inert[axis1,2], 4),
                  sep=""),
       ylab=paste(message[1],"\n",(dimnames(x$data)[[2]][axis2]),
                  " ",
                  round(x$inert[axis2,2], 4),
                  sep=""),cex=par('cex')*.6)
  title(main)
  nc <- x$tabdim[2]
  nr <- x$tabdim[1]

# setting up threshold-vector

  thresh<-c(rep(cmin,nc),rep(rmin,nr))

# default height for labels
 
  hlabels<- rep(par('cex'),nc+nr)
  
# default label-text

  tlabels<-dimnames(x$data)[[1]]
 
  if (mthd == "no")    mthd <- 0
  if (mthd == "persp") mthd <- 1
  if (mthd == "rep")   mthd <- 2 
  if (mthd == "ctr")   mthd <- 3
  if (mthd == "repn")  mthd <- 4
  if (mthd == "ctrn")  mthd <- 5 



# modify hlabels corresponding to the different methods

if (mthd == 1)
          hlabels<- x$data[,axis1,2]+ x$data[,axis2,2]       

if (mthd == 2)
          hlabels<- x$data[,axis1,2]     
 
if (mthd == 3)
          hlabels<-c(x$data[1:nc,axis1,3]/max(x$data[1:nc,axis1,3]),
                          x$data[(nc+1):(nc+nr),axis1,3]/
                          max(x$data[(nc+1):(nc+nr),axis1,3]))

# modifie tlabels corresponding to the different methods

  if ((mthd == 4) || (mthd == 5))
           tlabels<-paste(dimnames(x$data)[[1]],
                         as.integer(x$data[,axis1,(mthd - 2)] * 1000))
             
# preparing htresh to eliminate the values below threshold 
# whith a subscript: sub = (hthresh > thresh)

hthresh <- hlabels


if (mthd == 4)
        hthresh <- x$data[,axis1,2]

if  (mthd == 5)
        hthresh <- x$data[,axis1,3]/mean(x$data[,axis1,3]) * .5

sub <- hthresh > thresh

# plotting labels with different fonts for columns and rows

  text(x$data[1:nc,axis1,1][sub[1:nc]], 
       x$data[1:nc,axis2,1][sub[1:nc]],
       cex = hlabels [1:nc][sub[1:nc]] * magnify ,
       font = 2,
       labels=tlabels [1:nc] [sub[1:nc]])
                      
  text(x$data[(nc+1):(nc+nr),axis1,1][sub[(nc+1):(nc+nr)]],  
       x$data[(nc+1):(nc+nr),axis2,1][sub[(nc+1):(nc+nr)]],
       cex = hlabels[(nc+1):(nc+nr)][sub[(nc+1):(nc+nr)]] * magnify ,
       font = 3,col="red",
       labels=tlabels[(nc+1):(nc+nr)][sub[(nc+1):(nc+nr)]] )
        

 # adding comments

  ## if (mthd == 1) 
  ##     title(main=paste("\n\n\n(", message[2], ")", sep=""), cex=.5) 
      
  ## if (mthd == 2) title(main=paste("\n\n\n(", message[3], ")", sep=""), cex=.5)

  ## if (mthd == 3) title(main=paste("\n\n\n(", message[4], ")", sep=""), cex=.5)

  ## if (mthd == 4) title(main=paste("\n\n\n(", message[5], ")",  sep=""), cex=.5)

  ## if (mthd == 5) title(main=paste("\n\n\n(", message[6], ")",  sep=""), cex=.5)
  
  ## mtext("CRP-CU 1994         ",side =3,outer= T, line=-4,adj=1,cex=0.8)
  ## invisible()
}

 #########################################################################
#  mplcora  V4.0 6th Octobre 1993          Centre de Recherche Public   #
#                                           - Centre Universitaire -    #
#  This S function plots                  162a, Avenue de la Faiencerie #
#        4 graphs                               L-1511 Luxembourg       #
#  on the standard device                     Tel: (+352) 47 02 61      #
#                                             Fax: (+352) 47 02 64      #
#            ff                                                         #
#                                             IABD Project - FRONT      #
#                                             --------------------      #
#                                                                       #
#                                             R. Bisdorff - F. Fehlen   #
#                                                    E.Jacquemart       #
#########################################################################

mplcora.exit <- function(old.par, old.opt, ps, old.ps.opt)
{
  par(old.par)
  par(new=F)
  options(old.opt)
  if (ps)
    {
      dev.off()
      ps.options(old.ps.opt)
    }
}

mplcora  <- function (x,
                    axis1    = 1,
                    axis2    = 2,
                    rmin     = 0.7,
                    cmin     = 0.7,
                    mthd     = "persp",
                    magnify  = .8,
                    zoom,
                    xmax, xmin,
                    ymax, ymin,
                    ps       = F,
                    warn     = T,
                    file     = "",
                    flipx    = F,
                    flipy    = F,
                    main     = "",
                    rlevel   = 5,
                    clevel   = 5,
#                    main     = "",
                    ...)
{
  message <- setup.language(c("eng", "fr", "ger"), c(
       "Identification of axis", "","axis ",
       "Contr. absolues * 1000\nIdentification de l'axe","Representation dans le plan","axe ",
       "","",""), warn)

   #ps.opt <- NULL

   #if (ps)
   #  {
   #    ps.opt <- ps.options()
   #    ps.options(horizontal=T, region=c(16,16,578,824),
   #               setfont=ps.setfont.latin1)
   #    postscript(file=file)
   #  }

   #old.opt <- options()
   #old.par <- par ()

   #on.exit(mplcora.exit(old.par, old.opt, ps, ps.opt))

   #options(warn = -1)
message = ' '   
par(mfrow = c(2, 2))
par(cex=.5)
plinert(x, txt=main, ...)
plcora.small(x,
         axis1,
         axis2,
         mthd="ctrn",
         cmin=mean(x$data[1:x$tabdim[2], axis1, 3]) * clevel,
         rmin=mean(x$data[(x$tabdim[2] + 1):(x$tabdim[1] + x$tabdim[2]),
                   axis1, 3]) * rlevel,
         warn = F,
         main = paste(message[1], axis1),
         magnify = magnify,
         ...)
frame()
frame()
plcora.small(x,
         axis1,
         axis2,
         magnify=magnify*.9,
         main=paste(message[2],"\n",message[3],axis1," - ",message[3],axis2),
         ...)


plcora.small(x,
         axis2,
         axis1,
         mthd="ctrn",
         cmin=mean(x$data[1:x$tabdim[2], axis1, 3]) * clevel,
         rmin=mean(x$data[(x$tabdim[2] + 1):(x$tabdim[1] + x$tabdim[2]),
                   axis1, 3]) * rlevel,
         warn = F,
         main = paste(message[1], axis2),
         magnify = magnify,
         ...)
    
#   invisible()
}

 

#########################################################################
#  plcora.small  V4.1 6th Octobre 1993     Centre de Recherche Public   #
#                                           - Centre Universitaire -    #
#  This S function plots                  162a, Avenue de la Faiencerie #
#  the result of 'cora'                         L-1511 Luxembourg       #
#  on the standard device                     Tel: (+352) 47 02 61      #
#   whithout comments                         Fax: (+352) 47 02 64      #
#   modified by ff                                                      #
#                                             IABD Project - FRONT      #
#     to be used with mplcora                 --------------------      #
#      update of                                                        #
#   V4.0 1th July 1993                        R. Bisdorff - F. Fehlen   #
#                                                    E.Jacquemart       #
#########################################################################

plcora.exit <- function(old.par, old.opt, ps, old.ps.opt)
{
  par(old.par)
  par(new=F)
  options(old.opt)
  if (ps)
    {
      dev.off()
      ps.options(old.ps.opt)
    }
}

plcora.small <- function (x,
                    axis1    = 1,
                    axis2    = 2,
                    rmin     = 0.5,
                    cmin     = 0.5,
                    mthd     = "persp",
                    magnify  = 1.0,
                    zoom,
                    xmax, xmin,
                    ymax, ymin,
                    ps       = F,
                    warn     = T,
                    file     = "",
                    flipx    = F,
                    flipy    = F,
                    main     = "")
{
  message <- setup.language(c("eng", "fr", "ger"), c(
      "axis ",
      "The label size is proportional to the quality of the representation in the plane",
      "The label size is proportional to the quality of the representation on the horizontal axis",
      "The label size is proportional to the contribution to the horizontal axis",
      "Numbers are measuring the quality of the representation on the horizontal axis\n= squared cosine of the angle between the point on the horizontal axis * 1000",
      "Numbers are measuring the contribution of the point to the inertia of the horizontal axis\n= absolute contribution * 1000",
      "(=sum of relative contribution for all axes)",
      "(=sum of the absolute contribution for all line- resp. column-points)",

      "axe ",
      "La taille du texte est proportionnelle a la qualite de la representation dans le plan",
      "La taille du texte est proportionnelle a la qualite de la representation sur l'axe horizontal",
      "La taille du texte est proportionnelle a la contribution a l'axe horizontal",
      "Le valeurs mesurent la qualite de la representation sur l'axe horizontal\n= cosinus carre de l'angle du point sur l'axe horizontal * 1000",
      "Les valeurs mesurent la contribution du point e l'inertie de l'axe horizontal\n= la contribution absolue * 1000",
      "(=somme des contributions relatives pour tous les axes)",
      "(=somme des contributions relatives pour tous les points lignes , resp. points-colonnes)",

      "",
      "",
      "",
      "",
      "",
      "",
      "",
      ""), warn)

  ps.opt <- NULL

  if (ps)
    {
      ps.opt <- ps.options()
      ps.options(horizontal=T, region=c(16,16,578,824),
                 setfont=ps.setfont.latin1)
      postscript(file=file)
    }

  old.opt <- options()
  old.par <- par ()

  on.exit(plcora.exit(old.par, old.opt, ps, ps.opt))

  options(warn = -1)
   
   # mirror-option
     if (flipx == T)
        x$data[,axis1,1]<-x$data[,axis1,1]*(-1)
     if (flipy == T)
        x$data[,axis2,1]<-x$data[,axis2,1]*(-1)


  if (missing(xmax))  xmax <- max(x$data[,axis1,1])
  if (missing(xmin))  xmin <- min(x$data[,axis1,1])                   
  if (missing(ymax))  ymax <- max(x$data[,axis2,1])
  if (missing(ymin))  ymin <- min(x$data[,axis2,1])

  if (!missing(zoom))
    { 
      xmin <- zoom[1]
      xmax <- zoom[2]
      ymin <- zoom[3]
      ymax <- zoom[4]
     }
  
  plot(x$data[,axis1,1],
       x$data[,axis2,1],
       pch=" ",
       xlim=c(xmin, xmax),
       ylim=c(ymin, ymax),
       xlab=paste(  message[1],axis1 , ": " ,
                  round(x$inert[axis1,2], 2) *100,"%",
                  sep="") ,
       ylab=paste(   message[1],axis2 , ": " ,
                  round(x$inert[axis2,2], 2) *100,"%",
                  sep=""),cex=par('cex')*.8)
  title(main)
  nc <- x$tabdim[2]
  nr <- x$tabdim[1]

# setting up threshold-vector

  thresh<-c(rep(cmin,nc),rep(rmin,nr))

# default height for labels
 
  hlabels<- rep(par('cex'),nc+nr)
  
# default label-text

  tlabels<-dimnames(x$data)[[1]]
 
  if (mthd == "no")    mthd <- 0
  if (mthd == "persp") mthd <- 1
  if (mthd == "rep")   mthd <- 2 
  if (mthd == "ctr")   mthd <- 3
  if (mthd == "repn")  mthd <- 4
  if (mthd == "ctrn")  mthd <- 5 



# modify hlabels corresponding to the different methods

if (mthd == 1)
          hlabels<- x$data[,axis1,2]+ x$data[,axis2,2]       

if (mthd == 2)
          hlabels<- x$data[,axis1,2]     
 
if (mthd == 3)
          hlabels<-c(x$data[1:nc,axis1,3]/max(x$data[1:nc,axis1,3]),
                          x$data[(nc+1):(nc+nr),axis1,3]/
                          max(x$data[(nc+1):(nc+nr),axis1,3]))

# modifie tlabels corresponding to the different methods

  if ((mthd == 4) || (mthd == 5))
           tlabels<-paste(dimnames(x$data)[[1]],
                         as.integer(x$data[,axis1,(mthd - 2)] * 1000))
             
# preparing htresh to eliminate the values below threshold 
# whith a subscript: sub = (hthresh > thresh)

hthresh <- hlabels


if (mthd == 4)
        hthresh <- x$data[,axis1,2]

if  (mthd == 5)
        hthresh <- x$data[,axis1,3]/mean(x$data[,axis1,3]) * .5

sub <- hthresh > thresh

# plotting labels with different fonts for columns and rows

  text(x$data[1:nc,axis1,1][sub[1:nc]], 
       x$data[1:nc,axis2,1][sub[1:nc]],
       cex = hlabels [1:nc][sub[1:nc]] * magnify ,
       font = 2,
       labels=tlabels [1:nc] [sub[1:nc]])
                      
  text(x$data[(nc+1):(nc+nr),axis1,1][sub[(nc+1):(nc+nr)]],  
       x$data[(nc+1):(nc+nr),axis2,1][sub[(nc+1):(nc+nr)]],
       cex = hlabels[(nc+1):(nc+nr)][sub[(nc+1):(nc+nr)]] * magnify ,
       font = 3,
       labels=tlabels[(nc+1):(nc+nr)][sub[(nc+1):(nc+nr)]] )
        

     invisible()
}
#########################################################################
#  plinert  V3.1  20th Nov 92              Centre de Recherche Public   #
#                                           - Centre Universitaire -    #
#  This S function plots                  162a, Avenue de la Faiencerie #
#  the principal inertias                       L-1511 Luxembourg       #
#  as bar graph                               Tel: (+352) 47 02 61      #
#                                             Fax: (+352) 47 02 64      #
#                                                                       #
#                                             IABD Project - CREDI      #
#                                             --------------------      #
#                                                                       #
#                                           N. Beaumont - R. Bisdorff   #
#                                             F. Fehlen - B. Perbal     #
#########################################################################

plinert <- function (x,
                     txt      = message[1],
                     nbaxes   = 5,
                     lim      = inert[1],
                     warn     = T)
{
  message <- setup.language(c("eng", "fr", "ger"), c(
      "Correspondence analysis",
      "Axis",
      "",

      "Analyse des correspondances",
      "Axe",
      "Pourcentage de l'information expliquee par les axes",

      "",
      "",
      ""), warn)

  if (nbaxes > min(x$tabdim) - 1) nbaxes <- min(x$tabdim) - 1

  inert <- round(x$inert[1:nbaxes,2] * 100, 1)

  barplot(inert,
          names = paste(message[2], " ", 1:nbaxes, "\n",
                        inert[1:nbaxes], " %", sep=""),
          xlab = message[3],
          main = txt,
          ylim = c(0, lim))

  invisible()
}


 
#########################################################################
#  printtab  V3.1  20th Nov 92             Centre de Recherche Public   #
#                                           - Centre Universitaire -    #
#  This S function makes up               162a, Avenue de la Faiencerie #
#  a table from a matrix and                    L-1511 Luxembourg       #
#  then prints it on the                      Tel: (+352) 47 02 61      #
#  PostScript device                          Fax: (+352) 47 02 64      #
#                                                                       #
#                                             IABD Project - CREDI      #
#                                             --------------------      #
#                                                                       #
#                                           N. Beaumont - R. Bisdorff   #
#                                             F. Fehlen - B. Perbal     #
#########################################################################


#########################################################################
# printtab.exit: Restore Graphical Parameters and Device on exit	#
# Params: ps:	Boolean value: True: PostScript device used		#
#		               False: Default device used		#
#         f:	List of all Graphical Parameters			#
# Return: (nothing)							#
#########################################################################

printtab.exit <- function(f, ps, ps.opt)
{
  par(f)				# Restores Graph. Params.
  if (ps) 
    {
      dev.off()			# Restores default device
      ps.options(ps.opt)
    }
}

#########################################################################
# printtab: Makes up a table from a matrix and then prints it on the	#
#           PostScript device						#
# Params: (see documentation and on-line help)				#
# Return: (nothing)							#
#########################################################################

printtab <- function(data,
                     file     = "",
                     thresh   = F,
                     thtype   = "size",
                     percent  = T,
                     pos      = c(57, 43, 43, 43) / unit.factor,
                     horiz    = F,
                     dimwidth = cu * 15 / unit.factor,
                     width    = cu * 5 / unit.factor,
                     lspace   = cu / unit.factor,
                     frm      = T,
                     cex      = par("cex"),
                     font     = par("font"),
                     boldfont = bold[font],
                     adj      = par("adj"),
                     ps       = F,
                     warn     = T,
                     region   = c(16, 16, 578, 824) / unit.factor,
                     func     = NULL,
                     ...)		# See on-line help for details
{
  message <- setup.language(c("eng", "fr", "ger"),
                            c("Page", "Page", "Seite"),
                            warn)

# The three following lines are necessary to force the evaluation
# of these arguments before the postscript() function overwrites them.

  cex  <- cex
  font <- font
  adj  <- adj

  unit.factor <- unit.convert("pt", warn)
  region <- region * unit.factor
  ps.opt <- NULL

  if (ps)
    {
      ps.opt <- ps.options()
      ps.options(horizontal=horiz, region=region, setfont=ps.setfont.latin1)
      postscript(file=file)	# Sends graphics to PostScript if asked
    }

  f <- par()				# Saves Graph. Params.
  on.exit(printtab.exit(f, ps, ps.opt))	# Calls printtab.exit on exit

  bold <- c(5, 8, 11, 6, 1, 4, 9, 2, 7, 12, 3, 10, 13, 16, 17, 14, 15, 20, 21,
            18, 19, 23, 22, 25, 24, 27, 26, 29, 28, 31, 30, 33, 32, 33, 35)

	# This vector holds standard PostScript font numbers.
	# Those numbers refer to the default PostScript font
	# names in the 'ps.fonts' vector. For a given font type,
	# they give the corresponding enhanced text font number.
	# e.g. the enhanced font for Helvetica (index 1 in
	# 'ps.fonts') is Helvetica-Bold (index 5 in 'ps.fonts'),
	# so its number (5) is placed in the first position
	# of the 'bold' vector. Conversely, the fifth element of
	# the 'bold' vector is 1.

  par(cex=cex)				# Sets character expansion
  par(font=font)			# Sets font
  par(mai=c(0, 0, 0, 0))		# Sets margin size

  cu <- cex * 14			# Character unity

  pos <- pos * unit.factor
  width <- width * unit.factor
  dimwidth <- dimwidth * unit.factor
  lspace <- lspace * unit.factor

  pd <- par("pin") * 72			# Plot dim in points
  par(usr=c(0, pd[1], 0, pd[2]))	# Coord in points

  nr <- nrow(data)		# Total number of rows
  nc <- ncol(data)		# Total number of cols

  x1 <- pos[1]			# Horiz. left position of the dimension col.
  x2 <- x1 + dimwidth		# Horiz. left position of the first data col.
  x3 <- x2 + nc * width		# Horiz. right position of the last data col.

  if (x3 > pd[1] - pos[3])	# If x3 is out of the page
    {
      nc <- (pd[1] - pos[3] - x2) %/% width  # Recalculate number of cols
      x3 <- x2 + nc * width		     # Recalculate x3
    }

  y1 <- pd[2] - pos[2]		# Top vert. pos. of header line
  y2 <- y1 - 2 * lspace		# Top vert. pos. of the first data line

  nlfp <- (y2 - pos[4]) %/% lspace - 1	# Num. of lines on full page
  nfp  <- nr %/% nlfp			# Num. of full pages
  nllp <- nr %% nlfp			# Num. of lines on last page

  y3fp <- y2 - (nlfp + 1) * lspace	# Bottom vert. pos. of the last
					# data line on full page
  y3lp <- y2 - (nllp + 1) * lspace	# Bottom vert. pos. of the last
					# data line on last page

  xp <- x2 + cu + adj * (width - 2 * cu) + ((1:nc) - 1) * width
					# X positions
  if (length(thresh) > 1)		# If multiple threshold
    {
      thresh <- rep(thresh, ((nc - 1) %/% length(thresh)) + 1)[1:nc]
			# Sets up threshold vector
      if (percent)	# If threshold is percent of maximum col. value
        {
          for (i in 1:nc) thresh[i] <- thresh[i] * max(data[,i])
        }
    }
  else if ((!is.logical(thresh)) && percent) thresh <- thresh * max(data)
        
  funcattr <- list(data=data, thresh=thresh, pagesize=pd,
                   tablemin=c(0,0), tablemax=c(x3,y1),
                   dimwidth=dimwidth, width=width, lspace=lspace,
                   frm=frm, charunit=cu, pagenumber=0, nbcol=nc,
                   nbrow=0, firstrow=0)
                                                # Sets up 'func' params

  fdata <- format(round(data, options()$digits))

  if (nfp > 0)
    {
      funcattr$tablemin <- c(x1, y3fp)		# Sets up 'tablemin' list
						# element for a full page
      funcattr$nbrow <- nlfp			# Sets up 'nbrow' list
						# element for a full page

      xpm <- matrix(rep(xp, nlfp), ncol=nc, byrow=T)	# Matrix of horiz.
							# pos. for all data's
      yp <- y2 - (1:nlfp) * lspace		# Vector of vert. pos.
						# for one col. of data's
      ypm <- matrix(rep(yp, nc), ncol=nc)	# Matrix of vert. pos.	
						# for all data's
      for (pg in 1:nfp)
        {
          frame()

          if (frm)		# Draws the frame if needed
            {
              lines(c(x1, x3, x3, x1, x1), c(y1, y1, y3fp, y3fp, y1))
              lines(c(x1, x3), c(y2, y2))
              lines(c(x2, x2), c(y1, y3fp))
            }

          par(adj=1)					# Right justif.
          text(x2 - cu, y1 - lspace, paste(message[1], pg))
                                                        # Prints 'Page #'

          iy <- (1:nlfp) + (pg - 1) * nlfp		# Vert. data indexes

          text(x2 - cu, yp, dimnames(data)[[1]][iy])	# Prints vert. dimnames
          par(adj=adj)					# Resets justif.

          text(xp, y1 - lspace, dimnames(data)[[2]][1:nc])  # Horiz. dimnames

          if (!is.logical(thresh))		# If threshold specified
            {
              if (length(thresh) == 1)		# If unique threshold
                {
                  filter <- data[iy, 1:nc] >= thresh  # Upper selection filter
                  if (any(filter))		      # If any filter el. true
                    {
                      if (thtype == "size")	      # If size representation
                          text(as.vector(xpm)[filter],
                               as.vector(ypm)[filter],
                               as.vector(fdata[iy, 1:nc])[filter])
                      else
                          text(as.vector(xpm)[filter],    # else font repres.
                               as.vector(ypm)[filter],
                               as.vector(fdata[iy, 1:nc])[filter],
                               font=boldfont)
                    }

                  filter <- !filter		# Lower selection filter
                  if (any(filter))		# If any filter element true
                    {
                      if (thtype == "size")	      # If size representation
                          text(as.vector(xpm)[filter],
                               as.vector(ypm)[filter],
                               as.vector(fdata[iy, 1:nc])[filter],
                               cex=.7 * par("cex"))
                      else
                          text(as.vector(xpm)[filter],    # else font repres.
                               as.vector(ypm)[filter],
                               as.vector(fdata[iy, 1:nc])[filter])
                    }
                }
              else				# else multiple threshold
                {
                  for (cl in 1:nc)		# Do the same work as previous
                    {				# on each column
                      filter <- data[iy, cl] >= thresh[cl]
                      if (any(filter))
                        {
                          if (thtype == "size")
                              text(xp[cl],
                                   yp[filter],
                                   as.vector(fdata[iy, cl])[filter])
                          else
                              text(xp[cl],
                                   yp[filter],
                                   as.vector(fdata[iy, cl])[filter],
                                   font=boldfont)
                        }

                      filter <- !filter
                      if (any(filter))
                        {
                          if (thtype == "size")
                              text(xp[cl],
                                   yp[filter],
                                   as.vector(fdata[iy, cl])[filter],
                                   cex=.7 * par("cex"))
                          else
                              text(xp[cl],
                                   yp[filter],
                                   as.vector(fdata[iy, cl])[filter])
                        }
                    }
                }
            }

          else text(xpm, ypm, fdata[iy, 1:nc])	# No threshold

          if (!is.null(func))			# Calls 'func' if not NULL
            {
              savef <- par()
              funcattr$pagenumber <- pg
              funcattr$firstrow <- (pg - 1) * nlfp + 1
              func(funcattr=funcattr, ...)
              par(savef)
            }
        }
    }

  if (nllp > 0)		# Do the same work for the last page
    {
      xpm <- matrix(rep(xp, nllp), ncol=nc, byrow=T)
      yp <- y2 - (1:nllp) * lspace
      ypm <- matrix(rep(yp, nc), ncol=nc)

      frame()

      if (frm)
        {
          lines(c(x1, x3, x3, x1, x1), c(y1, y1, y3lp, y3lp, y1))
          lines(c(x1, x3), c(y2, y2))
          lines(c(x2, x2), c(y1, y3lp))
        }

      par(adj=1)
      text(x2 - cu, y1 - lspace, paste(message[1], nfp + 1))

      iy <- (nr - nllp + 1):nr

      text(x2 - cu, yp, dimnames(data)[[1]][iy])

      par(adj=adj)
      text(xp, y1 - lspace, dimnames(data)[[2]][1:nc])

      if (!is.logical(thresh))
        {
          if (length(thresh) == 1)
            {
              filter <- data[iy, 1:nc] >= thresh
              if (any(filter))
                {
                  if (thtype == "size")
                      text(as.vector(xpm)[filter],
                           as.vector(ypm)[filter],
                           as.vector(fdata[iy, 1:nc])[filter])
                  else
                      text(as.vector(xpm)[filter],
                           as.vector(ypm)[filter],
                           as.vector(fdata[iy, 1:nc])[filter],
                           font=boldfont)
                }

              filter <- !filter
              if (any(filter))
                {
                  if (thtype == "size")
                      text(as.vector(xpm)[filter],
                           as.vector(ypm)[filter],
                           as.vector(fdata[iy, 1:nc])[filter],
                           cex=.7 * par("cex"))
                  else
                      text(as.vector(xpm)[filter],
                           as.vector(ypm)[filter],
                           as.vector(fdata[iy, 1:nc])[filter])
                }
            }
          else
            {
              for (cl in 1:nc)
                {
                  filter <- data[iy, cl] >= thresh[cl]
                  if (any(filter))
                    {
                      if (thtype == "size")
                          text(xp[cl],
                               yp[filter],
                               as.vector(fdata[iy, cl])[filter])
                      else
                          text(xp[cl],
                               yp[filter],
                               as.vector(fdata[iy, cl])[filter],
                               font=boldfont)
                    }

                  filter <- !filter
                  if (any(filter))
                    {
                      if (thtype == "size")
                          text(xp[cl],
                               yp[filter],
                               as.vector(fdata[iy, cl])[filter],
                               cex=.7 * par("cex"))
                      else
                          text(xp[cl],
                               yp[filter],
                               as.vector(fdata[iy, cl])[filter])
                    }
                }
            }
        }

      else text(as.vector(xpm), as.vector(ypm), as.vector(fdata[iy, 1:nc]))

      if (!is.null(func))
        {
          savef <- par()
          funcattr$tablemin <- c(x1, y3lp)
          funcattr$nbrow <- nllp
          funcattr$pagenumber <- nfp + 1
          funcattr$firstrow <- nfp * nlfp + 1
          func(funcattr=funcattr, ...)
          par(savef)
        }
    }

  invisible()
}

#########################################################################
#  printtab.myfunc.demo                    Centre de Recherche Public   #
#  V3.0  6th Oct 92                         - Centre Universitaire -    #
#                                         162a, Avenue de la Faiencerie #
#  This S function is an example                L-1511 Luxembourg       #
#  of what can be passed to                   Tel: (+352) 47 02 61      #
#  the printtab's func argument               Fax: (+352) 47 02 64      #
#                                                                       #
#                                             IABD Project - CREDI      #
#                                             --------------------      #
#                                                                       #
#                                           N. Beaumont - R. Bisdorff   #
#                                             F. Fehlen - B. Perbal     #
#########################################################################

harrow <- function(x1, x2, y)
{
  lines(c(x1, x2), c(y, y))
  polygon(c(x1, x1 + 8, x1 + 8), c(y, y - 2, y + 2))
  polygon(c(x2, x2 - 8, x2 - 8), c(y, y - 2, y + 2))
}

varrow <- function(x, y1, y2)
{
  lines(c(x, x), c(y1, y2))
  polygon(c(x, x - 2, x + 2), c(y1, y1 + 8, y1 + 8))
  polygon(c(x, x - 2, x + 2), c(y2, y2 - 8, y2 - 8))
}

printtab.myfunc.demo <- function(funcattr)
{
  lines(c(0, 0, funcattr$pagesize[1], funcattr$pagesize[1], 0),
        c(0, funcattr$pagesize[2], funcattr$pagesize[2], 0, 0))

  varrow(funcattr$pagesize[1] - 15, 1, funcattr$pagesize[2] - 1)
  par(adj=1)
  text(funcattr$pagesize[1] - 20, funcattr$pagesize[2] / 2, "pagesize[2]")
  text(funcattr$pagesize[1] - 20, funcattr$pagesize[2] / 2 - funcattr$lspace,
       funcattr$pagesize[2])

  harrow(1, funcattr$pagesize[1] - 1, funcattr$pagesize[2] - 15)
  par(adj=0.5)
  text(funcattr$pagesize[1] / 2, funcattr$pagesize[2] - 15 - funcattr$lspace,
       "pagesize[1]")
  text(funcattr$pagesize[1] / 2,
       funcattr$pagesize[2] - 15 - 2 * funcattr$lspace,
       funcattr$pagesize[1])

  varrow(funcattr$tablemin[1] + 15, 1, funcattr$tablemin[2] - 1)
  par(adj=0)
  text(funcattr$tablemin[1] + 20, funcattr$tablemin[2] / 2, "tablemin[2]")
  text(funcattr$tablemin[1] + 20, funcattr$tablemin[2] / 2 - funcattr$lspace,
       funcattr$tablemin[2])

  harrow(1, funcattr$tablemin[1] - 1, funcattr$tablemin[2] + 15)
  par(adj=0.5)
  text(funcattr$tablemin[1] / 2,
       funcattr$tablemin[2] + 15 + 2 * funcattr$lspace,
       "tablemin[1]")
  text(funcattr$tablemin[1] / 2, funcattr$tablemin[2] + 15 + funcattr$lspace,
       funcattr$tablemin[1])

  varrow(funcattr$tablemax[1] + 15, 1, funcattr$tablemax[2])
  par(adj=0)
  text(funcattr$tablemax[1] + 20, funcattr$tablemax[2] / 2, "tablemax[2]")
  text(funcattr$tablemax[1] + 20, funcattr$tablemax[2] / 2 - funcattr$lspace,
       funcattr$tablemax[2])

  harrow(1, funcattr$tablemax[1],
              funcattr$tablemax[2] + 30 + 2 * funcattr$lspace)
  par(adj=0.5)
  text(funcattr$tablemax[1] / 2,
       funcattr$tablemax[2] + 30 + 4 * funcattr$lspace,
       "tablemax[1]")
  text(funcattr$tablemax[1] / 2,
       funcattr$tablemax[2] + 30 + 3 * funcattr$lspace,
       funcattr$tablemax[1])

  harrow(funcattr$tablemin[1], funcattr$tablemin[1] + funcattr$dimwidth - 1,
           funcattr$tablemax[2] + 15)
  par(adj=0.5)
  text(funcattr$tablemin[1] + funcattr$dimwidth / 2,
       funcattr$tablemax[2] + 15 + 2 * funcattr$lspace,
       "dimwidth")
  text(funcattr$tablemin[1] + funcattr$dimwidth / 2,
       funcattr$tablemax[2] + 15 + funcattr$lspace,
       funcattr$dimwidth)

  harrow(funcattr$tablemin[1] + funcattr$dimwidth,
           funcattr$tablemin[1] + funcattr$dimwidth + funcattr$width - 1,
           funcattr$tablemax[2] + 15)
  par(adj=0.5)
  text(funcattr$tablemin[1] + funcattr$dimwidth + funcattr$width / 2,
       funcattr$tablemax[2] + 15 + 2 * funcattr$lspace,
       "width")
  text(funcattr$tablemin[1] + funcattr$dimwidth + funcattr$width / 2,
       funcattr$tablemax[2] + 15 + funcattr$lspace,
       funcattr$width)

  par(adj=0)

  if (is.logical(funcattr$thresh)) t <- as.character(funcattr$thresh)
  else t <- paste(format(funcattr$thresh), collapse=" ")

  t <- c("func attributes list:",
         "",
         paste("thresh:",     t),
         paste("pagesize:",   format(funcattr$pagesize[1]),
                              format(funcattr$pagesize[2])),
         paste("tablemin:",   format(funcattr$tablemin[1]),
                              format(funcattr$tablemin[2])),
         paste("tablemax:",   format(funcattr$tablemax[1]),
                              format(funcattr$tablemax[2])),
         paste("dimwidth:",   format(funcattr$dimwidth)),
         paste("width:",      format(funcattr$width)),
         paste("lspace:",     format(funcattr$lspace)),
         paste("frm:",        as.character(funcattr$frm)),
         paste("charunit:",   format(funcattr$charunit)),
         paste("pagenumber:", format(funcattr$pagenumber)),
         paste("nbcol:",      format(funcattr$nbcol)),
         paste("nbrow:",      format(funcattr$nbrow)),
         paste("firstrow:",   format(funcattr$firstrow)))
         
  y <- funcattr$tablemax[2] - ((1:length(t)) - 1) * funcattr$lspace

  text(15, y, t)

  invisible()
}

#########################################################################
#  sumcora  V3.1  20th Nov 92              Centre de Recherche Public   #
#                                           - Centre Universitaire -    #
#  This S function uses the               162a, Avenue de la Faiencerie #
#  'printtab' function to print                 L-1511 Luxembourg       #
#  the matrixes got from a                    Tel: (+352) 47 02 61      #
#  correspondence analysis                    Fax: (+352) 47 02 64      #
#                                                                       #
#                                             IABD Project - CREDI      #
#                                             --------------------      #
#                                                                       #
#                                           N. Beaumont - R. Bisdorff   #
#                                             F. Fehlen - B. Perbal     #
#########################################################################

sumcora.exit <- function(ps, ps.opt)
{
  if (ps)
    {
      dev.off()
      ps.options(ps.opt)
    }
}

sumcora <- function(cora,
                    file     = "",
                    pos      = c(57, 83, 43, 70) / unit.factor,
                    horiz    = F,
                    cex      = par('cex'),
                    lspace   = cu / unit.factor,
                    level    = c(1.5, 1.5),
                    bycol    = T,
                    colnb    = 0,
                    txt      = character(0),
                    ps       = F,
                    warn     = T,
                    region   = c(16, 16, 578, 824) / unit.factor,
                    rnd      = 3,
                    ...,
                    thresh,
                    percent)
{
  message <- setup.language(c("eng", "fr", "ger"), c(
      "'thresh': unauthorized argument",
      "'percent': unauthorized argument",
      "Correspondence analysis",
      "Coordinates in the subspace:  columns",
      "Coordinates in the subspace:  rows",
      "Relative contributions - columns",
      "Relative contributions - rows",
      "(quality of the representation of the points)",
      "Absolute contributions - columns",
      "Absolute contributions - rows",
      "(contributions of the points to an axis)",
      "",
      "",
      "",

      "'thresh': argument non autorise",
      "'percent': argument non autorise",
      "Analyse des correspondances",
      "Coordonnees dans le sous-espace : colonnes",
      "Coordonnees dans le sous-espace : lignes",
      "Contributions relatives - colonnes",
      "Contributions relatives - lignes",
      "explication des points par l'axe",
      "Contributions absolues - colonnes",
      "Contributions absolues - lignes",
      "contributions des points a la variance de l'axe",
      "Valeur propre de l'axe",
      "contribution de l'axe a la variance totale du nuage",
      "( + coord. positives, - coord. negatives)",

      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      ""), warn)

  if (!missing(thresh))  stop(message[1])
  if (!missing(percent)) stop(message[2])

  cex <- cex

  unit.factor <- unit.convert("pt", warn)
  region <- region * unit.factor
  ps.opt <- NULL

  if (ps)
    {
      ps.opt <- ps.options()
      ps.options(horizontal=horiz, region=region, setfont=ps.setfont.latin1)
      postscript(file=file)	# Sends graphics to PostScript if asked
    }

  on.exit(sumcora.exit(ps, ps.opt))

  cu <- cex * 14
  pos[2] <- pos[2] + (2 + length(txt)) * lspace

  if (colnb == 0) colrange <- 1:ncol(cora$data[,,1])
  else colrange <- 1:colnb

 printtab(round(cora$inert,rnd),
           file     = file,
           pos      = pos,
           horiz    = horiz,
           cex      = cex,
           lspace   = lspace,
           ps       = F,
           region   = region,
           warn     = F,
           ...,
           func     = cora.coord.func,
           txt      = c(txt, message[12], message[13]))
printtab(round(cora$data[1:cora$tabdim[2],colrange,1],rnd),
           file     = file,
           pos      = pos,
           horiz    = horiz,
           cex      = cex,
           lspace   = lspace,
           ps       = F,
           region   = region,
           warn     = F,
           ...,
           func     = cora.coord.func,
           txt      = c(txt, message[3], message[4]))

  printtab(round(cora$data[(cora$tabdim[2] + 1):
                    (cora$tabdim[2] + cora$tabdim[1]),colrange,1],rnd),
           file     = file,
           pos      = pos,
           horiz    = horiz,
           cex      = cex,
           lspace   = lspace,
           ps       = F,
           region   = region,
           warn     = F,
           ...,
           func     = cora.coord.func,
           txt      = c(txt, message[3], message[5]))

  pos[2] <- pos[2] + lspace

  if (bycol)
    {
      thresh <- c()
      for (i in colrange)
        {
          thresh[i] <- mean(cora$data[1:cora$tabdim[2],i,2]) * level[2]
        }
    }
  else thresh <- mean(cora$data[1:cora$tabdim[2],colrange,2]) * level[2]        

  printtab(round(cora$data[1:cora$tabdim[2],colrange,2],rnd),
           file     = file,
           thresh   = thresh,
           percent  = F,
           pos      = pos,
           horiz    = horiz,
           cex      = cex,
           lspace   = lspace,
           ps       = F,
           region   = region,
           warn     = F,
           ...,
           func     = cora.contr.func,
           txt      = c(txt, message[3], message[6], message[8],message[14]),
           sgn      = sign(cora$data[1:cora$tabdim[2],colrange,1]))

  if (bycol)
    {
      thresh <- c()
      for (i in colrange)
        {
          thresh[i] <- mean(cora$data[(cora$tabdim[2] + 1):
                       (cora$tabdim[2] + cora$tabdim[1]),i,2]) * level[1]
        }
    }
  else thresh <- mean(cora$data[(cora$tabdim[2] + 1):
                      (cora$tabdim[2] + cora$tabdim[1]),colrange,2]) * level[1]

  printtab(round(cora$data[(cora$tabdim[2] + 1):
                    (cora$tabdim[2] + cora$tabdim[1]),colrange,2],rnd),
           file     = file,
           thresh   = thresh,
           percent  = F,
           pos      = pos,
           horiz    = horiz,
           cex      = cex,
           lspace   = lspace,
           ps       = F,
           region   = region,
           warn     = F,
           ...,
           func     = cora.contr.func,
           txt      = c(txt, message[3], message[7], message[8],message[14]),
           sgn      = sign(cora$data[(cora$tabdim[2] + 1):
                           (cora$tabdim[2] + cora$tabdim[1]),colrange,1]))

  if (bycol)
    {
      thresh <- c()
      for (i in colrange)
        {
          thresh[i] <- mean(cora$data[1:cora$tabdim[2],i,3]) * level[2]
        }
    }
  else thresh <- mean(cora$data[1:cora$tabdim[2],colrange,3]) * level[2]        

  printtab(round(cora$data[1:cora$tabdim[2],colrange,3],rnd),
           file     = file,
           thresh   = thresh,
           percent  = F,
           pos      = pos,
           horiz    = horiz,
           cex      = cex,
           lspace   = lspace,
           ps       = F,
           region   = region,
           warn     = F,
           ...,
           func     = cora.contr.func,
           txt      = c(txt, message[3], message[9], message[11],message[14]),
           sgn      = sign(cora$data[1:cora$tabdim[2],colrange,1]))

  if (bycol)
    {
      thresh <- c()
      for (i in colrange)
        {
          thresh[i] <- mean(cora$data[(cora$tabdim[2] + 1):
                       (cora$tabdim[2] + cora$tabdim[1]),i,3]) * level[1]
        }
    }
  else thresh <- mean(cora$data[(cora$tabdim[2] + 1):
                      (cora$tabdim[2] + cora$tabdim[1]),colrange,3]) * level[1]

  printtab(round(cora$data[(cora$tabdim[2] + 1):
                    (cora$tabdim[2] + cora$tabdim[1]),colrange,3],rnd),
           file     = file,
           thresh   = thresh,
           percent  = F,
           pos      = pos,
           horiz    = horiz,
           cex      = cex,
           lspace   = lspace,
           ps       = F,
           region   = region,
           warn     = F,
           ...,
           func     = cora.contr.func,
           txt      = c(txt, message[3], message[10], message[11],message[14]),
           sgn      = sign(cora$data[(cora$tabdim[2] + 1):
                           (cora$tabdim[2] + cora$tabdim[1]),colrange,1]))

  invisible()
}

cora.coord.func <- function(funcattr, txt)
{
  if (length(txt) > 0)
    {
      ytop <- funcattr$tablemax[2] + (length(txt) + 1) * funcattr$lspace

      if (funcattr$frm)
        {
          lines(c(funcattr$tablemin[1], funcattr$tablemin[1],
                  funcattr$tablemax[1], funcattr$tablemax[1]),
                c(funcattr$tablemax[2], ytop,
                  ytop, funcattr$tablemax[2]))
        }

      par(adj=0)

      ytop <- ytop - funcattr$lspace * (1:length(txt))
      text(funcattr$tablemin[1] + funcattr$charunit, ytop, txt)
    }

  invisible()
} 

cora.contr.func <- function(funcattr, txt, sgn)
{
  cora.coord.func(funcattr, txt)

  par(adj=0.5)

  xp <- funcattr$tablemin[1] + funcattr$dimwidth - funcattr$charunit / 2.0 +
        (1:funcattr$nbcol) * funcattr$width
  xpm <- matrix(rep(xp, funcattr$nbrow), ncol=funcattr$nbcol, byrow=T)
  yp <- funcattr$tablemax[2] - ((1:funcattr$nbrow) + 2) * funcattr$lspace
  ypm <- matrix(rep(yp, funcattr$nbcol), ncol=funcattr$nbcol)

  if (is.logical(funcattr$thresh)) tfilter <- T
  else if (length(funcattr$thresh) == 1)
      tfilter <- funcattr$data[funcattr$firstrow + (1:funcattr$nbrow) - 1,
                               1:funcattr$nbcol] >= funcattr$thresh
  else
    {
      tfilter <- matrix(logical(funcattr$nbrow * funcattr$nbcol),
                        ncol=funcattr$nbcol)
      for (i in 1:length(funcattr$thresh))
        {
          tfilter[,i] <- funcattr$data[funcattr$firstrow +
                         (1:funcattr$nbrow) - 1, i] >= funcattr$thresh[i]
        }
    }

  sfilter <- sgn[funcattr$firstrow + (1:funcattr$nbrow) - 1,
                1:funcattr$nbcol] == 1
  filter <- tfilter & sfilter

  if (any(filter)) text(array(xpm)[filter], array(ypm)[filter], "+")

  sfilter <- !sfilter
  filter <- tfilter & sfilter

  if (any(filter)) text(array(xpm)[filter], array(ypm)[filter], "-")

  invisible()
}
#########################################################################
#  qcora  V3.1  20th Nov 92                Centre de Recherche Public   #
#                                           - Centre Universitaire -    #
#  This S function performs               162a, Avenue de la Faiencerie #
#  quick identification                         L-1511 Luxembourg       #
#  of the axes                                Tel: (+352) 47 02 61      #
#                                             Fax: (+352) 47 02 64      #
#                                                                       #
#                                             IABD Project - CREDI      #
#                                             --------------------      #
#                                                                       #
#                                           N. Beaumont - R. Bisdorff   #
#                                             F. Fehlen - B. Perbal     #
#########################################################################

qcora <- function(x,
                  axis1    = 1,
                  axis2    = 2,
                  txt      = paste(message[1], axis1),
                  rlevel   = 1.5,
                  clevel   = 1.5,
                  warn     = T,
                  magnify   = 1)
{
  message <- setup.language(c("eng", "fr", "ger"), c(
      "Identification of axis",
      "Identification de l'axe",
      ""), warn)

  plcora(x,
         axis1,
         axis2,
         mthd="ctrn",
         cmin=mean(x$data[1:x$tabdim[2], axis1, 3]) * clevel,
         rmin=mean(x$data[(x$tabdim[2] + 1):(x$tabdim[1] + x$tabdim[2]),
                   axis1, 3]) * rlevel,
         warn = F,
         main = txt,
         magnify = magnify)
  invisible()
}

