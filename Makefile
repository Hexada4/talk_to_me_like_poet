.PHONY: *

VENV=.venv
PYTHON=$(VENV)/bin/python3
WORK_DIR=$(shell pwd)

# ================== LOCAL WORKSPACE SETUP ==================
venv:
	$(PYTHON) -m venv $(VENV)
	@echo 'Path to Python executable $(shell pwd)/$(PYTHON)'

base-requirements: 
	$(PYTHON) -m pip install -r $(WORK_DIR)/requirements.txt
	@sudo apt-get update && sudo apt-get install -y llvm-16 clang-16
	$(PYTHON) install -U pip numpy wheel packaging requests opt_einsum
	$(PYTHON) install -U keras_preprocessing --no-deps
	$(PYTHON) install tensorflow_text
	$(PYTHON) install better_profanity

parse_links:
	@echo 'parsing links'
	$(PYTHON) data/parser.py

train: 
	@echo 'training a model'
	@cd lyrics-generator_copy && python3 -m lyrics.train --songdata-file ../data/all_poems.csv --artists '*'
	@echo 'model trained. find it in dir'
