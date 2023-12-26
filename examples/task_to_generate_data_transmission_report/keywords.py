import os
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from StateMachineLibrary import StateMachineLibrary

from report_builder import HTMLReportBuilder


_sml = StateMachineLibrary()


@keyword
def task_setup():
    """Initializes state machine."""

    _sml.create_state_machine('data-transmission-report-machine')

    _sml.add_state('Parse test line info log', 'On update parse test line info log')
    _sml.add_state('Parse data transmission log', 'On update parse data transmission log')
    _sml.add_state('Build report', 'On update build report')

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    report_builder = HTMLReportBuilder(os.path.join(cur_dir, 'report.template.html'))

    _sml.update_context(report_builder=report_builder)


@keyword
def parse_test_line_info_log():
    """Parses test line info file."""

    data_transmission_test_line_log_path = BuiltIn().get_variable_value('${data_transmission_test_line_log_path}')
    report_builder = _sml.get_context()['report_builder']

    report_builder.get_test_line_data(data_transmission_test_line_log_path)


@keyword
def on_update_parse_test_line_info_log():
    """Navigates to next state."""

    _sml.go_to_state('Parse data transmission log')


@keyword
def parse_data_transmission_log():
    """Parses file with charts data."""

    data_transmission_log_path = BuiltIn().get_variable_value('${data_transmission_log_path}')
    report_builder = _sml.get_context()['report_builder']

    report_builder.get_chart_data(data_transmission_log_path)


@keyword
def on_update_parse_data_transmission_log():
    """Navigates to next state."""

    _sml.go_to_state('Build Report')


@keyword
def build_report():
    """Builds finale report."""

    final_report_path = BuiltIn().get_variable_value('${final_report_path}')
    report_builder = _sml.get_context()['report_builder']

    report_builder.build(final_report_path)

    logger.console(f'Report: {final_report_path}')


@keyword
def on_update_build_report():
    """Stops state machine."""

    _sml.stop_state_machine()
