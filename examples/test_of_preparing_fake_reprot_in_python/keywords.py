from robot.api import logger
from StateMachineLibrary import StateMachineLibrary


_report = {}


def sm_name():
    return 'report-machine'


def state_machine(func):
    def inner(*args, **kwargs):
        sm = StateMachineLibrary()
        func(sm)
    return inner


@state_machine
def prepare_report_setup(sm):
    sm.create_state_machine(sm_name())
    sm.add_state(get_battery_voltage.__name__, on_update_get_battery_voltage.__name__, sm_name())
    sm.add_state(get_time_of_running.__name__, on_update_get_time_of_running.__name__, sm_name())
    sm.add_state(show_report.__name__, on_update_show_report.__name__, sm_name())


def get_battery_voltage():
    logger.console('Getting battery voltage...')

    def get_voltage():
        return '2.7'
    _report['battery_voltage'] = get_voltage()


@state_machine
def on_update_get_battery_voltage(sm):
    sm.go_to_state(get_time_of_running.__name__, sm_name())


def get_time_of_running():
    logger.console('Getting time of running...')

    def get_time():
        return '58932 ms'
    _report['time_of_running'] = get_time()


@state_machine
def on_update_get_time_of_running(sm):
    sm.go_to_state(show_report.__name__, sm_name())


def show_report():
    logger.console('Report: {}'.format(_report))


def on_update_show_report():
    pass
