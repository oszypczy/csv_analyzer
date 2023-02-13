import sys
import os
import argparse
from pathlib import Path
from zaliczenie_csv_analizer_io import get_files_data, write_to_json


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--columns", action="store_true")
    parser.add_argument("--rows", action="store_true")
    parser.add_argument("--unique", action="store_true")
    parser.add_argument("--count", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("-f", action="store_true")
    args = parser.parse_args(arguments[1:])
    path = Path(args.directory)
    list_of_csv_files = path.glob('**/*.csv')
    list_of_files = get_files_data(list_of_csv_files)
    if args.columns:
        for each_file in list_of_files:
            print(f"{each_file.path} columns: {each_file.get_headers()}")
    if args.rows:
        for each_file in list_of_files:
            print(f"{each_file.path} rows: {each_file.get_num_of_rows()}")
    if args.unique:
        for each_file in list_of_files:
            print(f"{each_file.path} data:")
            print(f"Columns and unique values in them: {each_file.get_unique_values_number()}") # noqa 551
    if args.count:
        for each_file in list_of_files:
            print(f"{each_file.path} data:")
            print(f"Columns with values (each value with appearences): {each_file.get_counted_values()}") # noqa 551
    if args.out:
        if os.path.exists(args.out):
            if not args.f:
                raise FileExistsError("File with this name already exists!")
        with open(args.out, 'w') as handle:
            write_to_json(handle, args, list_of_files)


if __name__ == "__main__":
    main(sys.argv)
