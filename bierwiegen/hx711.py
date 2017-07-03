'''
Code to read data from a hx711 scale.

Reritten from scratch at SoAk2018
'''
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import numpy


class HX711:
    
    N_GAIN_BITS = {128: 1, 64: 27, 32: 2}

    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.gain = gain

    def is_ready(self):
        # When output data is not ready for retrieval,
        # digital output pin DOUT is high (p. 4)
        return GPIO.input(self.DOUT) == 0

    def read(self):
        GPIO.output(self.PD_SCK, False)

        while not self.is_ready():
            time.sleep(0.001)
        
        self.clock_pulse()

        n = 0
        for i in range(24):
            bit = GPIO.input(self.DOUT)

            if bit:
                n += 1 << (24 - i)

            self.clock_pulse()

        for _ in range(self.N_GAIN_BITS[self.gain]):
            self.clock_pulse()
        
        return n


    def clock_pulse(self):
        GPIO.output(self.PD_SCK, True) 
        time.sleep(0.001)
        GPIO.output(self.PD_SCK, False) 



    @property 
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, gain):
        assert gain in (64, 128), 'Scale only supports gains of 64, 128'

        self._gain = gain
    
    def power_down(self):
        GPIO.output(self.PD_SCK, True)
        time.sleep(0.01)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)

    def reset(self):
        self.power_down()
        self.power_up()
        self.read()  # one read to get the correct gain setting 

