start:
	poetry run flask --app example --debug run --port 8000

test:
	poetry run flask --app test --debug run --port 8000