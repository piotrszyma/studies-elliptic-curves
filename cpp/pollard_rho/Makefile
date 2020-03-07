CC = g++
OPTIONS = -Wall -std=c++17
INCLUDES = -I . -I/usr/local/opt/openssl/include
LIBS = -lgmp -lgmpxx
BIN = pollard_rho
.PHONY: all clean
OBJS = main.o pollard_rho.o number.o

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
