# MkDocs Caption

| | |
| --- | --- |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-caption.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/mkdocs-caption/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-caption.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/mkdocs-caption/) |
| Meta | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)|
| CI | ![](https://github.com/tobiasah/mkdocs-caption/actions/workflows/github-code-scanning/codeql/badge.svg) ![](https://github.com/tobiasah/mkdocs-caption/actions/workflows/lint.yml/badge.svg) ![](https://github.com/tobiasah/mkdocs-caption/actions/workflows/tests.yml/badge.svg) | 
-----

Enhance your [MkDocs](https://www.mkdocs.org/) documentation with easy figure, table captioning and numbering.

**Features**

* Table and Figure captioning and numbering
* Automatic link text generation for references
* Highly configurable
* Extensible to support captions for all Element types

![](docs/assets/demo.gif)

-----

## Documentation

For full documentation, visit [https://tobiasah.github.io/mkdocs-caption/](https://tobiasah.github.io/mkdocs-caption/).

## Installation

```console
pip install mkdocs-caption
```

## Quick Usage

In `mkdocs.yml`: 

```
...
plugins:
- caption
```

Inside the Markdown, the following will now be converted into a figure/table with 
caption and numbering.

```
![figure caption](img.jpg)

Table: table caption

| heading 1| heading 2 | 
| - | - | 
| content 1 | content 2 |
| content 3 | content 4 | 
```
```
<p>
  <figure id=_figure-1>
    <img src="img.jpg" />
    <figcaption>Figure 1. figure caption</figcaption>
  </figure>
</p>
<p>
<table id="_table_1">
  <thead>
    <tr>
      <th>heading 1</th>
      <th>heading 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>content 1</td>
      <td>content 2</td>
    </tr>
    <tr>
      <td>content 3</td>
      <td>content 4</td>
    </tr>
  </tbody>
  <caption>Table 1: table caption</caption>
</table>
```

## License

`mkdocs-caption` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
