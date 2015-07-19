#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: John Gill
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)
from __future__ import print_function

import datetime
import argparse
import csv
import time
import sys

import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT as DHT

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = BMP085.BMP085()
dht_sensor = DHT.DHT22
# Optionally you can override the bus number:
#sensor = BMP085.BMP085(busnum=2)

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER, 
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--csv', default=False,
                    action='store_true',
                    help="create comma separated value output")
parser.add_argument('--header', default=False, action='store_true',
                    help="include header in csv output")
parser.add_argument('--pin', type=int, default=4)
parser.add_argument('-s', '--sleep', default=60.0, type=float,
                    help="Time to sleep between samples")

opts = parser.parse_args()

outfile = sys.stdout

if opts.csv:

    if opts.header:
        print("date,temp,pressure,altitude,sealevel_pressure,humidity,temp_dht",
              file=outfile)
    writer = csv.writer(outfile)


while True:

    humidity, temperature = DHT.read_retry(dht_sensor, opts.pin)
    
    if opts.csv:
        writer.writerow([
            datetime.datetime.now(),
            sensor.read_temperature(),
            sensor.read_pressure(),
            sensor.read_altitude(),
            sensor.read_sealevel_pressure(),
            humidity, temperature
            ])

        outfile.flush()
    
    else:
        print('Datetime = {}'.format(datetime.datetime.now()))
        print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
        print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
        print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
        print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
        print()
	print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

    time.sleep(opts.sleep)
