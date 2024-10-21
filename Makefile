start:
	poetry run flask --app example --debug run --port 8000

build:
	./build.sh

test:
	poetry run flask --app test --debug run --port 8000

run:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 hexlet_flask_example:app
