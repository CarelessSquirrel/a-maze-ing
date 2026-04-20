PYTHON = python3
MAIN   = a_maze_ing.py
CONFIG = config.txt

BLUE   = \033[34m
GREEN  = \033[32m
YELLOW = \033[33m
RESET  = \033[0m

install:
	@echo "$(YELLOW)installing dependencies...$(RESET)"
	python3 -m pip install build setuptools
	python3 -m pip install -e .
	@echo "$(GREEN)dependencies installed!$(RESET)"

run:
	@echo "$(BLUE)starting A-Maze-ing...$(RESET)"
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	@echo "$(YELLOW)starting in debug mode...$(RESET)"
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@echo "$(YELLOW)cleaning up caches...$(RESET)"
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name build -exec rm -rf {} +
	@echo "$(GREEN)all clean!$(RESET)"

lint:
	@echo "$(BLUE)checking flake8...$(RESET)"
	flake8 .
	@echo "$(BLUE)checking mypy...$(RESET)"
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "$(GREEN)all checks passed!$(RESET)"

lint-strict:
	@echo "$(BLUE)checking flake8 (strict)...$(RESET)"
	flake8 .
	@echo "$(BLUE)checking mypy (strict)...$(RESET)"
	mypy . --strict
	@echo "$(GREEN)all strict checks passed!$(RESET)"

.PHONY: install run debug clean lint lint-strict
