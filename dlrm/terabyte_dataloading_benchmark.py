import terabyte_test_data_divider
import terabyte_data_cleaner
import data_utils

if __name__ == "__main__":
    terabyte_data_cleaner.clean_old_files()
    terabyte_test_data_divider.divide_data()

    data_utils.loadDataset(
        dataset="terabyte",
        max_ind_range=-1,
        sub_sample_rate=0.0,
        randomize="total",
        data_split="train",
        raw_path="./test_data/day",
        pro_data="",
        memory_map=False
    )
    terabyte_data_cleaner.clean_old_files()
