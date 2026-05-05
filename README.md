# ArchDataPy

**ArchDataPy** is a lightweight Python package designed to access and work with archaeological datasets from the R `archdata` package in Python. It provides tools to download the data directly from CRAN, extract the datasets, and load them as `pandas` DataFrames for easy analysis and manipulation.

## Features

- **Download datasets** from the R `archdata` package without needing R installed.
- **Load datasets** directly into Python as `pandas` DataFrames using `pyreadr`.
- Provides an efficient and Pythonic way to access widely used archaeological datasets.

## Installation

You can install `ArchDataPy` by cloning the repository and installing it locally:

```bash
git clone https://github.com/yourusername/archdatapy.git
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

### 1. Download packages and build a manifest

The `get_archdata` function now accepts either:
- a registry key for a known CRAN package, or
- a direct package archive URL or local archive path.

It returns a manifest mapping dataset names to `.rda` file paths, along with package metadata.

```python
from archdatapy import get_archdata

# Download the default registered package
manifest = get_archdata()
print(manifest.package_name)
print(manifest.source_url)
print(manifest.keys())
```

### 2. Load a specific dataset from the manifest

Use `load_archdata` with a path from the returned manifest.

```python
from archdatapy import load_archdata

dataset_name = 'Acheulean'  # Example key from the manifest
data = load_archdata(manifest[dataset_name])
print(data)
```

### 3. Use the built-in package registry

The package ships with a prebuilt registry in `package_registry.json`.
You can list available package registry keys and then pass one to `get_archdata`.

```python
from archdatapy import list_available_packages, get_archdata

print(list_available_packages())
manifest = get_archdata(data_url='archdata')
```

### 4. Add your own package source

If you want to use a different CRAN package archive, pass the archive URL or local `.tar.gz` path directly:

```python
manifest = get_archdata(data_url='https://cran.r-project.org/src/contrib/yourpackage_1.0.0.tar.gz')
```

### 5. Load R objects from `.rda` files

The `load_archdata` function currently uses `pyreadr`, so it can extract the R objects contained in the `.rda` file and return them as Python objects.

```python
data = load_archdata(manifest['YourDatasetName'])
print(data)
```

## Documentation

Full documentation is available on the GitHub Pages site: https://wccarleton.github.io/archdatapy

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the package.
License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

The datasets are sourced from the archdata R package, a collection of archaeological datasets maintained by CRAN. It provides all of the data sets used in [Quantitative Methods in Archaeology Using R](https://doi.org/10.1017/9781139628730) by David L Carlson, one of the Cambridge Manuals in Archaeology.