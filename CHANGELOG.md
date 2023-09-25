# Changelog

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