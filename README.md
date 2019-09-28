# bierwiegen
Bierwiegen mit einem raspberry-pi


## ADC

Wir nutzen einen hx711 24-bit ADC:
https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf

## Setup on a pi

```
$ sudo apt install python3 python3-pyqt5 python3-numpy python3-rpi.gpio python3-pyyaml
$ git clone https://github.com/pep-dortmund/bierwiegen
$ cd bierwiegen
$ pip install -e .
```

Add the following lines to `~/.config/lxsession/LXDE-pi/autostart`.
The first 3 will deactivate the screensaver, the other autostart the program.
```
@xset s noblank
@xset s off
@xset -dpms
@/home/pi/.local/bin/bierwiegen
```
