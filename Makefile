.PHONY: setup build deploy clean format outdated

setup:
	python3 -m venv .venv
	.venv/bin/python3 -m pip install -U pip setuptools wheel
	.venv/bin/python3 -m pip install -r requirements-dev.txt
	.venv/bin/python3 -m pip install -r src/activation_lambda/requirements.txt

build:
	sam build --parallel --cached

deploy:
	sam deploy

clean:
	sam delete

format:
	.venv/bin/python3 -m black .

outdated:
	.venv/bin/python3 -m pip list -o
