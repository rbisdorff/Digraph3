#
# makefile for gcc
#
CC = gcc
CCFLAGS = O4

calmat.x : arithm.o cent_red.o diag.o dist_fac.o getok.o chrgprog.o ifs.o labels.o loadmat.o chi_deux.o compo.o compolg.o compoc.o parser.o while.o matneut.o c_entry.o profil.o
		cc -o calmat  arithm.o c_entry.o cent_red.o chi_deux.o chrgprog.o compo.o compolg.o compoc.o diag.o dist_fac.o getok.o ifs.o labels.o loadmat.o matneut.o parser.o while.o profil.o -lm

arithm.o : arithm.c
		${CC}  -${CCFLAGS} -c arithm.c
c_entry.o : c_entry.c
		${CC}  -${CCFLAGS} -c c_entry.c
chi_deux.o : chi_deux.c
		${CC}  -${CCFLAGS} -c chi_deux.c
chrgprog.o : chrgprog.c
		${CC}  -${CCFLAGS} -c chrgprog.c
compo.o : compo.c
		${CC}  -${CCFLAGS} -c compo.c
compolg.o : compolg.c
		${CC}  -${CCFLAGS} -c compolg.c
compoc.o : compoc.c
		${CC}  -${CCFLAGS} -c compoc.c
diag.o : diag.c
		${CC}  -${CCFLAGS} -c diag.c
dist_fac.o : dist_fac.c
		${CC}  -${CCFLAGS} -c dist_fac.c
getok.o : getok.c
		${CC}  -${CCFLAGS} -c getok.c
ifs.o : ifs.c
		${CC}  -${CCFLAGS} -c ifs.c
labels.o : labels.c
		${CC}  -${CCFLAGS} -c labels.c
loadmat.o : loadmat.c
		${CC}  -${CCFLAGS} -c loadmat.c
matneut.o : matneut.c
		${CC}  -${CCFLAGS} -c matneut.c
parser.o : parser.c
		${CC}  -${CCFLAGS} -c parser.c
while.o : while.c
		${CC}  -${CCFLAGS} -c while.c
profil.o : profil.c
		${CC}  -${CCFLAGS} -c profil.c

install :
		sudo cp calmat /usr/local/bin
		sudo cp defdist.sh /usr/local/bin
		sudo cp defdista.sh /usr/local/bin

