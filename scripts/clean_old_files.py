if __name__ == "__main__":
    import importlib
    importlib.import_module('ensure_paths')

from scripts import terabyte_data_files_utils

if __name__ == "__main__":
    basic_path = "./test_data"
    terabyte_data_files_utils.clean_old_files(basic_path)
