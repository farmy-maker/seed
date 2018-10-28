# coding: utf-8
from device.controller import Controller

LED_PIN = 23  # pin of led


if __name__ == "__main__":
    controller = Controller(LED_PIN)
    controller.run(50, 1)
    print("Led Start for a second with 50% power")
