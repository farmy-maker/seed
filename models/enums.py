# coding: utf-8
from enum import Enum


class EnumBase(Enum):

    def __eq__(self, other):
        if isinstance(other, EnumBase):
            return self.name == other.name
        else:
            return self.value == other

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def choices(cls):
        return tuple((m.value, m.name) for m in cls)


FACTOR_NAME = dict(
    temperature=u"温度",
    humidity=u"湿度",
    light=u"照度",
    soil_moisture=u"水分",
    soil_temperature=u"土壌温度"
)


class PlantGrowthFactor(EnumBase):

    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    LIGHT = 'light'
    SOIL_MOISTURE = 'soil_moisture'
    SOIL_TEMPERATURE = 'soil_temperature'

    @property
    def display_name(self):
        return FACTOR_NAME[self]


STATUS_NAME = dict(
    germination='発芽',
    soil="種"
)


class PlantStatus(EnumBase):

    GERMINATION = 'germination'
    SOIL = 'soil'

    @property
    def display_name(self):
        return STATUS_NAME[self]


class PlantControllerType(EnumBase):

    LED = "led"
    PUMP = "pump"


class RelationOperator(EnumBase):

    GREATER_THAN = '>'
    LESS_THEN = '<'
    EQUAL_TO = '='


class TriggerActionType(EnumBase):

    TURN_ON = 'turn_on'
    TURN_OFF = 'turn_off'
    TOGGLE = 'toggle'
    FLASH = 'flash'
    FLASH_LONG = 'flash_long'


HARD_LEVEL_NAME = {1: '簡単', 2: "中", 3: "難"}


class HardLevel(EnumBase):

    EASY = 1
    NORMAL = 2
    HARD = 3

    @property
    def display_name(self):
        return HARD_LEVEL_NAME[self.value]


class DeviceType(EnumBase):

    OFFICIAL = 'official'
    NORMAL = 'normal'
    ABSTRACT = 'abstract'


class ChannelType(EnumBase):

    INPUT = "input"
    OUTPUT = "output"


class ModuleType(EnumBase):

    SENSOR = 'sensor'
    CONTROLLER = 'controller'

