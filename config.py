try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()
config.read('./config.ini')
CAMERA_TYPE = config.get('device', 'camera_type')
CAMERA_LIGHT_THRESHOLD = config.getint('device', 'camera_light_threshold')
DHT_PIN = config.getint('device', 'dht_pin')
PUMP_PIN = config.getint('device', 'pump_pin')
LED_PIN = config.getint('device', 'led_pin')
IMAGE_PATH = config.get('sys', 'image_path')
MODE = config.get('sys', 'mode')
DEBUG = MODE == 'debug'

FETCH_DATA_INTERVAL = config.getint('sys', 'fetch_data_interval')
FETCH_IMAGE_INTERVAL = config.getint('sys', 'fetch_image_interval')
TRIGGER_INTERVAL = config.getint('sys', 'trigger_interval')

CHART_INTERVAL = config.getint('sys', 'chart_interval')
CHART_BEFORE = config.getint('sys', 'chart_before')

USER = config.get('auth', 'user')
PASS = config.get('auth', 'pass')
