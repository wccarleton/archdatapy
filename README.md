# ArchDataPy

**ArchDataPy** is a lightweight Python package for accessing archaeological datasets from R package archives in Python. It can download registered CRAN source packages, extract their `.rda` data files, and load those files with `pyreadr`. It also includes a small dataset registry for direct access to selected datasets as `pandas` DataFrames.

## Features

- **Download registered R package archives** without needing R installed.
- **List available package sources**, including `archdata` and `folio`.
- **Load `.rda` files** into Python using `pyreadr`.
- **Load selected datasets directly** from the dataset registry as `pandas` DataFrames.
- **Use custom sources** by passing a CRAN archive URL or local `.tar.gz` package archive.

## Installation

You can install `ArchDataPy` from PyPI:

```bash
pip install archdatapy
```

For local development, clone the repository and install it in editable mode:

```bash
git clone https://github.com/wccarleton/archdatapy.git
cd archdatapy
pip install -e .
```

## Dependencies

This package requires the following Python libraries:

    requests
    pyreadr
    pandas

These dependencies are automatically installed when you install the package.

## Usage

### 1. List registered package sources

The package ships with a registry in `package_registry.json`. Registered package keys currently include `archdata` and `folio`.

```python
from archdatapy import list_available_packages

print(list_available_packages())
```

### 2. Download a package and build a manifest

The `get_archdata` function accepts either:
- a registry key for a known CRAN package, or
- a direct package archive URL or local archive path.

It returns a manifest mapping dataset names to `.rda` file paths, along with package metadata.

```python
from archdatapy import get_archdata

# Download the default registered package, archdata
manifest = get_archdata()
print(manifest.package_name)
print(manifest.source_url)
print(manifest.keys())
```

To download another registered package, pass its registry key:

```python
from archdatapy import get_archdata

manifest = get_archdata(data_url="folio")
print(manifest.package_name)
print(manifest.keys())
```

### 3. Load a specific `.rda` file from the manifest

Use `load_archdata` with a path from the returned manifest.

```python
from archdatapy import load_archdata

dataset_name = 'Acheulean'  # Example key from the manifest
data = load_archdata(manifest[dataset_name])
print(data)
```

`pyreadr.read_r()` returns a dictionary-like object because a single `.rda` file can contain one or more R objects.

### 4. Load a selected dataset directly

The package also ships with a smaller dataset registry in `datasets.json`. These entries point directly to individual dataset files and can be loaded with `get_dataset`.

```python
from archdatapy import get_dataset, list_available_datasets

print(list_available_datasets())
mask_site = get_dataset("MaskSite")
print(mask_site.head())
```

### 5. Use your own package source

If you want to use a different CRAN package archive, pass the archive URL or local `.tar.gz` path directly:

```python
manifest = get_archdata(data_url='https://cran.r-project.org/src/contrib/yourpackage_1.0.0.tar.gz')
```

## Documentation

Full documentation is available on the GitHub Pages site: https://wccarleton.github.io/archdatapy

## Contributing

Contributions are welcome. Please feel free to submit issues or pull requests to improve the package.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Roadmap

Future enhancements planned for ArchDataPy:

### High Priority (Completed ✅)
- [x] Registry-based package sourcing system
- [x] Modern packaging with `pyproject.toml` (PEP 517/518/621)
- [x] Type hints for better IDE support
- [x] Automated CI/CD with GitHub Actions
- [x] `.gitignore` and `MANIFEST.in` for clean distribution

### Medium Priority
- [ ] Expand package registry with curated archaeology datasets
- [ ] Add structured logging instead of print statements
- [ ] Improve error messages with helpful recovery suggestions
- [ ] Add `CONTRIBUTING.md` guide for registry contributions
- [ ] Include metadata (DOI, citations) in registry entries

### Lower Priority
- [ ] Optional caching layer for `load_archdata()`
- [ ] Docstring examples and doctests
- [ ] Dependency version compatibility checking
- [ ] GitHub issue/PR templates
- [ ] Support for additional data formats beyond `.rda`

### Contributing to the Registry

To add new package sources to the package registry:

1. Fork the repository
2. Edit `archdatapy/package_registry.json` to add your source
3. Submit a pull request with a description of the package and datasets

Registry entries should follow this structure:

```json
{
  "package_name": {
    "url": "https://cran.r-project.org/src/contrib/package_1.0.0.tar.gz",
    "description": "Description of the package and datasets",
    "homepage": "https://CRAN.R-project.org/package=package",
    "license": "Package license"
  }
}
```

## Acknowledgments

The default registry includes datasets from the R `archdata` package, a collection of archaeological datasets maintained on CRAN. It provides the datasets used in [Quantitative Methods in Archaeology Using R](https://doi.org/10.1017/9781139628730) by David L. Carlson.
