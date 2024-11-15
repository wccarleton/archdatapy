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

1. Download and Extract Datasets

The get_archdata function downloads and extracts datasets from the R archdata package. It returns a dictionary where each key is a dataset name and each value is the path to the .rda file for that dataset.

from archdatapy import get_archdata

2. Download datasets and get file paths
file_paths = get_archdata()
print(file_paths)  # View the available datasets and their paths

3. Load a Specific Dataset

The load_archdata function takes the path to an .rda file and loads it as a pandas DataFrame (or multiple DataFrames, depending on the dataset). This function wraps around pyreadr to simplify loading R data files in Python.

```python
from archdatapy import load_archdata

# Load a specific dataset
dataset_name = 'YourDatasetName'  # Replace with an actual dataset name from file_paths keys
data = load_archdata(file_paths[dataset_name])
print(data)  # View the loaded dataset
```

## Documentation

Full documentation is available on the GitHub Pages site: https://wccarleton.github.io/archdatapy

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the package.
License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

The datasets are sourced from the archdata R package, a collection of archaeological datasets maintained by CRAN. It provides all of the data sets used in [Quantitative Methods in Archaeology Using R](https://doi.org/10.1017/9781139628730) by David L Carlson, one of the Cambridge Manuals in Archaeology.