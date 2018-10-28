from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base, engine
from .enums import HardLevel, PlantStatus, FACTOR_NAME, RelationOperator, TriggerActionType, \
    PlantGrowthFactor
from datetime import datetime


class Plant(Base):

    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    seed_temperature = Column(String(64), nullable=True)
    water = Column(String(64), nullable=True)
    light_exposure = Column(String(32), nullable=True)
    temperature = Column(String(32), nullable=True)
    intro = Column(Text, nullable=True)
    hard_level = Column(Integer, default=HardLevel.NORMAL.value, nullable=True)
    wiki_link = Column(Text, nullable=True)
    image_path = Column(Text, nullable=True)
    status = Column(Enum(PlantStatus), default=PlantStatus.SOIL.value)

    factors = relationship("PlantFactor", lazy='dynamic', order_by='PlantFactor.id', back_populates="plant")
    triggers = relationship("PlantFactorTrigger", lazy='dynamic', order_by='PlantFactorTrigger.id', back_populates="plant")
    snapshots = relationship('PlantSnapshot', lazy='dynamic', order_by='PlantSnapshot.id.desc()', back_populates="plant")

    def __repr__(self):
        return "<{}>:{} {}".format(self.__class__.__name__, self.id, self.name)

    def __str__(self):
        return "{}".format(self.name)

    @property
    def image_path(self):
        return "images/plants/{}.jpg".format(self.id)

    @property
    def display_image_url(self):
        snapshot = self.snapshots.first()
        if snapshot:
            return snapshot.image_path
        else:
            return self.image_path or "images/default.png"

    @property
    def temperature_factor(self):
        return self.factors.filter(PlantFactor.factor_type == PlantGrowthFactor.TEMPERATURE).one()

    @property
    def humidity_factor(self):
        return self.factors.filter(PlantFactor.factor_type == PlantGrowthFactor.HUMIDITY).one()

    @property
    def light_factor(self):
        return self.factors.filter(PlantFactor.factor_type == PlantGrowthFactor.LIGHT).one()

    @property
    def soil_temperature_factor(self):
        return self.factors.filter(PlantFactor.factor_type == PlantGrowthFactor.SOIL_TEMPERATURE).one()

    @property
    def soil_moisture_factor(self):
        return self.factors.filter(PlantFactor.factor_type == PlantGrowthFactor.SOIL_MOISTURE).one()

    @property
    def triggered_actions(self):
        triggers = [t for t in self.triggers.all() if t.is_triggered]
        return [{'action_type': t.action_type.value, 'controller': t.controller.controller_type.value} for t in triggers]


class PlantFactor(Base):

    __tablename__ = 'plant_factors'

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey('plants.id'))
    factor_type = Column(Enum(PlantGrowthFactor))
    channel_id = Column(Integer, ForeignKey('device_channels.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    plant = relationship("Plant", uselist=False, back_populates="factors")
    channel = relationship("DeviceChannel", back_populates="plant_factor")
    triggers = relationship("PlantFactorTrigger", order_by='PlantFactorTrigger.id', back_populates="factor")

    @property
    def latest_value(self):
        return self.channel.latest_value

    @property
    def display_name(self):
        return FACTOR_NAME[self.factor_type]


class PlantFactorTrigger(Base):

    __tablename__ = 'plant_factor_triggers'

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey('plants.id'))
    factor_id = Column(Integer, ForeignKey('plant_factors.id'))
    threshold = Column(Float, nullable=True)
    operator = Column(Enum(RelationOperator), nullable=True)
    controller_id = Column(Integer, ForeignKey('device_controllers.id'))
    action_type = Column(Enum(TriggerActionType))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    plant = relationship("Plant", uselist=False, back_populates="triggers")
    factor = relationship("PlantFactor", uselist=False, back_populates="triggers")
    controller = relationship("DeviceController", uselist=False, back_populates="triggers")

    def is_triggered_by_value(self, value):
        operators = {
            '>': self._gt,
            '<': self._lt,
            '=': self._eq
        }
        if self.operator and self.threshold:
            return operators[self.operator](value)
        else:
            return False

    @property
    def is_triggered(self):
        if self.factor.latest_value:
            return self.is_triggered_by_value(self.factor.latest_value.value)
        else:
            return False

    def _eq(self, value):
        return value == self.threshold

    def _gt(self, value):
        return value > self.threshold

    def _lt(self, value):
        return value < self.threshold


class PlantSnapshot(Base):

    __tablename__ = 'plant_snapshots'

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey('plants.id'))
    memo = Column(Text, nullable=True)
    event = Column(String(64))
    plant_status = Column(Enum(PlantStatus), default=PlantStatus.GERMINATION.value)
    created_at = Column(DateTime, default=datetime.now)

    plant = relationship("Plant", uselist=False, back_populates="snapshots")

    def __str__(self):
        return "<{}>: {}".format(self.__class__.__name__, self.pk)

    @property
    def image_path(self):
        return "images/snapshots/{}.jpg".format(self.created_at.strftime("%Y%m%d%H%M%s"))


Base.metadata.create_all(engine)

