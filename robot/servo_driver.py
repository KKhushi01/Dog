# robot/servo_driver.py

import time
import math
import atexit
import RPi.GPIO as GPIO
from . import config


class GPIOServoController:
    """
    Simple GPIO PWM-based servo controller.

    Uses BCM pin numbering.
    """

    def __init__(self, frequency=config.SERVO_FREQ):
        self.frequency = frequency
        self._pwms = {}
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        atexit.register(self.cleanup)

    def setup_servo(self, pin):
        if pin in self._pwms:
            return
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, self.frequency)
        pwm.start(0)  # 0% duty initially
        self._pwms[pin] = pwm

    def set_servo_pulse(self, pin, pulse_us):
        """
        Set pulse width in microseconds on the given pin.
        """
        if pin not in self._pwms:
            self.setup_servo(pin)

        period_us = 1_000_000.0 / self.frequency  # e.g., 20,000 us at 50 Hz
        duty_cycle = 100.0 * (pulse_us / period_us)  # percentage
        duty_cycle = max(0.0, min(100.0, duty_cycle))
        self._pwms[pin].ChangeDutyCycle(duty_cycle)

    def cleanup(self):
        for pwm in self._pwms.values():
            try:
                pwm.stop()
            except Exception:
                pass
        self._pwms.clear()
        try:
            GPIO.cleanup()
        except Exception:
            pass


class Servo:
    def __init__(self, controller: GPIOServoController, pin: int,
                 min_us=config.SERVO_MIN_US,
                 max_us=config.SERVO_MAX_US,
                 min_angle=0.0, max_angle=180.0):
        self.controller = controller
        self.pin = pin
        self.min_us = min_us
        self.max_us = max_us
        self.min_angle = min_angle
        self.max_angle = max_angle

        # Ensure PWM is set up
        self.controller.setup_servo(pin)

    def angle_to_pulse(self, angle_deg):
        # clamp angle
        angle = max(self.min_angle, min(self.max_angle, angle_deg))
        span = self.max_us - self.min_us
        normalized = (angle - self.min_angle) / (self.max_angle - self.min_angle)
        return int(self.min_us + span * normalized)

    def set_angle(self, angle_deg):
        pulse = self.angle_to_pulse(angle_deg)
        self.controller.set_servo_pulse(self.pin, pulse)

    def off(self):
        # Optionally turn off PWM (0% duty)
        self.controller.set_servo_pulse(self.pin, 0)
