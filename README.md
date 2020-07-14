# ExposeText

**Expose the text in a document for modification.**

---

![Tests](https://github.com/openredact/expose-text/workflows/Tests/badge.svg?branch=master)
![Black & Flake8](https://github.com/openredact/expose-text/workflows/Black%20&%20Flake8/badge.svg?branch=master)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

_**:warning: Disclaimer :warning::**_ This is a prototype. Do not use for anything critical.

## What is ExposeText

ExposeText extracts the plain text in a document and gives you an API to modify it.
This enables you to modify various file formats as easily as strings while keeping the original formatting.

## Supported Formats

- .txt
  - The encoding is automatically detected using [chardet](https://github.com/chardet/chardet) which should work fine in most cases.
- .html
  - You can either pass an HTML snippet, a body or a complete HTML document. If you pass a complete HTML document, everything but the body is ignored.
  - The output file will always be encoded in UTF-8.
- .docx


## Usage

You can use ExposeText on files and binary data objects.

This is how you can expose the text inside a file:
```python
>>> from expose_text import FileWrapper
>>>
>>> wrapper = FileWrapper('myfile.docx')
>>> wrapper.text
'This is the content as string.'

>>> wrapper[12:19] = 'new content'
>>> wrapper.text
'This is the new content as string.'

>>> fw.save('newfile.docx')
```

If you want to work directly with binary data you have to provide the file format:
```python
>>> from expose_text import BinaryWrapper
>>>
>>> wrapper = BinaryWrapper(my_bytes, '.docx')
>>> wrapper.text
'This is the content as string.'

>>> wrapper[12:19] = 'new content'
>>> wrapper.text
'This is the new content as string.'

>>> bw.bytes  # get the modified file as bytes
b'...'
```

Depending on your usecase use one of the following interfaces for making modifications.

### Functional API

Queue several alterations based on the initial indices and then apply them.
```python
>>> wrapper.text
'This is the content as string.'

>>> wrapper.add_alter(12, 19, 'new content')
>>> wrapper.add_alter(29, 30, '!')
>>> wrapper.apply_alters()
>>> wrapper.text
'This is the new content as string!'
```

### Slicing API

Make and immediately apply a single alteration.
```python
>>> wrapper.text
'This is the content as string.'

>>> wrapper[12:19] = 'new content'
>>> wrapper.text
'This is the new content as string.'

>>> wrapper[33] = '!'  # note that you have to use the updated index here
>>> wrapper.text
'This is the new content as string!'
```

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

## How to contact us

For usage questions, bugs, or suggestions please file a Github issue.
If you would like to contribute or have other questions please email hello@openredact.org

## License

[MIT License](https://github.com/openredact/expose-text/blob/master/LICENSE)
