import os
from os import path

def results_files_names(basic_path):
    file_names = []

    for i in range(24):
        file_names += [f"{basic_path}/day_{i}_reordered.npz"]

    for i in range(26):
        file_names += [f"{basic_path}/day_fea_dict_{i}.npz"]

    return file_names

def files_names(basic_path):
    files_names = results_files_names(basic_path)

    files_names += [f"{basic_path}/day_day_count.npz",
                   f"{basic_path}/terabyte_processed.npz",
                   f"{basic_path}/day_fea_count.npz"]

    for i in range(24):
        files_names += [f"{basic_path}/day_{i}",
                       f"{basic_path}/day_{i}.npz",
                       f"{basic_path}/day_{i}_processed.npz",
                       f"{basic_path}/day_{i}_intermediate_s.npy",
                       f"{basic_path}/day_{i}_intermediate_y.npy",
                       f"{basic_path}/day_{i}_intermediate_d.npy"]

    return files_names


def clean_old_files(basic_path):
    for file_name in files_names(basic_path):
        if path.exists(file_name):
            print(f"removing old file: {file_name}")
            os.remove(file_name)

if __name__ == "__main__":
    clean_old_files()