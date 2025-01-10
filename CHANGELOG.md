# Changelog

## Version 1.3.0

* Fix bug in the post processing which cause references with ids which contain other ids
  to be replaced with the wrong text.
* Adapt figure generation to allow packing multiple images into the same figure.
  This is necessary to e.g allow having different images for light and dark mode.
* Fix bug in the post processing which causes the windows build to fail.
* Fix bug in the post processing which causes incorrect substitutions when a
  reference to a target is placed before the target.

## Version 1.2.0

* Allow automatic link text generation across different pages.

## Version 1.1.0

* Allow markdown syntax within the caption element.

## Version 1.0.0

* Prevent conversion of emojis into figure elements with captions.
* Add new config parameter `ignore_classes` to explicitly prevent conversion 
  of specific images into figures.

## Version 0.0.11

* Prevent conversion of inline images even if they have an alt text (#9)

## Version 0.0.10

* Allow caption elements within indented blocks (e.g. admonitions). Can be disabled
  with the `allow_indented_caption` option.

## Version 0.0.9

* Fixed problem of leaking the figure caption element into the resulting HTML.
* Allow specifying the position of the caption for tables.
* Allow specifying the position of the caption for custom captions.
* Fix bug where the caption identifier was picked up even if it was not 
  the first word in the line.
* Allow multiline captions

## Version 0.0.8

* Introduce the `Figure` identifier to allow the same kind of syntax for images and tables.
  This also allows adding custom attributes to the figure element.
* Allow customizing the Markdown identifier for a caption through `markdown_identifier`.
* Add missing `from __future__ import annotations` to allow type annotations in Python 3.8

### Breaking Changes

* Rename `identifier` in the individual config options to `default_id`. This change was necessary 
  because it caused a lot of confusion since the identifier term is used by this plugin 
  to refer to `Table`, `Figure` and `Custom` **identifier**.