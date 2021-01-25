.PHONY: all run

all: run

flake8:
	@$(PYTHON) -m flake8 --max-line-length=110 .

run:
	@$(PYTHON) wsgi.py
