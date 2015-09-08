#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pierre Haessig — September 2015
""" Interface to communicate with a COZIR CO2 sensor
(cf. manufacturer website http://www.gassensing.co.uk/product/cozir-ambient/)

communication is based on USB-TTL cable which connects the sensor to the computer
"""

from __future__ import division, print_function
import serial
from enum import Enum

# Verbosity level (0,1,2)
verbosity = 1

class OpModes(Enum):
    '''Operating Modes of the COZIR sensor'''
    command = 0
    streaming = 1
    polling = 2


class Cozir(object):
    '''a COZIR CO2 sensor, connected through a USB-TTL cable to a virtual serial port
    
    All read operations are blocking (serial port read operations)
    '''

    def __init__(self, port):
        '''sensor, connected to serial port `port`
        
        Example:
        
        >>> c = Cozir('/dev/ttyUSB0')
        >>> print('CO2: {} ppm'.format(c.read_CO2()))
        CO2: 1201.0 ppm
        '''
        self.ser = serial.Serial(port, timeout=1)
        if verbosity >= 1:
            print('connected to "{}"'.format(port))
        
        # Set operating mode to polling
        self.set_mode(OpModes.polling)
    
    def __repr__(self):
        return "Cozir('{}')".format(self.ser.port)
    
    def write(self, com):
        '''write the command `com` followed by "\\r\\n"'''
        if verbosity >= 2:
            print('writing "{}"'.format(com))
        self.ser.write(com + '\r\n')
    
    ### Data Polling commands
    def read_CO2(self, with_filter=True):
        '''CO2 concentration in ppm
        
        with or without the digital smoothing filter
        
        note: the multiplier is *not implemented*.
        
        (Z or z command)
        '''
        if with_filter:
            com = b'Z'
        else:
            com = b'z'
        self.write(com)
        
        res = self.ser.readline().strip()
        assert res.startswith(com + b' ')
        res = float(res[2:])
        
        return res

    def read_temperature(self):
        '''temperature in degrees Celsius
        
        (T command)
        '''
        self.write('T')
        res = self.ser.readline().strip()
        assert res.startswith('T ')
        res = (float(res[2:]) - 1000)/10.
        return res
    
    def read_humidity(self):
        '''relative humidity in %
        
        (H command)
        '''
        self.write('H')
        res = self.ser.readline().strip()
        assert res.startswith('H ')
        res = float(res[2:])/10.
        return res
    
    ### Operating mode functions
    def set_mode(self, mode):
        '''set operating mode: command, streaming or polling (using OpModes enum)'''
        assert isinstance(mode, OpModes)
        if verbosity >= 1:
            print('set operating mode to "{}"'.format(mode.name))
        self.write('K {:d}'.format(mode.value))
        
        # Read the response
        res = self.ser.readline().strip()
        assert res == b'K {:05d}'.format(mode.value)
        
        self._mode = mode
    
    def get_mode(self):
        '''return *cached* value of operating mode'''
        return self._mode
    
    ### Information commands
    def read_firmware(self):
        '''firmware version and sensor serial number
        
        (Y command)
        
        Returns a tuple of strings like
        ('Oct 18 2013,14:02:10,AL19', '124584 00000')
        '''
        self.write('Y')
        res = self.ser.readline()
        res += self.ser.readline()
        res = res.strip()
        assert res.startswith('Y,')
        res = res[2:]
        
        # split firmware and seria number
        fw, sn = res.splitlines()
        
        assert sn.startswith(' B ')
        sn = sn[3:]
        
        return fw, sn
    
    def read_info(self):
        '''Information about the sensor configuration and behavior.
        
        returns lots of fields
        
        (* command)
        '''
        self.write('*')
        res = ''
        l = self.ser.readline()
        while l:
            res += l
            l = self.ser.readline()
        
        assert res.startswith(' * ')
        res = res[3:].strip()
        return res
    
    def read_CO2_multiplier(self):
        '''number indicating what multiplier must be applied to the CO2 reads
        to get a value in ppm
        
        (. command)
        '''
        self.write('.')
        
        res = self.ser.readline().strip()
        assert res.startswith('. ')
        res = float(res[2:])
        
        return res
    
    ### Customization commands
    def read_filter(self):
        '''read the setting of the digital filter for the CO2 measurement'''
        self.write('a')
        res = self.ser.readline().strip()
        assert res.startswith('a ')
        res = int(res[2:])
        return res
    
    def set_filter(self, val):
        '''set the setting of the digital filter to `val`, between 0 and 65535'''
        val = int(val)
        assert 0 <= val <= (2**16-1)
        self.write('A {:d}'.format(val))
        if verbosity >= 1:
            print('set filter to {:d}'.format(val))
        # Read the response
        res = self.ser.readline().strip()
        assert res.startswith('A ')
    
    ### Calibration commands
    def read_autocal(self):
        '''read the autocalibration settings of the CO2 measurement
        
        Returns the tuple (is_active, ini_interv, reg_interv)
        '''
        self.write('@')
        
        res = self.ser.readline().strip()
        assert res.startswith('@ ')
        res = res[2:]
        
        if res == '0':
            # autocalibration is disabled
            is_active = False
            ini_interv = None
            reg_interv = None
        
        else:
            is_active = True
            ini_interv, reg_interv = res.split(' ')
            ini_interv = float(ini_interv)
            reg_interv = float(reg_interv)
        
        return is_active, ini_interv, reg_interv
    
    def set_autocal(self, is_active, ini_interv=1.0, reg_interv=8.0):
        '''set the autocalibration settings of the CO2 measurement
        
        is_active: bool
        ini_interv: float, initial autocalibration interval in days
        reg_interv: float, regular autocalibration interval in day
        '''
        if not is_active:
            self.write('@ 0')
            
            # Read the response
            res = self.ser.readline().strip()
            assert res == '@ 0'
        else:
            ini_interv = float(ini_interv)
            reg_interv = float(reg_interv)
            self.write('@ {:.1f} {:.1f}'.format(ini_interv, reg_interv))
            
            # Read the response
            res = self.ser.readline().strip()
            assert res.startswith('@ ')

        
if __name__ == '__main__':
    c = Cozir('/dev/ttyUSB0')
    
    print('CO2: {} ppm'.format(c.read_CO2()))
    print('Temp: {} °C'.format(c.read_temperature()))
    print('Humid: {} %'.format(c.read_humidity()))
