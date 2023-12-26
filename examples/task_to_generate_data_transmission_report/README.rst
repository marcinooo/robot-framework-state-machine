==================================
Data transmission report generator
==================================

There is a test line to test the temperature of the phone chipset depending on the transmitted data level.

We have two files:

- *data_transmission_test_line.json* which contains information about test line
- *data_transmission.csv* which contains temperature and throughput level outputs from test

We have to build report which combines data from above files!


Usage
=====

Install dependencies:

`$ pip install -r requirements.txt`

Run task:

`robot -L TRACE -d logs task.robot`
