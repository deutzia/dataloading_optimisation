import os
from os import path


def file_names(basic_path):
    file_names = [f"{basic_path}/day_day_count.npz",
                  f"{basic_path}/terabyte_processed.npz",
                  f"{basic_path}/day_fea_count.npz"]

    for i in range(24):
        file_names += [f"{basic_path}/day_{i}"]

    for i in range(26):
        file_names += [f"{basic_path}/day_{i}.npz",
                       f"{basic_path}/day_fea_dict_{i}.npz",
                       f"{basic_path}/day_{i}_processed.npz"]
    return file_names


def clean_old_files(basic_path):
    for file_name in file_names(basic_path):
        if path.exists(file_name):
            print(f"removing old file: {file_name}")
            os.remove(file_name)
