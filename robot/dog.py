# robot/dog.py

import time
from .servo_driver import GPIOServoController
from .leg import Leg
from . import motions, config


class SpotMicroDog:
    def __init__(self):
        self.controller = GPIOServoController()
        self.legs = {
            "FL": Leg("FL", self.controller),
            "FR": Leg("FR", self.controller),
            "RL": Leg("RL", self.controller),
            "RR": Leg("RR", self.controller),
        }
        self.current_pose = motions.STAND_POSE
        self._apply_pose(self.current_pose)

    def _apply_pose(self, pose_dict):
        for leg_name, joints in pose_dict.items():
            leg = self.legs[leg_name]
            leg.set_angles(
                joints["shoulder"],
                joints["upper"],
                joints["lower"],
            )

    def _interpolate_pose(self, target_pose, duration=config.DEFAULT_MOVE_TIME, steps=20):
        start_pose = self.current_pose
        for i in range(1, steps + 1):
            alpha = i / steps
            intermediate = {}
            for leg_name in self.legs.keys():
                intermediate[leg_name] = {}
                for joint in ["shoulder", "upper", "lower"]:
                    a0 = start_pose[leg_name][joint]
                    a1 = target_pose[leg_name][joint]
                    intermediate[leg_name][joint] = a0 + alpha * (a1 - a0)
            self._apply_pose(intermediate)
            time.sleep(duration / steps)
        self.current_pose = target_pose

    def stand(self):
        self._interpolate_pose(motions.STAND_POSE)

    def sit(self):
        self._interpolate_pose(motions.SIT_POSE)
