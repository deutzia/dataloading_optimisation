import sys
import os
from os import path
import bcolors

if __name__ == "__main__":
    import importlib
    importlib.import_module('ensure_paths')

def lacking_results_files(basic_path):
    from scripts import terabyte_data_files_utils

    lacking = []
    for file_name in terabyte_data_files_utils.results_files_names(basic_path):
        if (not path.exists(file_name)):
            lacking.append(file_name)

    return lacking

# Ensures that the results of data_utils.py for the data_file exist in the files system.
# It they are absent, they will be created.
def ensure_tgrel_results_exists(data_file):
    from scripts import terabyte_dataloading_benchmark
    from dlrm_tgrel import data_utils

    basic_path = "./test_data/tgrel"
    used_datafile_path = f"{basic_path}/used_datafile"

    if not os.path.exists(basic_path):
        os.makedirs(basic_path)

    recreate_tgrel_outputs = False
    try:
        recreate_tgrel_outputs = open(used_datafile_path).read() != data_file
    except:
        recreate_tgrel_outputs = True

    recreate_tgrel_outputs |= (lacking_results_files(basic_path) != [])

    if recreate_tgrel_outputs:
        with open(used_datafile_path, "w+") as f:
            f.write(data_file)
        terabyte_dataloading_benchmark.launch_dataloading(basic_path=basic_path, datafile=data_file,
                                                          data_utils_module=data_utils)


# Loads records from day_{d}_reordered.npz files for all days,
# transforms the records categorical features from following integers to original hashes
#   (using day_fea_dict_{i}.npz files)
# Returns the records sorted.
def get_records_sorted(basic_path):
    dict = [[] for i in range(26)]

    for i in range(26):
        with np.load(f"{basic_path}/day_fea_dict_{i}.npz") as f:
            dict[i] = f["unique"]

    records = []

    for d in range(24):
        with np.load(f"{basic_path}/day_{d}_reordered.npz") as f:
            for (y, x_int, x_cat) in zip(f["y"], f["X_int"], f["X_cat"]):
                line = [0 for i in range(1 + 13 + 26)]
                line[0] = int(y)
                line[1:14] = map(lambda x: int(x), x_int)
                for j in range(26):
                    line[j + 14] = dict[j][int(x_cat[j])]
                records.append(line)

    records.sort()
    return records


if __name__ == "__main__":
    from scripts import terabyte_dataloading_benchmark
    import numpy as np
    import argparse

    parser = argparse.ArgumentParser(
        description="Compares outputs of original tgrel's data_utils.py and data_utils provided by a user"
    )
    # model related parameters
    parser.add_argument("--data-utils-dir", type=str, required=True,
                        help="The name of the directory inlcuding the data_utils.py script to be tested")
    default_data_file = "day_0_repr_sample_1000r"
    parser.add_argument("--data-file", type=str, default=default_data_file,
                        help=f"The name of the data file that will be used to test the script. Defaultly: {default_data_file}")
    args = parser.parse_args()

    data_utils = importlib.import_module(f"{args.data_utils_dir}.data_utils", package=True)

    # Disable stdout and stderr
    devnull = open(os.devnull, "w")
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = devnull
    sys.stderr = devnull

    # Create data_utils outputs
    data_file = f"./test_data/{args.data_file}"
    ensure_tgrel_results_exists(data_file)
    terabyte_dataloading_benchmark.launch_dataloading(basic_path="./test_data", datafile=data_file,
                                                      data_utils_module=data_utils)
    # Enable stdout and stderr
    sys.stdout = stdout
    sys.stderr = stderr

    lacking_files = lacking_results_files("./test_data")
    if (lacking_files != []):
        sys.stderr.write(f"{bcolors.ERR}Results files to check are not created. Missing files:\n")
        for f in lacking_files:
            sys.stderr.write(f"{f}\n")
        sys.stderr.write(f"{bcolors.ENDC}")
        sys.exit(1)

    # Compare results of the data_utils scripts
    tgrel_records = get_records_sorted("./test_data/tgrel")
    records = get_records_sorted("./test_data")

    equal_results = tgrel_records == records

    color = bcolors.OK if equal_results else bcolors.ERR
    print(
        f"{color}The results of data_utils.py and dlrm_tgrel/data_utils.py for {data_file}"\
        f" are {'' if equal_results else 'NOT '}equal.{bcolors.ENDC}")
    sys.exit(not equal_results)
