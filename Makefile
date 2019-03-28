.PHONY: clean data jupyter lint requirements venv

#################################################################################
# GLOBALS                                                                       #
#################################################################################
PROJECT_NAME = powertac_logfiles
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_DIR =  $(PROJECT_DIR)/env
JUPYTER_DIR =  $(VENV_DIR)/share/jupyter

PYTHON_INTERPRETER = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip
IPYTHON = $(VENV_DIR)/bin/ipython
JUPYTER = $(VENV_DIR)/bin/jupyter

NOTEBOOK_DIR =  $(PROJECT_DIR)/notebooks

#################################################################################
# STANDARD COMMANDS                                                             #
#################################################################################

## Install Python Dependencies
requirements: venv
	$(PIP) install -U pip setuptools wheel
	$(PIP) install -r requirements.txt

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	@$(PYTHON_INTERPRETER) -m flake8 --config=$(PROJECT_DIR)/.flake8 src

# Launch jupyter server and create custom kernel if necessary
jupyter:
ifeq ($(wildcard $(JUPYTER_DIR)/kernels/$(PROJECT_NAME)/*),)
	@echo "Creating custom kernel..."
	@$(IPYTHON) kernel install --sys-prefix --name=$(PROJECT_NAME)
endif
ifeq ($(wildcard $(JUPYTER_DIR)/nbextensions/table_beautifier/*),)
	@echo "Installing jupyter notebook extensions..."
	@$(JUPYTER) contrib nbextension install --sys-prefix
	@$(JUPYTER) nbextensions_configurator enable --sys-prefix
endif
	@echo "Running jupyter notebook in background..."
	@JUPYTER_CONFIG_DIR=$(NOTEBOOK_DIR) $(JUPYTER) notebook --notebook-dir=$(NOTEBOOK_DIR)

## Install virtual environment
venv:
ifeq ($(wildcard $(VENV_DIR)/*),)
	@echo "Did not find $(VENV_DIR), creating..."
	mkdir -p $(VENV_DIR)
	python3.6 -m venv $(VENV_DIR)
endif

#################################################################################
# CUSTOM COMMANDS                                                               #
#################################################################################

## process logfiles
powertac_logfiles:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/cli/run.py

## visualize broker performence
visualize_log_files:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/visualize/make_visualize.py --database No

## visualize broker performence
visualize_database:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/visualize/make_visualize.py --database Yes

## visualize broker performence
visualize_log_files_multiple_games:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/visualize/make_visualize.py --database No --combine_game_ids $(game_id)

## visualize broker performence
visualize_database_multiple_games:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/visualize/make_visualize.py --database Yes --combine_game_ids $(game_id)

## visualize broker performence
visualize_multiple_games: visualize_log_files_multiple_games visualize_database_multiple_games

## visualize broker performence in Power Tac 2018
visualize_powertac_2018_log_files:
	@$(PYTHON_INTERPRETER) src/$(PROJECT_NAME)/visualize/make_visualize.py --database No --combine_game_ids '2018'

## create data directories
data_dir:
	mkdir data
	mkdir data/local
	mkdir data/processed
	mkdir data/web
	mkdir data/web/extracted
	mkdir data/web/extracted/log
	mkdir data/web/raw

## create output directories
output_dir:
	mkdir output

## cleaning data directory
clean_data_dir:
	rm -r data
	make data_dir

## clean output directories
clean_output_dir:
	rm -r output
	make output_dir

## initial project setupt
initialize: requirements data_dir output_dir
