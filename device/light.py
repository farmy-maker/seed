#!/usr/bin/python
from smbus2 import SMBus
import time

DEVICE = 0x23
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07

ONE_TIME_HIGH_RES_MODE_1 = 0x20

bus = SMBus(1)


def convert_to_number(data):
    return round((data[1] + (256 * data[0])) / 1.2, 2)


def read_light(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1, 16)
    return convert_to_number(data)


if __name__ == "__main__":
    while True:
        print("Light Level: " + str(read_light()) + " lux")
        time.sleep(3)
