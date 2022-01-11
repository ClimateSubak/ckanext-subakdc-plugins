[![Tests](https://github.com/ClimateSubak/ckanext-subakdc-plugins/workflows/Tests/badge.svg?branch=main)](https://github.com/ClimateSubak/ckanext-subakdc-plugins/actions)

# ckanext-subakdc-plugins
Custom plugins for the Subak Data Catalogue

## Requirements
None

## Installation
To install ckanext-subakdc-plugins:

1. Add the following lines to `ckan/Dockerfile` in the `docker-ckan` project:

    ```
    RUN pip install -e git+https://github.com/climatesubak/ckanext-subakdc-plugins.git#egg=ckanext-subakdc-plugins && \
        pip install -r https://raw.githubusercontent.com/climatesubak/ckanext-subakdc-plugins/main/requirements.txt
    ```

3. Add `subakdc-plugins` to `CKAN__PLUGINS` in your .env file

4. Rebuild and start the `ckan` container. E.g. using `make rebuild.ckan`


## Config settings
None at present

## Developer installation
To install ckanext-subakdc-plugins for development:

1. Clone this repo into the `/src` folder of the `docker-ckan` project

2. Add `subakdc-plugins` to `CKAN__PLUGINS` in your .env file

3. Rebuild and start the `ckan` container. E.g. using `make rebuild.ckan`

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-subakdc-plugins

If ckanext-subakdc-plugins should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
