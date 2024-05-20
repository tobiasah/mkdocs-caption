# Config

## Default 

The plugin can be configured in the `mkdocs.yml` file.
The default configuration is as follows:

```{ .yaml .annotate }
plugins:
  - caption:
    additional_identifier: []  # (1)!
    cross_reference_text: '{page_title}/{local_ref}'
    table: # (2)!
      enable: true
      start_index: 1
      increment_index: 1
      position: bottom
      default_id: '_table-{index}'
      reference_text: 'Table {index}'
      caption_prefix: 'Table {index}:'
      markdown_identifier: 'Table:'
      allow_indented_caption: True
    figure: # (3)!
      enable: true
      start_index: 1
      increment_index: 1
      position: bottom
      default_id: '_figure-{index}'
      reference_text: 'Figure {index}'
      caption_prefix: 'Figure {index}:'
      markdown_identifier: 'Figure:'
      allow_indented_caption: True
      ignore_alt: False
      ignore_classes: ["twemoji"]
    custom: # (4)!
      enable: true
      start_index: 1
      increment_index: 1
      position: bottom
      default_id: '_{identifier}-{index}'
      reference_text: '{Identifier} {index}'
      caption_prefix: '{Identifier} {index}:'
      markdown_identifier: '{Identifier}:'
      allow_indented_caption: True
```

1.  list of additional identifiers (e.g. [`List`, `Example`]. These identifiers will be treated as
    custom captions. Note that each identifier has its own counter.)
2.  Configuration that applies for the table captioning.
3.  Configuration that applies for the figure/image captioning.
4.  Configuration that applies for the custom element captioning. Note that this 
    configuration applies for all elements that are specified in the `additional_identifier` list.

!!! note
    The `{index}` placeholders are replaced with the current index. The `{identifier}` placeholder
    is replaced with the lower case identifier and the `{Identifier}` is replaced with the 
    capitalized identifier.

!!! warning
    The configuration in the `mkdocs.yml` file is applied to all custom identifiers.
    It is not possible to customize the figure element for a specific identifier only.

The configuration can be split in three parts: `table`, `figure` and `custom`. Each part
has the same configuration options that apply for the respective element.
The following table lists all available options.

| Option | Description |
| --- | --- |
| enable | Enable/disable the captioning/plugin for the specified identifier |
| start_index | The index to start with |
| increment_index | The increment for the index |
| position | The position of the caption (top, bottom) relative to the target element |
| default_id | The default id assigned to the resulting HTML element |
| reference_text | The text used for references to this element. Note, this only will be applied if the anchor does not specify its own link text |
| caption_prefix | The prefix put before of the caption text |
| markdown_identifier | The identifier that this plugin will search for in the markdown. (Note that every match of this identifier will be treated as a caption element. A false match will most likely result in an error) |
| allow_indented_caption | Flag if caption elements should also be parsed within indented blocks. By default this is enabled. |
| ignore_alt | Flag if the alt attribute should be ignored. This will disable the feature that 
uses the alt text as a caption. (Only available for figures) |
| ignore_classes | List of classes ignored when adding the captions. (Only available for figures) |

## Overwriting the default configuration

It is also possible to overwrite the default configuration (mkdocs.yml) for a specific page.
This can be done by adding a `caption` section to the page header.

```
---
caption:
  table:
    start_index: 4
---
# Page Title
...
```