import csv
from datetime import datetime
from typing import Any, Union, Type
from venv import logger

import pandas as pd
import plotly.express as px

# DEFAULT_COURSE_ID, DEFAULT_COURSE_DIR = "course-v1:ITMOUniversity+DATANTECH2035+summer_2022_1", "DATANTECH2035"
# DEFAULT_COURSE_ID, DEFAULT_COURSE_DIR = "course-v1:ITMOUniversity+DATSTBASE+spring_2024_ITMO_bac", "DATSTBASE"
DEFAULT_COURSE_ID, DEFAULT_COURSE_DIR = "course-v1:ITMOUniversity+DATSTPRO+spring_2024_ITMO_bac", "DATSTPRO"

RESULT_PATH = f'../../../../metric_results/{DEFAULT_COURSE_DIR}/'
# RESULT_PATH = './metric_results/existing/'

def save_output_to_file(result_file, result, field_names, result_path=RESULT_PATH):
    print(f'Save result to file {result_file}')
    with open(result_path + result_file, mode='w', encoding='utf-8', newline='') as res_file:
        result_file_writer = csv.writer(res_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        result_file_writer.writerow(field_names)
        for res in result:
            result_file_writer.writerow(res)
    logger.info('Result is in the file ', result_path + result_file)


def find_alias(url, urls_and_names_mapping):
    for url_mapping in urls_and_names_mapping:
        if url_mapping[0] == url + '/':
            return url_mapping[1]
    return None


def generate_bar_figure(result_file, fields, xaxis_title=None, yaxis_title=None):
    data = pd.read_csv(RESULT_PATH + result_file)
    fig = px.bar(data, x=fields[0], y=fields[1])
    if xaxis_title and yaxis_title:
        fig.update_layout(xaxis_title=xaxis_title, yaxis_title=yaxis_title)
    fig.show()


def generate_line_figure(result_file, fields):
    data = pd.read_csv(result_file)
    fig = px.line(data, x=fields[0], y=fields[1])
    fig.show()


ColumnType = Union[str, int, float, datetime]

def convert_value(value: str, desired_type: Type[ColumnType]) -> ColumnType:
    try:
        if desired_type == datetime:
            return desired_type.strptime(value, '%Y-%m-%d')
        return desired_type(value)
    except TypeError:
        return None

def csv_to_json(csv_file_path: str, column_types: dict[str, Type[ColumnType]]) -> list[dict[str, ColumnType]]:
    logger.info("Parsing csv file")
    json_data = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        headers = csv_reader.fieldnames
        for row in csv_reader:
            json_row = {header: convert_value(row[header], column_types.get(header, str)) for header in headers}
            json_data.append(json_row)
    return json_data

def get_single_value_from_csv(csv_file_path: str) -> int:
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            return int(row[0])

if __name__ == '__main__':
    # print(csv_to_json(
    #     '../../metric_results/DATANTECH2035/video/play_video_count_daily.csv',
    #     {
    #         'date': datetime,
    #         'count': int
    #     }))

    print(get_single_value_from_csv('../../metric_results/DATANTECH2035/common/students_count.csv'))
