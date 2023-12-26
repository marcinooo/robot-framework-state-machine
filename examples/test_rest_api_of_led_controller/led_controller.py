"""
REST API to simulate fake led controller.

Run command:
$ uvicorn led_controller:app --reload

"""

from typing import Union
from fastapi import FastAPI


class LEDController:

    def __init__(self):
        self.status = 'off'

    def on(self):
        self.status = 'on'
        return self.status

    def off(self):
        self.status = 'off'
        return self.status


app = FastAPI()
led_controller = LEDController()


@app.get('/led-controller')
def read_controller(status: Union[str, None] = None):

    if status is None:
        response = {'status': led_controller.status}
    elif status == 'on':
        response = {'status': led_controller.on()}
    elif status == 'off':
        response = {'status': led_controller.off()}
    else:
        response = {'error': 'status reading error'}

    return response
