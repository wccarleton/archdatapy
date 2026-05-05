# Changelog

All notable changes to ArchDataPy will be documented in this file.

The format is based on Keep a Changelog, and this project uses semantic
versioning where practical.

## [1.1.0] - 2026-05-05

### Added

- Added registry-based package sourcing for known CRAN package archives.
- Added `ArchdataManifest` metadata for package name and source URL.
- Added `list_available_packages()` for package registry discovery.
- Added `get_dataset()` and `list_available_datasets()` for individual dataset registry access.
- Added the `folio` package to the default package registry.
- Added modern package metadata for PyPI publication.

### Changed

- Moved package metadata to `pyproject.toml`.
- Updated the README installation instructions for PyPI.

## [1.0.0] - 2024-05-04

### Added

- Initial package for downloading R `archdata` package archives and loading `.rda` files with `pyreadr`.
