# coding: utf-8
from models.base import session
from datetime import datetime, timedelta
from models.enums import PlantGrowthFactor
from models.device import Device, DeviceChannel, DeviceController, PlantControllerType, ChannelData
from models.plant import Plant, PlantFactor, PlantSnapshot
import random


def init_all(session):
    # TODO: init from json or csv file
    plant = Plant(name=u"Plant")
    session.add(plant)
    device = Device(name="Raspberry Pi")
    session.add(device)
    session.commit()
    for factor in PlantGrowthFactor:
        channel = DeviceChannel(device_id=device.id)
        session.add(channel)
        session.commit()
        plant_factor = PlantFactor(plant_id=plant.id,
                                   factor_type=factor,
                                   channel_id=channel.id)
        session.add(plant_factor)
        session.commit()
    pump_controller = DeviceController(device_id=device.id, controller_type=PlantControllerType.PUMP)
    session.add(pump_controller)
    led_controller = DeviceController(device_id=device.id, controller_type=PlantControllerType.LED)
    session.add(led_controller)
    session.commit()


def generate_fake_data(session):
    channels = session.query(DeviceChannel).all()
    for channel in channels:
        for i in range(30):
            recorded_at = datetime.now() - timedelta(minutes=random.randint(1, 60*24))
            c_data = ChannelData(channel_id=channel.id, value=random.randint(0, 700), recorded_at=recorded_at)
            session.add(c_data)

    plant = session.query(Plant).first()
    for i in range(20):
        plant_snap = PlantSnapshot(plant_id=plant.id,
                                   created_at=datetime(2018, 10, 16, random.randint(0, 23), random.choice([0, 30])))
        session.add(plant_snap)
    session.commit()


if __name__ == "__main__":
    init_all(session)
    # generate_fake_data(session)
