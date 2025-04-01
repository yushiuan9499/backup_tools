CC=g++
CFLAGS=-c -O2 -Wall -std=c++17 
LDFLAGS=-lgit2

all: bin/check_n_split

bin/check_n_split: build/check_n_split.o
	$(CC) build/check_n_split.o -o bin/check_n_split $(LDFLAGS)

build/check_n_split.o: src/check_n_split.cpp
	$(CC) $(CFLAGS) src/check_n_split.cpp -o build/check_n_split.o
