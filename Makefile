sandbox: install
	python sandbox/manage.py syncdb --noinput
	python sandbox/manage.py migrate
	python sandbox/manage.py loaddata sandbox/fixtures/auth.json sandbox/fixtures/countries.json
	python sandbox/manage.py oscar_import_catalogue sandbox/fixtures/books-catalogue.csv

install:
	pip install -r requirements.txt
	python setup.py develop
