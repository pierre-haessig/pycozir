#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pierre Haessig — September 2015
""" Log data from a COZIR CO2 sensor in a CSV file
"""

from __future__ import division, print_function, unicode_literals

import time
from datetime import datetime
import argparse
from cozir import Cozir


### Command line interface

def log_time(string):
    'check the --time argument'
    val = float(string)
    if val < 1:
        msg = 'logging interval should be greater than 1 s'
        raise argparse.ArgumentTypeError(msg)
    return val

parser = argparse.ArgumentParser(
    description='Log data from a COZIR sensor connected to port PORT in a CSV file')

parser.add_argument(
    '-o', '--output', metavar='FILENAME',
    help='output filename (datetime based if omitted)')
parser.add_argument(
    '-t', '--time', metavar='INTERVAL',
    default=30, type=log_time,
    help='logging time interval (in seconds), default is 30 s',
    )
parser.add_argument(
    'port',
    help="name or number of the serial port on which the sensor is connected. Examples: '/dev/ttyUSB0' or 'COM3'")
args = parser.parse_args()


log_fname = args.output
if log_fname is None:
    log_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_fname = 'cozir_log_{}.csv'.format(log_time)

sleep_duration = args.time # s


### Open the sensor
port =  args.port
# TODO: add a try/except for port opening errors
c = Cozir(port)

with open(log_fname, 'w') as log:
    print('logging to "{}"'.format(log_fname))
    print('logging interval: {} s'.format(sleep_duration))
    log.write('datetime,CO2,Temperature,Humidity\n')
    
    while True:
        co2 = c.read_CO2()
        temp = c.read_temperature()
        humid = c.read_humidity()
        
        t = datetime.now().isoformat()
        line = '{},{:.0f},{:.1f},{:.1f}'.format(t, co2, temp, humid)
        line_units = '{:.0f} ppm, {:.1f} °C, {:.1f} %'.format(co2, temp, humid)
        print(line_units)
        
        log.write(line+'\n')
        log.flush()
        time.sleep(sleep_duration)
