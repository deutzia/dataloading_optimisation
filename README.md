# DLRM

## Launching terabyte dataloading pipeline with benchmark

### Overview
- `/scripts/terabyte_dataloading_benchmark.py` is a script for launching a pipeline for sample data with `data_utils.py`. It uses files: `/scripts/terabyte_test_data_divider.py`, `/scripts/terabyte_data_files_utils.py`.

- `/scripts/terabyte_test_data_divider.py` splits the file `day_0_repr_sample_1000r` into 24 files required by `data_utils.py`.

- `/scripts/terabyte_data_files_utils.py` has a function for removing all files created by `/scripts/data_divider.py` and `data_utils.py`.

- `/scripts/terabyte_dataloading_benchmark.py` should be run in `/` (the main directory) as a working directory.

- `/test_data/` is a directory, where `day_0_repr_sample_*` files should be placed manually before launching `/scripts/terabyte_dataloading_benchmark.py`.

### Steps to launch terabyte dataloading pipeline
- put `day_0_repr_sample_*` files in directory `/test_data/`,

- run `python3 scripts/terabyte_dataloading_benchmark.py --data-utils-dir DATA_UTILS_DIR` in `/`, where `DATA_UTILS_DIR` is a directory including your `data_utils.py`.

- to see more options of launching, run `python3 scripts/terabyte_dataloading_benchmark.py -h`.

## Comparing outputs of a custom data_utils and the tgrel's orignal one

To compare outputs of the `/DATA_UTILS_DIR/data_utils.py` provided by a user and the tgrel's original one (`/dlrm_tgrel/data_utils.py`)
run `python3 scripts/cmp_data_utils_outputs.py --data-utils-dir DATA_UTILS_DIR` in `/`

(it defaultly compares results for `day_0_repr_sample_1000r`, which should be put in `/test_data/`).

If you would like to compare outputs for another data file, type:

`python3 scripts/cmp_data_utils_outputs.py --data-utils-dir DATA_UTILS_DIR --data-file DATA_FILE`,

where `DATA_FILE` is one of the following:
- `day_0_repr_sample_24r`
- `day_0_repr_sample_1000r`
- `day_0_repr_sample_small`
- `day_0_repr_sample_medium`
- `day_0_repr_sample_big`
