#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pierre Haessig — September 2015
""" Log data from the COZIR CO2 sensor in a CSV file

TODO:
* automatic selection of logfile name
* changeable logging interval
"""

from __future__ import division, print_function, unicode_literals

import time
from datetime import datetime

from cozir import Cozir


log_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_fname = 'cozir_log_{}.csv'.format(log_time)
sleep_duration = 30 # s

c = Cozir('/dev/ttyUSB0')

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
