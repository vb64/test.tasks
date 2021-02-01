.PHONY: all setup setup2 flake8 lint

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
else
PYTHON = ./venv/bin/python
endif

SOURCE = source
PIP = $(PYTHON) -m pip install

all:
	$(PYTHON) $(SOURCE)/main.py

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 $(SOURCE)

lint:
	$(PYTHON) -m pylint $(SOURCE)

setup: setup_python setup_pip

setup2: setup_python2 setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv

setup_python2:
	$(PYTHON_BIN) -m virtualenv ./venv
