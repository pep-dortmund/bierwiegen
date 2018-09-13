'''
Code to read data from a hx711 scale.
'''
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import numpy as np


class HX711:
    
    N_GAIN_BITS = {128: 1, 64: 27, 32: 2}

    def __init__(self, dout, pd_sck, scale, gain=128):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.power_down()
        self.power_up()

        self.gain = gain
        self.scale = scale
        self.zero = 0

    def is_ready(self):
        # When output data is not ready for retrieval,
        # digital output pin DOUT is high (p. 4)
        return GPIO.input(self.DOUT) == 0

    def tare(self, n=10):
        self.zero = self.read_median(n=n)

    def set_scale(self, reference, n=10):
        self.scale = reference / (self.read_median(n=n) - self.zero)

    def read_median(self, n):
        return np.median([self.read_raw() for i in range(n)])

    def read(self, n=10):
        vals = self.read_median(n=n)
        return (vals - self.zero) * self.scale

    def read_raw(self):
        GPIO.output(self.PD_SCK, False)

        while not self.is_ready():
            time.sleep(0.001)

        n = 0
        for i in range(24):
            GPIO.output(self.PD_SCK, True)
            bit = GPIO.input(self.DOUT)
            GPIO.output(self.PD_SCK, False)

            if bit:
                n += 1 << (24 - i)

        for _ in range(self.N_GAIN_BITS[self.gain]):
            self.clock_pulse()
        
        return n

    def clock_pulse(self):
        GPIO.output(self.PD_SCK, True) 
        time.sleep(0.01)
        GPIO.output(self.PD_SCK, False) 

    @property 
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, gain):
        assert gain in (64, 128), 'Scale only supports gains of 64, 128'

        self._gain = gain
        GPIO.output(self.PD_SCK, False)
        self.read_raw()
    
    def power_down(self):
        GPIO.output(self.PD_SCK, True)
        time.sleep(0.01)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)

    def reset(self):
        self.power_down()
        self.power_up()
        self.read_raw()  # one read to get the correct gain setting 

