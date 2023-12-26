===================
LED controller test
===================

Imagine an LED controller that has multiple functions. One of them is turning the LEDs on and off.
The controller serves the http API to control the LEDs (it is simulated by the led_controller.py script).

Requests to control:

- GET *http://127.0.0.1:8000/led-controller?status=on* - turns on LEDs
- GET *http://127.0.0.1:8000/led-controller?status=off* - turns off LEDs
- GET *http://127.0.0.1:8000/led-controller* - reads status of LEDs

We have to test it!


Usage
=====

Install dependencies:

`$ pip install -r requirements.txt`

Run controller server:

`$ uvicorn led_controller:app --reload`

Run test:

`robot -L TRACE -d logs test.robot`
