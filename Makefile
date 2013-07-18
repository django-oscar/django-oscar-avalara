install:
	python setup.py develop
	pip install -r requirements.txt

sandbox: install
	python sandbox/manage.py syncdb --noinput
	python sandbox/manage.py migrate
	python sandbox/manage.py loaddata sandbox/fixtures/auth.json sandbox/fixtures/countries.json
	python sandbox/manage.py oscar_import_catalogue sandbox/fixtures/books-catalogue.csv
