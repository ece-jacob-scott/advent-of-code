SRC_DIR := src
SRC := $(wildcard $(SRC_DIR)/*.rs)

.PHONY: build
build: main

main: $(SRC)
	rustc $(SRC)

