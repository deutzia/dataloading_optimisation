if __name__ == "__main__":
    import importlib
    importlib.import_module('ensure_paths')

from scripts import terabyte_data_files_utils, terabyte_test_data_divider

def launch_dataloading(basic_path, datafile, data_utils_module):
    terabyte_data_files_utils.clean_old_files(basic_path)
    terabyte_test_data_divider.divide_data(basic_path, datafile)

    data_utils_module.loadDataset(
        dataset="terabyte",
        max_ind_range=-1,
        sub_sample_rate=0.0,
        randomize="total",
        data_split="train",
        raw_path=f"{basic_path}/day",
        pro_data="",
        memory_map=True
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Launches data_utils.loadDataset(...) for data_utils.py provided by a user"
    )
    # model related parameters
    parser.add_argument("--data-utils-dir", type=str, required=True,
                        help="The name of the directory inlcuding the data_utils.py")
    default_data_file = "day_0_repr_sample_1000r"
    parser.add_argument("--data-file", type=str, default=default_data_file,
                        help=f"The name of the data file that will be an input for data_utils. Defaultly: {default_data_file}")
    args = parser.parse_args()

    basic_path = "./test_data"
    datafile = f"./test_data/{args.data_file}"

    data_utils_module = importlib.import_module(f"{args.data_utils_dir}.data_utils", package=True)

    launch_dataloading(basic_path, datafile, data_utils_module)
    terabyte_data_files_utils.clean_old_files(basic_path)
