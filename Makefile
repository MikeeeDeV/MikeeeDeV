.PHONY: all build test preview clean check nix-build nix-shell help

PYTHON ?= python3

all: build test

help:
	@echo "MikeeeDeV Profile & VectorForge Engine - Commands"
	@echo "  make build       Run all SVG and Markdown generators"
	@echo "  make test        Run full test suite (snapshots, library, XML)"
	@echo "  make library     Compile catalog and batch render all 235 SVGs"
	@echo "  make gallery     Preview VectorForge interactive showroom"
	@echo "  make preview     Serve profile locally on port 8080"
	@echo "  make nix-build   Build hermetic derivation via Nix Flake"
	@echo "  make clean       Remove temporary caches"

build:
	$(PYTHON) scripts/run_all.py
	$(PYTHON) -m library.catalog

library:
	$(PYTHON) -m library.catalog

test:
	$(PYTHON) -m unittest discover tests -v

gallery:
	@echo "Serving VectorForge Showroom on http://localhost:8080/library/gallery/index.html ..."
	$(PYTHON) -m http.server 8080

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
