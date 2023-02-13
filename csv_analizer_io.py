import csv
import json


def read_from_csv(handle, path):
    headers = handle.readline().split(',')
    headers = [header.rstrip() for header in headers]
    handle.seek(0)
    data = {}
    reader = csv.DictReader(handle)
    for each_header in headers:
        values = []
        for row in reader:
            values.append(row[each_header])
        data[each_header] = values
        handle.seek(0)
        reader = csv.DictReader(handle)
    return File(data, path)


def write_to_json(handle, args, files):
    data = []
    for file in files:
        file_data = {}
        inside_dict = {}
        if args.columns:
            columns = file.get_headers()
            inside_dict['columns'] = columns
        if args.rows:
            rows = file.get_num_of_rows()
            inside_dict['rows'] = rows
        if args.unique:
            unique = file.get_unique_values_number()
            inside_dict['unique_values'] = unique
        if args.count:
            counted = file.get_counted_values()
            inside_dict['counted_values'] = counted
        file_data[file.path] = inside_dict
        data.append(file_data)
    json.dump(data, handle, indent=2)


def get_files_data(files):
    final_list = []
    for each_file in files:
        with open(str(each_file), 'r') as handle:
            final_list.append(read_from_csv(handle, str(each_file)))
    return final_list


class File:
    def __init__(self, data, path):
        self.columns = data
        self.path = path

    def get_headers(self):
        return list(self.columns.keys())

    def get_num_of_rows(self):
        rows = list(self.columns.values())
        return len(rows[0])

    def get_unique_values_number(self):
        final_dict = {}
        for each_key in list(self.columns.keys()):
            final_dict[each_key] = len(set(self.columns[each_key]))
        return final_dict

    def get_counted_values(self):
        final_dict = {}
        for each_key in list(self.columns.keys()):
            local_dict = {}
            for each_value in set(self.columns[each_key]):
                local_dict[each_value] = self.columns[each_key].count(each_value) # noqa 551
            final_dict[each_key] = local_dict
        return final_dict
