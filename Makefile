shell:
	pipenv shell

lint:
	pipenv run pre-commit run --all-files

build-css:
	npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

build-css-dev:
	npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

install:
	npm i
	make build-css
	pipenv install

install-dev:
	npm i
	make build-css
	pipenv install --dev

uninstall:
	pipenv --rm

update:
	pipenv update --dev
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

run:
	pipenv run python3.12 main.py

clean:
	pipenv clean
