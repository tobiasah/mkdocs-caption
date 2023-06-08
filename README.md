# MkDocs Caption

| | |
| --- | --- |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-caption.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/mkdocs-caption/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-caption.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/mkdocs-caption/) |
| Meta | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)|

-----

Enhance your [MkDocs](https://www.mkdocs.org/) documentation with easy figure, table captioning and numbering.

**Features**

* Table and Figure captioning and numbering
* Automatic link text generation for references
* Highly configurable
* Extensible to support captions for all Element types

-----

**Table of Contents**

- [Installation](#installation)
- [Quick Usage](#license)
- [Images](#images)
- [Tables](#tables)
- [Custom captions](#custom-captions)
- [Configuration](#configuration)
- [License](#license)

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

Inside the Markdown the follwoining will now be converted into a figure/table with 
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

## Images

The plugin uses the title attribute as the source for the caption. The fallback
is the alt attribute. If neither is present the image will not be captioned.
The caption is prefixed with the image number. The image number is incremented
for every image that is captioned.

Markdown this offers three ways to add a caption to an image.

```
![figure caption](img.jpg)

![](img.jpg "figure caption")

![](img.jpg){title="figure caption"}
```

Each captioned image is also assosiated with an id, which by default is constructed
from the image number (`_figure-x`). It is also possible to overwrite the default id
by adding an attribute `id` to an image. The id can be used to link to the image.
The plugin also adds a link text (`figure x`) to all references without a link text.
Please note that this feature does not support cross page references.

```
take a look at [](#_figure-1).
```
```
take a look at <a href="#_figure-1">figure 1</a>.
```

## Tables

The plugin allows easy captioning of tables in markdown. Since Markdown does not
support captions for tables the plugin uses a custom syntax here. A predefined prefix
is used to identify a table caption (`Table:`). The caption must be placed right 
before the table (even if the caption should be at the bottom of the table).
The caption is prefixed with the table number. The table number is incremented
for every image that is captioned.

```
Table: table caption

| heading 1| heading 2 |
| - | - |
| content 1 | content 2 |
...
```
Each captioned table is also assosiated with an id, which by default is constructed
from the table number (`_table-x`). It is also possible to overwrite the default id
by adding an attribute `id` to the table (see below). The id can be used to link to the
table. The plugin also adds a link text (`table x`) to all references without a link text.
Please note that this feature does not support cross page references.

```
take a look at [](#_table-1).
```
```
take a look at <a href="#_table-1">table 1</a>.
```

The caption can also be extendet by attributes that are automatically added to the
table element. The attributes are specified similar to image attributes be curly brackets.
There are two attributes that have special meaning: `id` and `cols`.
The `id` attribute is used to overwrite the default id of the table. The `cols`
attribute can be used to controll the column width of the table.

```
Table: table caption {id="my-table" cols="1,3"}

| heading 1| heading 2 |
| - | - |
| content 1 | content 2 |
...
```
<table id="my-table">
  <colgroup>
    <col width="25%" span="1">
    <col width="75%" span="1">
  </colgroup>
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

Note that the sum of the specified column widths is treated as 100%.

## Custom captions

In addition to tables and figures the plugin also supports custom captions. 
Custom captions must be manually defined in the `mkdocs.yml` file. Similar to 
table captions the are placed right before the target element (e.g. an enumeration).
The plugin will wrap the target element in a figure with the specified caption and
options.

In `mkdocs.yml`: 

```
...
plugins:
- caption:
    additional_identifier: [`List`]
```

In Markdown:

```
List: list caption

1. item 1
2. item 2
```

```
<figure id="_list-1">
  <ul>
    <li>item 1</li>
    <li>item 2</li>
  </ul>
  <figcaption>List 1: list caption</figcaption
</figure>
```

The same configuration options as for the table also apply for the custom captions.
Note that each identifier has its own counter.

## Configuration

The plugin can be configured in the `mkdocs.yml` file. The following options are available:

```
plugins:
  - caption:
    additional_identifier: [] # list of additional identifiers (e.g. [`List`, `Example`])
    table:
      enable: true
      start_index: 1
      increment_index: 1
      position: bottom  # (top, bottom)
      identifier: '_table-{index}'
      reference_text: 'table {index}'
      caption_prefix: 'Table {index}:'
    figure:
      enable: true
      start_index: 1
      increment_index: 1
      position: bottom
      identifier: '_figure-{index}'
      reference_text: 'figure {index}'
      caption_prefix: 'figure {index}:'
    custom:
      enable: true
      start_index: 1
      increment_index: 1
      position: bottom
      identifier: '_{identifier}-{index}'
      reference_text: '{identifier} {index}'
      caption_prefix: '{identifier} {index}:'
```

The `{index}` placeholders is replaced with the current index. The `{identifier}` placeholder
is replaced with the identifier of the current element and is only relevant for the custom option.  

It is also possible to overwrite the default configuration for a specific page. This can be
done by adding a `caption` section to the page header.

```
---
caption:
  table:
    start_index: 4
---
# Page Title
...
```

## License

`mkdocs-caption` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
