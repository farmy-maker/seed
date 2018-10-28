from models.device import ChannelData
from models.plant import Plant, PlantSnapshot
from config import IMAGE_PATH, MODE
from datetime import datetime
import time
from flask_socketio import SocketIO
from threading import Lock
from device import device
thread = None
thread_lock = Lock()

socketio = SocketIO()


def get_data_socketio():
    plant = Plant.query.first()
    while True:
        time.sleep(2)
        data = device.fetch_data()
        socketio.emit('data', data)
        if MODE == 'demo':
            triggers = get_triggers(plant=plant)
            for t in triggers:
                if t.is_triggered_by_value(data[t.factor.factor_type]):
                    if t.controller.controller_type == 'led':
                        getattr(device.led_controller, t.action_type.value)()
                    elif t.controller.controller_type == 'pump':
                        getattr(device.pump_controller, t.action_type.value)()


@socketio.on('connect')
def on_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=get_data_socketio)


def fetch_and_save_data(session, plant):
    data = device.fetch_data()
    try:
        session.add(ChannelData(channel_id=plant.light_factor.channel.id, value=data['light']))
        session.add(ChannelData(channel_id=plant.soil_moisture_factor.channel.id, value=data['soil_moisture']))
        session.add(ChannelData(channel_id=plant.soil_temperature_factor.channel.id, value=data['soil_temperature']))
        session.add(ChannelData(channel_id=plant.temperature_factor.channel.id, value=data['temperature']))
        session.add(ChannelData(channel_id=plant.humidity_factor.channel.id, value=data['humidity']))
        session.commit()
    except:
        session.rollback()
        raise


def fetch_and_save_image(session, plant):
    image = device.fetch_image()
    if image:
        now = datetime.now()
        file_name = now.strftime("%Y%m%d%H%M%s") + ".jpg"
        with open(IMAGE_PATH + file_name, 'wb') as image_file:
            image_file.write(image)
        snapshot = PlantSnapshot(plant_id=plant.id, created_at=now)
        try:
            session.add(snapshot)
            session.commit()
        except:
            session.rollback()
            raise


def get_triggers(plant):
    triggers = plant.triggers.all()
    return triggers


def trigger_led(plant):
    triggers = get_triggers(plant)
    for t in triggers:
        if t.controller.controller_type == 'led' and t.is_triggered:
            getattr(device.led_controller, t.action_type.value)()


def trigger_pump(plant):
    triggers = get_triggers(plant)
    for t in triggers:
        if t.controller.controller_type == 'pump' and t.is_triggered:
            getattr(device.led_controller, t.action_type.value)()

