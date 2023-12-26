"""Module contains builder of data transmission report."""

import csv
import json
from typing import Union
from collections.abc import MutableMapping
from datetime import datetime
from jinja2 import Environment


def flatten_dictionary(mapping: MutableMapping, parent_key: Union[str, None] = None) -> dict:
    """Removes nested dictionaries by flattening them. E.g.: {'a': 1, 'b': {'c': 2}}  ->  {'a': 1, 'b/c': 2}"""

    new_mapping = {}

    for key, value in mapping.items():

        new_key = f'{parent_key}/{key}' if parent_key is not None else key

        if isinstance(value, dict):
            nested_mapping = flatten_dictionary(value, new_key)
            new_mapping.update(nested_mapping)
        else:
            new_mapping[new_key] = value

    return new_mapping


class HTMLReportBuilder:
    """Prepares html report based on source data files."""

    def __init__(self, template_path: str) -> None:
        self.template_path = template_path

        self._render_artifacts = {
            'report_generated_on': str(datetime.now())
        }

    def get_test_line_data(self, test_line_log_path: str) -> 'HTMLReportBuilder':
        """Gets test line information and place it HTML table."""

        with open(test_line_log_path, 'r') as fh:
            data = json.load(fh)

        data = flatten_dictionary(data)

        test_line_info = (
            f'<table>\n'
            f'<tr>{"".join(f"<th>{key}</th>" for key in data.keys())}</tr>\n'
            f'<tr>{"".join(f"<td>{value}</td>" for value in data.values())}</tr>\n'
            f'</table>\n'
        )

        self._render_artifacts.update({'test_line_info': test_line_info})

        return self

    def get_chart_data(self, chart_log_path: str) -> 'HTMLReportBuilder':
        """Gets csv throughput data and placed it in JavaScript arrays."""

        timestamp_values = []
        throughput_values = []
        temperature_values = []

        with open(chart_log_path, 'r') as fh:
            reader = csv.DictReader(fh)

            for row in reader:
                timestamp_values.append(row['timestamp'])
                throughput_values.append(float(row['throughput']))
                temperature_values.append(float(row['temperature']))

        self._render_artifacts.update({
            'data_collected_on': timestamp_values[0],
            'timestampValues': str([timestamp.split(' ')[1] for timestamp in timestamp_values]),
            'throughputValues': str(throughput_values),
            'temperatureValues': str(temperature_values)
        })

        return self

    def build(self, report_path: str) -> None:
        """Builds final report by dumping all collected information to output file."""

        with open(self.template_path, 'r') as source_fh, open(report_path, 'w') as destination_fh:
            environment = Environment()
            template = environment.from_string(source_fh.read())
            report = template.render(**self._render_artifacts)

            destination_fh.write(report)


if __name__ == '__main__':
    report_builder = HTMLReportBuilder('./report.template.html')
    report_builder.get_test_line_data('./data_transmission_test_line.json')
    report_builder.get_chart_data('./data_transmission.csv')
    report_builder.build('./report.html')
