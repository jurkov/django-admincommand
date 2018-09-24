.PHONY: setup destroy_and_build push_test push

setup:
	pip install --upgrade twine

destroy_and_build:
	rm -rf dist/
	python setup.py bdist_wheel

push_test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

push:
	twine upload dist/*
