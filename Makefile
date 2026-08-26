.PHONY: install verify test figures clean

install:
	python -m pip install -r requirements.txt
	python -m pip install -e .

verify:
	python verify.py

test:
	pytest -q

figures:
	python reproduce.py --core-figures

clean:
	rm -rf reproduced_figures .pytest_cache build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
