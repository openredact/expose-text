# ExposeText

_**:warning: Disclaimer :warning::**_ This is a prototype. Do not use for anything critical.

A Python module that exposes text for modification in multiple file types.

![Tests](https://github.com/openredact/expose-text/workflows/Tests/badge.svg?branch=master)
![Black & Flake8](https://github.com/openredact/expose-text/workflows/Black%20&%20Flake8/badge.svg?branch=master)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## Supported Formats

### .txt

- The encoding is automatically detected using [chardet](https://github.com/chardet/chardet) which should work fine in most cases.

### .html

- You can either pass an HTML snippet, a body or a complete HTML document. If you pass a complete HTML document, everything but the body is ignored.
- The output file will always be encoded in UTF-8.

### .docx


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

## License

MIT
