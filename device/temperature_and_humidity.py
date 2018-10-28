import time
import RPi.GPIO as GPIO
from dht11 import DHT11

DHT_PIN = 14

GPIO.cleanup()


def _get_temperature_and_humidity(pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    instance = DHT11(pin=pin)
    result = instance.read()
    if result.is_valid():
        return result


def get_temperature_and_humidity(pin):
    for retry in range(100):
        time.sleep(0.05)
        result = _get_temperature_and_humidity(pin)
        if result:
            return round(result.temperature, 2), round(result.humidity, 2)
    return None, None


if __name__ == "__main__":
    while True:
        temperature, humidity = get_temperature_and_humidity(DHT_PIN)
        if temperature:
            print("Temperature: {}C".format(temperature))
            print("Humidity: {}%".format(humidity))
            time.sleep(3)
