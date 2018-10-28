# coding: utf-8
from device.controller import Controller

PUMP_PIN = 24  # pin of pump


if __name__ == "__main__":
    controller = Controller(PUMP_PIN)
    controller.run(50, 1)
    print("Pump Start for a second with 50% power")
