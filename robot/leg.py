# robot/leg.py

from .servo_driver import Servo
from . import config


class Leg:
    def __init__(self, name: str, controller):
        self.name = name
        pins = config.SERVO_PINS[name]
        self.shoulder = Servo(controller, pins["shoulder"])
        self.upper = Servo(controller, pins["upper"])
        self.lower = Servo(controller, pins["lower"])

    def set_angles(self, shoulder_deg, upper_deg, lower_deg):
        self.shoulder.set_angle(shoulder_deg)
        self.upper.set_angle(upper_deg)
        self.lower.set_angle(lower_deg)

    def neutral(self):
        self.set_angles(
            config.NEUTRAL_ANGLES["shoulder"],
            config.NEUTRAL_ANGLES["upper"],
            config.NEUTRAL_ANGLES["lower"],
        )
