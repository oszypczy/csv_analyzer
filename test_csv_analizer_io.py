from io import StringIO
from zaliczenie_csv_analizer_io import read_from_csv, File, write_to_json
import argparse


def test_read_from_csv():
    data = "ID,name\r\n123,Oliwier\r\n420,Lidka"
    handle = StringIO(data)
    file = read_from_csv(handle, '/dane.csv')
    assert file.columns == {'ID': ['123', '420'], 'name': ['Oliwier', 'Lidka']}
    assert file.get_headers() == ['ID', 'name']
    assert file.get_num_of_rows() == 2


def test_get_unique_values_from_columns():
    data = {'ID': ['123', '420'], 'name': ['Oliwier', 'Oliwier']}
    file = File(data, '/dane.csv')
    assert file.get_unique_values_number() == {'ID': 2, 'name': 1}


def test_write_to_json():
    data = {'ID': ['123', '420'], 'name': ['Oliwier', 'Oliwier']}
    files = [File(data, '/dane.csv')]
    handle = StringIO()
    args = argparse.Namespace(columns=True, rows=True, unique=False, count=False) # noqa 551
    write_to_json(handle, args, files)
    handle.seek(0)
    content = handle.read()
    assert content == '[\n  {\n    "/dane.csv": {\n      "columns": [\n        "ID",\n        "name"\n      ],\n      "rows": 2\n    }\n  }\n]' # noqa 551


def test_get_counted_values_from_columns():
    data = {'ID': ['123', '420'], 'name': ['Oliwier', 'Oliwier']}
    file = File(data, '/dane.csv')
    assert file.get_counted_values() == {'ID': {'420': 1, '123': 1}, 'name': {'Oliwier': 2}} # noqa 551
