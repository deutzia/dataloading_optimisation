# dataloading_optimisation
Contents:
- [DLRM](https://github.com/deutzia/dataloading_optimisation/new/dlrm_dev#DLRM)
  - [Launching terabyte dataloading pipeline with benchmark](https://github.com/deutzia/dataloading_optimisation/new/dlrm_dev#launching_terabyte_dataloading_pipeline_with_benchmark)

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
