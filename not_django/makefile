.PHONY: all run

ifeq ($(OS),Windows_NT)
PYTHON = C:\Python27\python.exe
else
PYTHON = python
endif

MAKE = @make PYTHON=$(PYTHON)

all: run

flake8:
	$(MAKE) -C source flake8
	$(MAKE) -C tests flake8

# make tests >log_file 2>&1
tests: flake8
	$(MAKE) -C tests

run:
	$(MAKE) -C source run

setup:
	$(PYTHON) -m pip install -r tests/requirements.txt
