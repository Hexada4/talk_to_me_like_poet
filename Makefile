
VENV=.venv
PYTHON=$(VENV)/bin/python3
WORK_DIR=$(shell pwd)
DATASET=$(shell pwd)/path/to/dataset.csv
EMBEDDINGS=$(shell pwd)/path/to/embeddings.txt

# ================== LOCAL WORKSPACE SETUP ==================
base-requirements:
	$(PYTHON) -m pip install -r $(WORK_DIR)/requirements.txt
	@sudo apt-get update && sudo apt-get install -y llvm clang
	$(PYTHON) install -U pip numpy wheel packaging requests opt_einsum
	$(PYTHON) install -U keras_preprocessing --no-deps
	$(PYTHON) install tensorflow_text
	$(PYTHON) install better_profanity

parse_links:
	@echo 'parsing links'
	$(PYTHON) data/parser.py

train: 
	@echo 'training a model'
	@cd lyrics-generator_copy && python3 -m lyrics.train --songdata-file $(DATASET) --artists '*' --embedding-file $(EMBEDDINGS) --early-stopping-patience 80
	@echo 'model trained. find it in dir'
