import os
from archdatapy import get_archdata, load_archdata

def test_get_archdata():
    # Test the get_archdata function
    file_paths = get_archdata()
    
    # Check that file_paths is a dictionary
    assert isinstance(file_paths, dict), "Expected file_paths to be a dictionary"
    
    # Check that the dictionary is not empty
    assert len(file_paths) > 0, "Expected file_paths dictionary to contain entries"
    
    # Check that each key-value pair in the dictionary has the expected format
    for dataset_name, file_path in file_paths.items():
        assert isinstance(dataset_name, str), "Expected dictionary keys to be strings (dataset names)"
        assert isinstance(file_path, str), "Expected dictionary values to be strings (file paths)"
        assert os.path.exists(file_path), f"File path {file_path} does not exist"

def test_load_archdata():
    # First, get the paths from get_archdata
    file_paths = get_archdata()
    
    # Pick one dataset to load for testing
    dataset_name = next(iter(file_paths))  # Get the first dataset name
    file_path = file_paths[dataset_name]
    
    # Load the dataset
    data = load_archdata(file_path)
    
    # Check that the data returned is a dictionary (from pyreadr)
    assert isinstance(data, dict), "Expected data to be a dictionary returned by pyreadr"
    
    # Check that at least one object is present in the .rda file
    assert len(data) > 0, "Expected at least one object in the .rda file"
    
    # Check that the contents of data are pandas DataFrames
    for obj_name, obj_value in data.items():
        import pandas as pd
        assert isinstance(obj_value, pd.DataFrame), f"Expected object {obj_name} to be a pandas DataFrame"
