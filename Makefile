.PHONY: setup build deploy format clean

setup:
	python3 -m venv .venv
	.venv/bin/python3 -m pip install -U pip
	.venv/bin/python3 -m pip install -r requirements-dev.txt

build:
	sam build

deploy:
	sam deploy

clean:
	sam delete

format:
	.venv/bin/black -t py312 --line-length 100 .
