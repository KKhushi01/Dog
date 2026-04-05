# robot/config.py

# PWM frequency for servos
SERVO_FREQ = 50  # Hz

# ========= EDIT THIS SECTION WITH YOUR GPIO PINS =========
# BCM numbering (GPIO number, NOT physical pin number)
#
# Example only – change to match your wiring.
SERVO_PINS = {
    "FL": {  # Front Left leg
        "shoulder": 4,   # GPIO pin for shoulder servo signal
        "upper": 3,      # GPIO pin for upper leg servo signal
        "lower": 2,      # GPIO pin for lower leg servo signal
    },
    "FR": {  # Front Right leg
        "shoulder": 19,
        "upper": 13,
        "lower": 5,
    },
    "RL": {  # Rear Left leg
        "shoulder": 10,
        "upper": 22,
        "lower": 27,
    },
    "RR": {  # Rear Right leg
        "shoulder": 0,
        "upper": 11,
        "lower": 9,
    },
}
# ========= STOP EDITING HERE FOR PINS =========

# Neutral angle in degrees for each joint (rough starting point)
NEUTRAL_ANGLES = {
    "shoulder": 90.0,  # middle of travel
    "upper": 90.0,
    "lower": 90.0,
}

# Servo pulse limits (tweak later if needed)
SERVO_MIN_US = 500    # 0°
SERVO_MAX_US = 2500   # 180°

# Motion timing defaults
DEFAULT_MOVE_TIME = 0.8  # seconds for a full posture change
