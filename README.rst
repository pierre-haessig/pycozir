Python interface to COZIR CO2 sensors
-------------------------------------

Pierre Haessig, september 2015

This module wraps the communication on a serial port with a COZIR CO2 sensor.
It gives a higher level API than the serial communication protocol.

Functionalities:

* reading data (CO2, temperature and humidity)
* configure the sensor (digital filter, calibration, ...)


Usage
-----

Create a connection to a sensor connected to serial port '/dev/ttyUSB0'::

    >>> from cozir import Cozir
    >>> c = Cozir('/dev/ttyUSB0')
    connected to "/dev/ttyUSB0"
    set operating mode to "polling"

Read data from sensors::

    >>> print('CO2: {} ppm'.format(c.read_CO2()))
    CO2: 1189.0 ppm
    >>> print('Temp: {} °C'.format(c.read_temperature()))
    Temp: 27.3 °C
    >>> print('Humid: {} %'.format(c.read_humidity()))
    Humid: 39.3 %

note: temperature and humidity sensors are an optional add-on in COZIR sensors.


About the COZIR CO2 sensor
--------------------------

More information on the manufacturer website:
http://www.gassensing.co.uk/product/cozir-ambient/


