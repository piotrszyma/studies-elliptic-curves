CC = g++
OPTIONS = -Wall -std=c++17 -O3
INCLUDES = -I .
LIBS = -lgmp -lgmpxx
BIN = pollard_rho.bin
.PHONY: all clean
OBJS = main.o pollard_rho.o

all: ${OBJS}
	${CC} ${OPTIONS} -lgmp -lgmpxx ${OBJS} -o ${BIN}

main.o: main.cpp
	${CC} ${OPTIONS} ${INCLUDES} -c main.cpp

%.o: %.cpp %.h
	${CC} ${OPTIONS} ${INCLUDES} -c $*.cpp

run:
	./${BIN}

clean:
	rm -rf *.o out
