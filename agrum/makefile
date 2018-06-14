#
# make file for compiling the C++/agrum sources
#
CC = g++-7
CCFLAGS = -Wall -DNDEBUG -std=c++11
INCLUDE = /usr/include
INSTALL = /usr/bin
LDagrum = agrum
all:	
	make enum
	make enumPiping
	make detect

enum : digraphsEnumChordlessCircuits.o
	${CC} -o enumChordlessCircuits digraphsEnumChordlessCircuits.o -l${LDagrum}
digraphsEnumChordlessCircuits.o : digraphsEnumChordlessCircuits.cpp
	${CC} ${CCFLAGS} -c digraphsEnumChordlessCircuits.cpp -I${INCLUDE}

enumPiping : digraphsEnumChordlessCircuitsInOutPiping.o
	${CC} -o enumChordlessCircuitsInOutPiping digraphsEnumChordlessCircuitsInOutPiping.o -l${LDagrum} 
digraphsEnumChordlessCircuitsInOutPiping.o : digraphsEnumChordlessCircuitsInOutPiping.cpp
	${CC} ${CCFLAGS} -c digraphsEnumChordlessCircuitsInOutPiping.cpp -I${INCLUDE}

detect : digraphsDetectChordlessCircuits.o
	${CC} -o detectChordlessCircuits digraphsDetectChordlessCircuits.o -l${LDagrum}

digraphsDetectChordlessCircuits.o : digraphsDetectChordlessCircuits.cpp
	${CC} ${CCFLAGS} -c digraphsDetectChordlessCircuits.cpp -I${INCLUDE}

install : enumChordlessCircuits enumChordlessCircuitsInOutPiping detectChordlessCircuits
	cp enumChordlessCircuits ${INSTALL}
	cp enumChordlessCircuitsInOutPiping ${INSTALL}
	cp detectChordlessCircuits ${INSTALL}
