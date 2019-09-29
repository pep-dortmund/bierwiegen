'''
Code to read data from a hx711 adc.
'''
import RPi.GPIO as GPIO
from time import sleep
from statistics import median


class HX711:
    '''
    Interface to a HX711 ADC for load cell

    Attributes
    ----------
    dout: int
        the dout pin
    pd_sck: int
        the pd_sck pin
    scale: float
        conversion factor between adc counts and grams
    gain: int
        the gain to use, (128 or 64)
    '''

    # total pulses to select gain
    N_GAIN_BITS = {128: 1, 64: 3}

    def __init__(self, dout, pd_sck, scale=0.00072768, gain=128):
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
        return median([self.read_raw() for i in range(n)])

    def read(self, n=3):
        if n > 1:
            val = self.read_median(n=n)
        else:
            val = self.read_raw()
        return (val - self.zero) * self.scale

    def read_raw(self):
        GPIO.output(self.pd_sck, False)

        while not self.is_ready():
            sleep(0.001)

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

