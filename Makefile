.PHONY: all build test preview clean check nix-build nix-shell help

PYTHON ?= python3

all: build test

help:
	@echo "MikeeeDeV Profile Engine - Commands"
	@echo "  make build       Run all SVG and Markdown generators"
	@echo "  make test        Run test suite (snapshot & XML validation)"
	@echo "  make check       Build and run test suite"
	@echo "  make preview     Serve profile locally on port 8080"
	@echo "  make nix-build   Build hermetic derivation via Nix Flake"
	@echo "  make clean       Remove temporary caches"

build:
	$(PYTHON) scripts/run_all.py

test:
	$(PYTHON) -m unittest discover tests -v

check: build test

preview:
	@echo "Opening preview on http://localhost:8080 (Ctrl+C to stop)..."
	$(PYTHON) -m http.server 8080

nix-build:
	nix build .#packages.x86_64-linux.default

nix-shell:
	nix develop

clean:
	rm -rf data/cache/*.json
	rm -rf .pytest_cache
	@echo "Cleaned cache files."
