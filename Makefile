.PHONY: *

VENV=.venv
PYTHON=$(VENV)/bin/python3
WORK_DIR=$(shell pwd)

# ================== LOCAL WORKSPACE SETUP ==================
venv:
	$(PYTHON) -m venv $(VENV)
	@echo 'Path to Python executable $(shell pwd)/$(PYTHON)'

base-requirements: venv
	$(PYTHON) -m pip install -r $(WORK_DIR)/requirements.txt
	@sudo apt-get update && sudo apt-get install -y llvm-16 clang-16
	$(PYTHON) install -U pip numpy wheel packaging requests opt_einsum
	$(PYTHON) install -U keras_preprocessing --no-deps
	$(PYTHON) install better_profanity

parse_links:
	$(PYTHON) data/parser.py

train: parse_links
	$(PYTHON)
