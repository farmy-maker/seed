#!/usr/bin/python
import argparse
from picamera import PiCamera
from datetime import datetime
from io import BytesIO


DEFAULT_PICTURE_PATH = "/tmp/"

try:
    pi_camera = PiCamera()
    pi_camera.start_preview()
    print('pi camera Init.')
except:
    pi_camera = None


def take_picture_pi():
    file_stream = BytesIO()
    pi_camera.capture(file_stream, 'jpeg')
    return file_stream.getvalue()


if __name__ == "__main__":
    raw = take_picture_pi()
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    with open(DEFAULT_PICTURE_PATH + file_name, 'wb') as f:
        f.write(raw)
    print('Take Picture by Pi Camera. Save to {}'.format(DEFAULT_PICTURE_PATH))
