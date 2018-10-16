from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base, engine
from .enums import PlantControllerType
from datetime import datetime, timedelta
from itertools import groupby


class Device(Base):

    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(Text, nullable=True)
    url = Column(String(128), nullable=True)
    channels = relationship("DeviceChannel", order_by='DeviceChannel.id', back_populates="device")
    controllers = relationship("DeviceController", order_by='DeviceController.id', back_populates="device")

    def __str__(self):
        return self.name

    @property
    def triggered_actions(self):
        triggers = []
        for c in self.channels.all():
            triggers.extend([t for t in c.triggers.all() if t.is_triggered])
        return [{'action_type': t.action_type, 'num': t.controller.num} for t in triggers]


class DeviceController(Base):

    __tablename__ = 'device_controllers'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    control_type = Column(Enum(PlantControllerType))

    device = relationship("Device", back_populates="controllers")
    triggers = relationship("PlantFactorTrigger", order_by='PlantFactorTrigger.id', back_populates="controller")

    def __str__(self):
        return "{}:controller:{}".format(self.device.name, self.id)


class DeviceChannel(Base):

    __tablename__ = 'device_channels'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))

    device = relationship("Device", back_populates="channels")
    plant_factor = relationship("PlantFactor", uselist=False, back_populates="channel")

    datum = relationship("ChannelData", lazy='dynamic', back_populates="channel")

    def __str__(self):
        return "{}:channel:{}".format(self.device.name, self.id)

    def get_datum_before_minutes(self, minutes):
        return self.datum.order_by(ChannelData.recorded_at).\
            filter(ChannelData.recorded_at >= (datetime.now() - timedelta(minutes=minutes)))

    def get_avg_datum_before_minutes(self, minutes, base=30):
        recent_datum = self.get_datum_before_minutes(minutes)
        return ChannelData.get_avg_datum_group_by_minute(recent_datum, base=base)

    def get_avg_datum_in_one_day(self):
        return self.get_avg_datum_before_minutes(60*24, base=30)

    def get_labels_for_display(self):
        datum = self.get_avg_datum_in_one_day()
        return [d.strftime("%d/%H:%M") for d in datum.keys()]

    def get_datum_for_display(self):
        datum = self.get_avg_datum_in_one_day()
        return list(datum.values())

    @property
    def latest_value(self):
        recent_data = self.datum.order_by(ChannelData.recorded_at.desc()).first()
        return recent_data

    @property
    def triggered_actions(self):
        return [t for t in self.triggers.all() if t.is_triggered]


class ChannelData(Base):

    __tablename__ = 'channel_data'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('device_channels.id'))
    value = Column(Float)
    recorded_at = Column(DateTime, index=True, default=datetime.utcnow)

    channel = relationship("DeviceChannel", back_populates="datum")

    def __str__(self):
        return "channel:{}:data:{}".format(self.channel_id, self.recorded_at)

    @property
    def recorded_passed(self):
        now = datetime.now()
        diff_min = (now - self.recorded_at).total_seconds() // 60
        if diff_min < 60:
            return "{} 分前".format(int(diff_min))
        elif diff_min < 60 * 24:
            return "{} 時間前".format(int(diff_min // 60))
        else:
            return "{} 日前".format(int(diff_min // (60 * 24)))

    @staticmethod
    def get_avg_datum_group_by_minute(datum, base=30):
        grouped_datum = groupby(datum,
                                lambda data: data.recorded_at.replace(minute=base * (data.recorded_at.minute // base),
                                                                      second=0, microsecond=0))

        def mean(datum_iter):
            numbers = [d.value for d in datum_iter]
            return round(float(sum(numbers)) / max(len(numbers), 1), 2)
        return {dt: mean(datum_iter) for dt, datum_iter in grouped_datum}

Base.metadata.create_all(engine)
