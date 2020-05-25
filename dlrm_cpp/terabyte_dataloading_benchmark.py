if __name__ == "__main__":
    import importlib
    importlib.import_module('ensure_paths')

import os
from dlrm import terabyte_test_data_divider
from dlrm import terabyte_data_files_utils

def launch_dataloading(basic_path, datafile):
    terabyte_data_files_utils.clean_old_files(basic_path)
    terabyte_test_data_divider.divide_data(basic_path, datafile)

    max_ind_range=-1
    sub_sample_rate=0.0
    randomize="total"
    raw_path=f"{basic_path}/day"
    memory_map=True

    os.system("../dlrm_cpp/build/dataloading_optimizations "
              f"--max-ind-range={max_ind_range} "
              f"--data-sub-sample-rate={sub_sample_rate} "
              f"--data-randomize={randomize} "
              f"--raw-data-file={raw_path} "
              f"--memory-map={memory_map}")


if __name__ == "__main__":
    basic_path = "./test_data"
    datafile = "./test_data/day_0_repr_sample_1000r"

    launch_dataloading(basic_path, datafile)
    # terabyte_data_files_utils.clean_old_files(basic_path)
