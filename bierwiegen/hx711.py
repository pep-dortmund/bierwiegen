'''
Code to read data from a hx711 scale.
'''
from __future__ import print_function
import RPi.GPIO as GPIO
from time import sleep
import numpy as np


class HX711:
    '''
    A HX711 scale

    Attributes
    ----------
    dout: int
        the dout pin
    pd_sck: int
        the pd_sck pin
    scale: float
        conversion factor between adc bits and grams
    gain: int
        the gain to use, (128 or 64)
    '''
    
    # total pulses to select gain
    N_GAIN_BITS = {128: 1, 64: 3}

    def __init__(self, dout, pd_sck, scale, gain=128):
        self.pd_sck = pd_sck
        self.dout = dout

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pd_sck, GPIO.OUT)
        GPIO.setup(self.dout, GPIO.IN)
        GPIO.output(self.pd_sck, False)

        self.power_down()
        self.power_up()

        self.gain = gain
        self.scale = scale
        self.zero = 0

    def is_ready(self):
        # When output data is not ready for retrieval,
        # digital output pin dout is high (p. 4)
        return GPIO.input(self.dout) == 0

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
        GPIO.output(self.pd_sck, False)

        while not self.is_ready():
            sleep(1e-6)

        n = sum(self.read_bit() << (24 - i) for i in range(24))

        for _ in range(self.N_GAIN_BITS[self.gain]):
            self.clock_pulse()

        # out of range markers
        if n == 0x800000:
            return -np.inf
        elif n == 0x7fffff:
            return np.inf
        
        return n

    def read_bit(self):
        GPIO.output(self.pd_sck, True)
        bit = GPIO.input(self.dout)
        GPIO.output(self.pd_sck, False)

        return bit

    def clock_pulse(self):
        GPIO.output(self.pd_sck, True) 
        sleep(10e-6)
        GPIO.output(self.pd_sck, False) 

    @property 
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, gain):
        assert gain in (64, 128), 'Scale only supports gains of 64, 128'

        self._gain = gain
        GPIO.output(self.pd_sck, False)
        self.read_raw()
    
    def power_down(self):
        GPIO.output(self.pd_sck, True)
        sleep(0.01)

    def power_up(self):
        GPIO.output(self.pd_sck, False)

    def reset(self):
        self.power_down()
        self.power_up()
        self.read_raw()  # one read to get the correct gain setting 

