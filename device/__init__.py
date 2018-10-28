from datetime import datetime
import random
from config import CAMERA_TYPE, DHT_PIN, PUMP_PIN, LED_PIN, DEBUG, CAMERA_LIGHT_THRESHOLD
try:
    from device.light import read_light
    from device.soil_moisture import get_moisture
    from device.soil_temperature import get_celsius
    from device.temperature_and_humidity import get_temperature_and_humidity
    from device.controller import Controller
except Exception as e:
    print('Warning. {}'.format(str(e)))


from threading import Lock
thread_lock = Lock()


class Device:

    def __init__(self, camera_type, dht_pin, pump_pin, led_pin, debug=False):
        self.camera_type = camera_type
        self.dht_pin = dht_pin
        self.pump_pin = pump_pin
        self.led_pin = led_pin
        self.debug = debug
        self.camera_ok = self.check_camera()
        print("Farmy device init.")

    @property
    def pump_controller(self):
        return Controller(self.pump_pin)

    @property
    def led_controller(self):
        return Controller(self.led_pin)

    def fetch_data(self):
        data = dict(
            light=0,
            soil_moisture=0,
            soil_temperature=0,
            temperature=0,
            humidity=0,
        )
        if self.debug:
            data.update(dict(
                light=random.randint(0, 100),
                soil_moisture=random.randint(0, 100),
                soil_temperature=random.randint(0, 100),
                temperature=random.randint(0, 100),
                humidity=random.randint(0, 100)
            ))
        else:
            global thread
            with thread_lock:
                data.update(dict(
                    light=read_light(),
                    soil_moisture=get_moisture(),
                    soil_temperature=get_celsius(),
                ))
                temperature, humidity = get_temperature_and_humidity(self.dht_pin)
                if temperature is not None:
                    data.update(dict(
                        temperature=temperature,
                        humidity=humidity
                    ))
                now = datetime.now()
                data.update(dict(
                    ts=int((now - datetime.fromtimestamp(0)).total_seconds()),
                    dt=now.strftime("%Y/%m/%d %H:%M:%S"),
                ))
        return data

    def fetch_image(self):
        with thread_lock:
            if not self.debug and self.camera_ok:
                light = read_light()
                if light <= CAMERA_LIGHT_THRESHOLD:
                    print('Too dark to take photo.')
                    return
                if self.camera_type == 'web':
                    from device.camera.webcam import take_picture_web
                    image_raw = take_picture_web()
                elif self.camera_type == 'pi':
                    from device.camera.pi import take_picture_pi
                    image_raw = take_picture_pi()
                else:
                    raise ValueError("camera_type `{}` invalid".format(self.camera_type))
                return image_raw
            elif self.debug:
                print('debug mode. no image fetched.')
            elif not self.camera_ok:
                print('camera is not ready.')

    def check_camera(self):
        if self.debug:
            return False
        elif self.camera_type == "web":
            from device.camera.webcam import web_camera
            if web_camera is None:
                print("web camera not found.")
                return False
        elif self.camera_type == "pi":
            from device.camera.pi import pi_camera
            if pi_camera is None:
                print("Pi Camera not found.")
                return False
        else:
            print("camera_type `{}` invalid".format(self.camera_type))
            return False
        return True


device = Device(
    camera_type=CAMERA_TYPE,
    dht_pin=DHT_PIN,
    pump_pin=PUMP_PIN,
    led_pin=LED_PIN,
    debug=DEBUG,
)
