from itertools import islice
from os import path


def divide_data(basic_path, datafile):
    total_count = 0
    if path.exists(datafile):
        print("Reading data from path=%s" % (datafile))
        with open(str(datafile)) as f:
            for _ in f:
                total_count += 1
    else:
        print("file " + datafile + " not found!")

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
