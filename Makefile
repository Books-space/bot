lint:
	@flake8 bot
	@mypy bot

install:
	poetry install

run:
	python -m bot