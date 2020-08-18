# ExposeText

**Expose the text in a document for modification.**

---

[![PyPI version](https://badge.fury.io/py/expose-text.svg)](https://badge.fury.io/py/expose-text)
![Tests](https://github.com/openredact/expose-text/workflows/Tests/badge.svg?branch=master)
![Black & Flake8](https://github.com/openredact/expose-text/workflows/Black%20&%20Flake8/badge.svg?branch=master)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

_**:warning: Disclaimer :warning::**_ This is a prototype. Do not use for anything critical.

## What is ExposeText?

Dealing with document file formats can be quite painful.
Oftentimes code must be written that’s specific to one file format.
We have written ExposeText with the goal to make modifying documents as simple as changing Python strings.
A slice of the original document can be directly assigned a new content by using the character indices of the extracted text, all while keeping the document's original formatting.

We published a blog post about ExposeText on [Medium](https://medium.com/@openredact/introducing-exposetext-modify-document-files-as-simply-as-strings-cc5caa5f9c66?source=friends_link&sk=825c8f64dfa4e943b66d1faf351340a2).

![](https://raw.githubusercontent.com/openredact/expose-text/master/docs/expose-text.png "Exposing the plain text content, then modifying it")

## Supported Formats

ExposeText has prototypical support for the following file formats:

- .txt
  - Per default, the encoding is assumed to be UTF-8.
  - You can install [chardet](https://github.com/chardet/chardet) (`pip install chardet`), to automatically detect the encoding.
- .html
  - You can pass either an HTML snippet, an HTML body or a complete HTML document. If you pass a complete HTML document, every text content outside the body is ignored.
  - The output file will always be encoded in UTF-8.
- .docx
  - Only text within `<w:t>` tags (the tags for anything that is text) is exposed. E.g. the mailto link of an e-mail address is not exposed.
- .pdf
  - Per default, text in PDFs can only be replaced with characters that occur in the file (fonts are stored economically in PDF files).
  - If you install the additional dependencies [Poppler (pdftohtml)](https://poppler.freedesktop.org/) and [wkhtmltopdf](https://wkhtmltopdf.org/), the PDF is rerendered and there is no more restriction on the characters that can be used.


## Usage

ExposeText supports files as well as binary data objects.
Depending on your use case you can use one of the following interfaces for making modifications.

### Installation

`expose-text` can be installed from PyPi and has to be installed in a virtual environment (venv or conda for instance)

```bash
pip install expose-text
```

### Slicing API

The slicing API applies each alteration immediately.

Exposing and modifying text inside a file:
```python
>>> from expose_text import FileWrapper
>>>
>>> wrapper = FileWrapper("myfile.docx")
>>> wrapper.text
'This is the content as string.'

>>> wrapper[12:19] = "new content"
>>> wrapper.text
'This is the new content as string.'

>>> wrapper[33] = "!"  # note that you have to use the updated index here
>>> wrapper.text
'This is the new content as string!'

>>> wrapper.save("newfile.docx")
```

If you want to work directly with binary data you have to pass the file format:
```python
>>> from expose_text import BinaryWrapper
>>>
>>> wrapper = BinaryWrapper(my_bytes, ".docx")
>>> wrapper.text
'This is the content as string.'

>>> wrapper[12:19] = "new content"
>>> wrapper.text
'This is the new content as string.'

>>> wrapper.bytes  # get the modified file as bytes
b'...'
```

### Functional API

With the functional API, you can queue several alterations based on the initial indices and then apply them together.
```python
>>> wrapper.text
'This is the content as string.'

>>> wrapper.add_alter(12, 19, "new content")
>>> wrapper.add_alter(29, 30, "!")
>>> wrapper.apply_alters()
>>> wrapper.text
'This is the new content as string!'
```

## Development

### Install requirements

You can install all (production and development) requirements using:

```
pip install -r requirements.txt
```

### Install the pre-commit hooks

This repository uses git hooks to validate code quality and formatting.

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

### Testing in Docker

You can run the test as well in a Docker container:

```bash
docker build -t expose-text
docker run expose-text
```

## How to contact us

For usage questions, bugs, or suggestions please file a Github issue.
If you would like to contribute or have other questions please email hello@openredact.org.

## License

[MIT License](https://github.com/openredact/expose-text/blob/master/LICENSE)
