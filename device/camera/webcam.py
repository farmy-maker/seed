#!/usr/bin/python
from SimpleCV import Camera
from datetime import datetime
from io import BytesIO

DEFAULT_PICTURE_PATH = "/tmp/"


try:
    web_camera = Camera()
    web_camera.getImage()
    print('webcam Init.')
except:
    web_camera = None


def take_picture_web():
    file_stream = BytesIO()
    img_raw = web_camera.getImage().getPIL()
    img_raw.save(file_stream, format='jpeg')
    return file_stream.getvalue()


if __name__ == "__main__":
    raw = take_picture_web()
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    with open(DEFAULT_PICTURE_PATH + file_name, 'wb') as f:
        f.write(raw)
    print('Take Picture by Webcam. Save to {}'.format(DEFAULT_PICTURE_PATH))
