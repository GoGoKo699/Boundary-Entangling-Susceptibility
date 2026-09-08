.PHONY: install test verify figures records evidence
install:
	python -m pip install -r requirements-reproducible.txt
	python -m pip install -e .
test:
	pytest -q
verify:
	python verify.py
figures:
	python reproduce.py --core-figures
records:
	python scripts/analysis/reproduce_core_records.py
evidence:
	python scripts/analysis/reassess_evidence.py --bootstrap 5000 --seed 2026090501
