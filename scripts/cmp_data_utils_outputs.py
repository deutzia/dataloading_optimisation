import sys
import os
from os import path

if __name__ == "__main__":
    import importlib
    importlib.import_module('ensure_paths')

# Ensures that the results of tgrel_data_utils.py for the data_file exist in the files system.
# It they are absent, they will be created.
def ensure_tgrel_results_exists(data_file):
    from dlrm import terabyte_data_files_utils
    from dlrm import terabyte_dataloading_benchmark
    from dlrm import tgrel_data_utils

    basic_path = "./test_data/tgrel"
    used_datafile_path = f"{basic_path}/used_datafile"

    if not os.path.exists(basic_path):
        os.makedirs(basic_path)

    recreate_tgrel_outputs = False
    try:
        recreate_tgrel_outputs = open(used_datafile_path).read() != data_file
    except:
        recreate_tgrel_outputs = True

    recreate_tgrel_outputs |= any(map(lambda file_name: not path.exists(file_name),
                                      terabyte_data_files_utils.file_names(basic_path)))

    if recreate_tgrel_outputs:
        with open(used_datafile_path, "w+") as f:
            f.write(data_file)
        terabyte_dataloading_benchmark.launch_dataloading(basic_path=basic_path, datafile=data_file,
                                                          data_utils_module=tgrel_data_utils)


if __name__ == "__main__":
    from dlrm import terabyte_dataloading_benchmark
    from dlrm import data_utils
    import numpy as np
    from npz_diff import npz_equal

    # Disable stdout and stderr
    devnull = open(os.devnull, "w")
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = devnull
    sys.stderr = devnull

    # Create data_utils outputs
    data_file = "./test_data/day_0_repr_sample_1000r"
    ensure_tgrel_results_exists(data_file)
    terabyte_dataloading_benchmark.launch_dataloading(basic_path="./test_data", datafile=data_file,
                                                      data_utils_module=data_utils)

    # Enable stdout and stderr
    sys.stdout = stdout
    sys.stderr = stderr

    # Compare dictionaries created by the data_utils scripts
    equal_results = True
    for suffix in [f"day_fea_dict_{i}.npz" for i in range(26)]:
        if not npz_equal(f"./test_data/tgrel/{suffix}", f"./test_data/{suffix}"):
            equal_results = False

    print(f"The results of data_utils.py and tgrel_data_utils.py are {'' if equal_results else 'NOT '}equal.")
