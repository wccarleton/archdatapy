import os
import tarfile
import tempfile
import requests
import pyreadr

def get_archdata(save_location=None, data_url=None):
    """
    Downloads and extracts datasets from the R archdata package.

    Parameters:
        save_location (str): Optional. Path to save extracted files. If None, uses a temporary directory.
        data_url (str): Optional. URL for the archdata package source. Defaults to CRAN URL.

    Returns:
        dict: A dictionary with extension-stripped file names as keys and full paths to the .rda files as values.
    """
    # Default CRAN URL for the archdata package source
    if data_url is None:
        data_url = "https://cran.r-project.org/src/contrib/archdata_1.2-1.tar.gz"

    # Use temporary directory if no save location is provided
    temp_dir = tempfile.mkdtemp() if save_location is None else save_location

    # Download the .tar.gz file
    tar_path = os.path.join(temp_dir, 'archdata.tar.gz')
    response = requests.get(data_url)
    if response.status_code == 200:
        with open(tar_path, 'wb') as file:
            file.write(response.content)
    else:
        raise ConnectionError("Failed to download archdata package from CRAN.")

    # Extract the .tar.gz archive to get .rda files
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(temp_dir)

    # Path to the 'data' directory within the extracted files
    data_dir = os.path.join(temp_dir, 'archdata/data')

    # Collect the file paths of all .rda files in the data directory
    file_paths = {}
    for filename in os.listdir(data_dir):
        if filename.endswith('.rda'):
            key = filename.rsplit('.', 1)[0]  # Use filename without extension as the key
            file_paths[key] = os.path.join(data_dir, filename)

    return file_paths


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
