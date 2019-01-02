# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/).

## [0.2] - 2019-01-01

### Added

- build_indices now passes the number of of indices to templates.
- Added tests.
- Added more doc strings to functions.

### Changed

- Enabled trim_blocks and lstrip_blocks for Jinja2 templates to remove
  blank lines in output.
- In build/blog.build_indices, site\['blog']\['continue'] is set to None now
  instead of False if there is only one index to build.
- Fixed build_indices so that it properly handles multiple indices.
- **Breaking change**: Merged parse_post into parse_page, build_post into
  build_page, and build/blog.py render_template into build/site.py the
  render_template and moved all to `build/__init__.py`. This required moving
  dictionary created from blog.yml into a sub-dictionary of the site.yml
  dictionary. This will break any templates from version 0.1 that relied
  on being passed a blog dictionary.
- Added .strip() to data\['page_text'] assignment in parse_page.
- Reformatted `build/__init__.py` build/blog.py and build/site.py with Black.

## 0.1 - 2018-12-27

### Added

- Site building functionality
- Blog building functionality

[0.2]: https://github.com/wtee/anesgesgi/compare/v0.1.0...v0.2.0