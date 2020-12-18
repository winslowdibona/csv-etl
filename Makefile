pytest:
	python setup.py pytest

test-cov:
	pytest --cov-report html:cov_html --cov=csv_etl tests/

docs:
	pdoc --html csv_etl --force

build-dist:
	python setup.py sdist bdist_wheel

test-upload:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	twine upload dist/*

clean:
	rm -rf html
	rm -rf cov_html
	rm -rf build
	rm -rf .pytest_cache
	rm -rf .eggs
	rm -rf csv_etl/__pycache__
	rm -rf csv_etl.egg-info
	rm -rf tests/__pycache__
	rm .coverage
