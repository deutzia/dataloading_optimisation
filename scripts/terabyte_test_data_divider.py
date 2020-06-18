from itertools import islice
from os import path

if __name__ == "__main__":
    import importlib
    importlib.import_module('ensure_paths')

def divide_data(basic_path, datafile):
    total_count = 0
    if path.exists(datafile):
        print("Reading data from path=%s" % (datafile))
        with open(str(datafile)) as f:
            for _ in f:
                total_count += 1
    else:
        print("Error: file " + datafile + " not found!")
        exit(1)

    print(f"Found {total_count} data entries")
    file_count = 24;
    print(f"Dividing it into {file_count} files")
    per_file = total_count // 24

    input_file = open(str(datafile))
    for i in range(24):
        output_file = open(f"{basic_path}/day_{i}", "w")
        line_to_write_count = per_file
        if i == 23:
            line_to_write_count += (total_count % per_file)
        print(f"generating day {i} file (populated with {line_to_write_count} entries)")
        for q in range(per_file):
            line = input_file.readline()
            output_file.write(line)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Divides data file into 24 files"
    )
    # model related parameters
    default_data_file = "day_0_repr_sample_1000r"
    parser.add_argument("--data-file", type=str, default=default_data_file,
                        help=f"The name of the data file that will be an input for data_utils. Defaultly: {default_data_file}")
    args = parser.parse_args()

    basic_path = "./test_data"
    datafile = f"./test_data/{args.data_file}"

    divide_data(basic_path, datafile)