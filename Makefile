install:
	npm install
	npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css
	python -m pip install -r requirements.txt

build-css:
	npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

build-css-dev:
	npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

run:
	python -m hypercorn main:app

run-dev:
	python main.py

