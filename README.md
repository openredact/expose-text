# ExposeText

A Python module that exposes text for modification in multiple file types.

![Tests](https://github.com/openredact/expose-text/workflows/Tests/badge.svg?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## Supported Formats

### .txt

### .html

Note: Only HTML in UTF-8 encoding is supported. HTML special entities will be replaced with their UTF-8 equivalent.

## Development

### Install requirements

You can install all requirements using:

```
pip install -r requirements.txt
```

Compared to installation with `setup.py`, [requirements.txt](requirements.txt) additionally installs developer dependencies.

To install it using `setup.py` run:

```
pip install .
```

### Install the pre-commit hooks

```
pre-commit install
git config --bool flake8.strict true  # Makes the commit fail if flake8 reports an error
```

To run the hooks:
```
pre-commit run --all-files
```

### Testing

The tests can be executed with:
```
pytest --doctest-modules --cov-report term --cov=expose_text
```
