# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/).

## [Unreleased]

### Added

- Added tests for some functions in build and utils.
- Added more doc strings to functions.

### Changed

- **Breaking change**: Merged parse_post into parse_page, build_post into
  build_page, and build/blog.py render_template into build/site.py the
  render_template and moved all to build/\__init__.py. This required moving
  dictionary created from blog.yml into a sub-dictionary of the site.yml
  dictionary. This will break any templates from version 0.1 that relied
  on being passed a blog dictionary.
- Added .strip() to data\['page_text'] assignment in parse_page.
- Reformatted build/\__init__.py build/blog.py and build/site.py with Black.

## 0.1 - 2018-12-27

### Added

- Site building functionality
- Blog building functionality