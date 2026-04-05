from robot.dog import SpotMicroDog
import time

dog = SpotMicroDog()

LEGS = ["FL", "FR", "RL", "RR"]
JOINTS = ["shoulder", "upper", "lower"]

def test_servo(leg, joint):
    servo = getattr(dog.legs[leg], joint)

    print(f"\nTesting {leg} - {joint}")
    
    angles = [90, 30, 150, 90]  # center → one side → other side → center
    
    for angle in angles:
        print(f"Angle: {angle}")
        servo.set_angle(angle)
        time.sleep(1.5)

while True:
    print("\nAvailable legs:", LEGS)
    leg = input("Enter leg (or 'q' to quit): ").strip().upper()
    
    if leg == 'Q':
        break
    if leg not in LEGS:
        print("Invalid leg")
        continue

    print("Available joints:", JOINTS)
    joint = input("Enter joint: ").strip().lower()
    
    if joint not in JOINTS:
        print("Invalid joint")
        continue

    test_servo(leg, joint)