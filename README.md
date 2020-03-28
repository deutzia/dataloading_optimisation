# dataloading_optimisation
Contents:
- [DLRM](https://github.com/deutzia/dataloading_optimisation/tree/dlrm_dev#DLRM)
  - [Launching terabyte dataloading pipeline with benchmark](https://github.com/deutzia/dataloading_optimisation/tree/dlrm_dev#launching-terabyte-dataloading-pipeline-with-benchmark)
    - [Overview](https://github.com/deutzia/dataloading_optimisation/tree/dlrm_dev#overview)
    - [Steps to launch terabyte dataloading pipeline](https://github.com/deutzia/dataloading_optimisation/tree/dlrm_dev#steps-to-launch-terabyte-dataloading-pipeline)

# DLRM

## Launching terabyte dataloading pipeline with benchmark

### Overview
- `/dlrm/terabyte_dataloading_benchmark.py` is a script for launching a pipeline for sample data. It uses files: `/dlrm/data_divider.py`, `/dlrm/data_utils.py`, `/dlrm/data_cleaner.py`.

- `/dlrm/data_divider.py` splits the file `day_0_repr_sample_1000r` into 24 files required by `/dlrm/data_utils.py`.

- `/dlrm/data_cleaner.py` removes all files created by `/dlrm/data_divider.py` and `/dlrm/data_utils.py`.

- `/dlrm/terabyte_dataloading_benchmark.py` should be run in `/dlrm/` as a working directory.

- `/dlrm/test_data/` is a directory, where `day_0_repr_sample_*` files should be placed manually before launching `/dlrm/terabyte_dataloading_benchmark.py`.

### Steps to launch terabyte dataloading pipeline
- put `day_0_repr_sample_*` files in directory `/dlrm/test_data/`,

- go to `/dlrm/` directory and run `python3 terabyte_dataloading_benchmark.py`.


## Comparing outputs of the current data_utils and the tgrel's orignal one

To compare outputs of the current ./dlrm/data_utils.py and original the tgrel's original one (./dlrm/tgrel_data_utils.py)
run `python3 ../scripts/cmp_data_utils_outputs.py` in `/dlrm/`

(it defaultly compares results for `day_0_repr_sample_1000r`, which is located in `/dlrm/test_data/`).

If you would like to compare outputs for another data file, type:

`python3 ../scripts/cmp_data_utils_outputs.py <data_file_name>`,

where `<data_file_name>` is one of the following:
- `day_0_repr_sample_24r`
- `day_0_repr_sample_1000r`
- `day_0_repr_sample_small`
- `day_0_repr_sample_medium`
- `day_0_repr_sample_big`
