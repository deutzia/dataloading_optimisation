from dlrm import terabyte_test_data_divider
from dlrm import terabyte_data_files_utils
from dlrm import data_utils


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
    basic_path = "./test_data"
    datafile = "./test_data/day_0_repr_sample_1000r"
    data_utils_module = data_utils

    launch_dataloading(basic_path, datafile, data_utils_module)
    terabyte_data_files_utils.clean_old_files(basic_path)
