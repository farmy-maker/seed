from device import device
from datetime import datetime
import json


if __name__ == "__main__":
    data = device.fetch_data()
    print(json.dumps(data, indent=True))

    image = device.fetch_image()
    if image:
        file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        with open('/tmp/' + file_name, 'wb') as image_file:
            image_file.write(image)
            print('image saved at /tmp/' + file_name)
    else:
        print("image fetch fail.")

    print('flash pump')
    device.pump_controller.turn_on()
    print("flash led")
    device.led_controller.flash()

