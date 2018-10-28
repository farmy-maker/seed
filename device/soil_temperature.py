# -*- coding: utf-8 -*-
import time
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()


def get_celsius():
    return round(sensor.get_temperature(), 2)


if __name__ == "__main__":
    while True:
        temperature = get_celsius()
        print("Celsius: {0:.3f}".format(temperature))
        time.sleep(3)
