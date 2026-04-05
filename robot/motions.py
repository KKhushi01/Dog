# robot/motions.py

# Poses: leg -> joint -> angle (degrees)
# 0–180 range assumed for now, adjust once you see motion.

STAND_POSE = {
    "FL": {"shoulder": 20, "upper": 70, "lower": 80},
    "FR": {"shoulder": 20, "upper": 20, "lower": 30},
    "RL": {"shoulder": 0, "upper": 30, "lower": 0},
    "RR": {"shoulder": 20, "upper": 60, "lower": 20},
    
}

SIT_POSE = {
    # Front legs more vertical/straight
    "FL": {"shoulder": 90, "upper": 80, "lower": 120},
    "FR": {"shoulder": 90, "upper": 80, "lower": 120},
    # Rear legs folded under body
    "RL": {"shoulder": 90, "upper": 130, "lower": 60},
    "RR": {"shoulder": 90, "upper": 130, "lower": 60},
}



# "FL": {"shoulder": 0, "upper": 0, "lower": 0},
    # "FR": {"shoulder": 0, "upper": 0, "lower": 0},
    # "RL": {"shoulder": 0, "upper": 0, "lower": 0},
    # "RR": {"shoulder": 0, "upper": 0, "lower": 0},