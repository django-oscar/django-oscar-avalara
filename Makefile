install:
	pip install -r requirements.txt
	python setup.py develop

sandbox: install
	python sandbox/manage.py reset_db --router=default --noinput
	python sandbox/manage.py syncdb --noinput
	python sandbox/manage.py migrate
	python sandbox/manage.py loaddata sandbox/fixtures/*.json
	python sandbox/manage.py oscar_import_catalogue sandbox/fixtures/books-catalogue.csv

release:
	python setup.py sdist upload
	git push --tags
