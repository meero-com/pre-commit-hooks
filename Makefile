.PHONY: init-pre-commit pre-commit init-test test test-debug clean-test

init-pre-commit: ## Before you can run hooks, you need to have the pre-commit package manager installed
	python3 -m pip install pre-commit
	pre-commit install

pre-commit: ## run pre-commit locally
	pre-commit run -a

init-test:
	python3 -m pip install pip==22.0.4
	pip3 install -r requirements-dev.txt

test: ## Run python test on terraform modules
	pytest -vv

test-debug: ## Run python test on terraform modules
	pytest -s

clean-test: ## Remove local tests artifacts not source controlled
	@find . | grep -E "(__pycache__|\.pytest)" | xargs rm -rf
