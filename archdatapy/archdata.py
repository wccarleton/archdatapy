import os
import tarfile
import tempfile
import requests
import pyreadr
import json
import pandas as pd


class ArchdataManifest(dict):
    """Dictionary-like manifest with metadata for extracted R package datasets."""

    def __init__(self, files, package_name=None, source_url=None):
        super().__init__(files)
        self.package_name = package_name
        self.source_url = source_url

    def to_dict(self):
        return dict(self)


def _load_package_registry():
    registry_path = os.path.join(os.path.dirname(__file__), 'package_registry.json')
    with open(registry_path, 'r') as f:
        return json.load(f)


def _resolve_data_url(data_url):
    registry = _load_package_registry()
    if data_url is None:
        if 'archdata' in registry:
            return 'archdata', registry['archdata']['url']
        default_key = next(iter(registry))
        return default_key, registry[default_key]['url']

    if data_url in registry:
        return data_url, registry[data_url]['url']

    if os.path.exists(data_url):
        package_name = os.path.splitext(os.path.basename(data_url))[0]
        return package_name, data_url

    if data_url.startswith(('http://', 'https://')):
        package_name = os.path.splitext(os.path.basename(data_url))[0]
        return package_name, data_url

    raise ValueError(
        "data_url must be a registry key, a URL to a package archive, or an existing local archive path."
    )


def list_available_packages():
    """
    Lists all available package keys in the package registry.

    Returns:
        list: List of package registry keys.
    """
    registry = _load_package_registry()
    return list(registry.keys())


def _safe_extract(tar, path="."):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not os.path.commonpath([path, os.path.abspath(member_path)]) == os.path.abspath(path):
            raise Exception("Attempted Path Traversal in Tar File")
    tar.extractall(path)


def _find_rda_files(root_dir):
    file_paths = {}
    search_root = root_dir

    # Prefer package data directories named 'data'
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == 'data':
            search_root = dirpath
            break

    for dirpath, _, filenames in os.walk(search_root):
        for filename in filenames:
            if filename.endswith('.rda'):
                file_path = os.path.join(dirpath, filename)
                relative_key = os.path.relpath(file_path, search_root)
                key = relative_key.replace(os.sep, '/')
                key = key.rsplit('.', 1)[0]
                file_paths[key] = file_path

    return file_paths


def get_archdata(save_location=None, data_url=None):
    """
    Downloads and extracts datasets from an R package archive.

    Parameters:
        save_location (str): Optional directory to use for download and extraction.
            If None, uses a temporary directory.
        data_url (str): Optional package registry key or URL for the package archive.
            If None, uses the default registered package.

    Returns:
        ArchdataManifest: A dictionary-like manifest mapping dataset names to .rda paths.
    """
    package_name, resolved_url = _resolve_data_url(data_url)
    temp_dir = tempfile.mkdtemp() if save_location is None else save_location
    os.makedirs(temp_dir, exist_ok=True)

    if os.path.exists(resolved_url) and not resolved_url.startswith(('http://', 'https://')):
        tar_path = resolved_url
    else:
        tar_path = os.path.join(temp_dir, f'{package_name}.tar.gz')
        response = requests.get(resolved_url)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to download package archive from {resolved_url}.")
        with open(tar_path, 'wb') as file:
            file.write(response.content)

    with tarfile.open(tar_path, 'r:*') as tar:
        _safe_extract(tar, temp_dir)

    file_paths = _find_rda_files(temp_dir)
    if not file_paths:
        raise FileNotFoundError('No .rda files were found in the package archive.')

    return ArchdataManifest(file_paths, package_name=package_name, source_url=resolved_url)


def load_archdata(file_path):
    """
    Loads an .rda file and returns the contents using pyreadr.

    Parameters:
        file_path (str): Full path to the .rda file.

    Returns:
        dict: The result from pyreadr.read_r(), containing all objects in the .rda file.
    """
    result = pyreadr.read_r(file_path)
    return result


def _load_dataset_registry():
    """
    Loads the dataset registry from datasets.json.

    Returns:
        dict: Dictionary of available datasets.
    """
    registry_path = os.path.join(os.path.dirname(__file__), 'datasets.json')
    with open(registry_path, 'r') as f:
        return json.load(f)


def get_dataset(dataset_name, cache_dir=None):
    """
    Downloads and loads a specific dataset from the registry.

    Parameters:
        dataset_name (str): Name of the dataset to load.
        cache_dir (str): Optional directory to cache downloaded files.

    Returns:
        pandas.DataFrame or dict: The loaded dataset.
    """
    registry = _load_dataset_registry()
    if dataset_name not in registry:
        raise ValueError(f"Dataset '{dataset_name}' not found in registry.")

    dataset_info = registry[dataset_name]
    url = dataset_info['url']
    format_type = dataset_info['format']

    if cache_dir is None:
        cache_dir = tempfile.gettempdir()

    # Create cache filename
    cache_filename = f"{dataset_name}.{format_type}"
    cache_path = os.path.join(cache_dir, cache_filename)

    # Download if not cached
    if not os.path.exists(cache_path):
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to download dataset from {url}.")
        with open(cache_path, 'wb') as f:
            f.write(response.content)

    # Load based on format
    if format_type == 'csv':
        return pd.read_csv(cache_path)
    elif format_type == 'rda':
        return load_archdata(cache_path)
    else:
        raise ValueError(f"Unsupported format: {format_type}")


def list_available_datasets():
    """
    Lists all available datasets in the registry.

    Returns:
        list: List of dataset names.
    """
    registry = _load_dataset_registry()
    return list(registry.keys())
