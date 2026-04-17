from adafruit_servokit import ServoKit
import time

# Initialize PCA9685 (16 channels)
kit = ServoKit(channels=16)

# -------- SERVO CHANNEL MAPPING --------
legs = {
    "FL": [0, 1, 2],   # Front Left
    "FR": [3, 4, 5],   # Front Right
    "BL": [6, 7, 8],   # Back Left
    "BR": [9, 10, 11]  # Back Right
}

# -------- BASIC CONTROL FUNCTIONS --------
def set_servo(channel, angle):
    angle = max(0, min(180, angle))  # clamp safety
    kit.servo[channel].angle = angle

def set_leg(leg, hip, shoulder, knee):
    ch = legs[leg]
    set_servo(ch[0], hip)
    set_servo(ch[1], shoulder)
    set_servo(ch[2], knee)

def move_smooth(channel, start, end, step=1, delay=0.01):
    if start < end:
        for a in range(start, end + 1, step):
            set_servo(channel, a)
            time.sleep(delay)
    else:
        for a in range(start, end - 1, -step):
            set_servo(channel, a)
            time.sleep(delay)

# -------- ROBOT POSES --------
def stand():
    print("Standing...")
    for leg in legs:
        set_leg(leg, 90, 90, 90)

def sit():
    print("Sitting...")
    for leg in legs:
        set_leg(leg, 90, 120, 60)

# -------- TEST FUNCTIONS --------
def test_all_servos():
    print("Testing all servos...")
    for ch in range(12):
        print(f"Channel {ch}")
        set_servo(ch, 90)
        time.sleep(0.5)
        set_servo(ch, 0)
        time.sleep(0.5)
        set_servo(ch, 180)
        time.sleep(0.5)

def test_leg(leg):
    print(f"Testing leg {leg}")
    ch = legs[leg]

    # Move hip
    move_smooth(ch[0], 60, 120)
    move_smooth(ch[0], 120, 60)

    # Move shoulder
    move_smooth(ch[1], 60, 120)
    move_smooth(ch[1], 120, 60)

    # Move knee
    move_smooth(ch[2], 60, 120)
    move_smooth(ch[2], 120, 60)

# -------- INTERACTIVE MENU --------
def menu():
    while True:
        print("\n--- Robot Dog Control ---")
        print("1: Test all servos")
        print("2: Stand")
        print("3: Sit")
        print("4: Test Front Left (FL)")
        print("5: Test Front Right (FR)")
        print("6: Test Back Left (BL)")
        print("7: Test Back Right (BR)")
        print("8: Manual control (channel + angle)")
        print("0: Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            test_all_servos()
        elif choice == "2":
            stand()
        elif choice == "3":
            sit()
        elif choice == "4":
            test_leg("FL")
        elif choice == "5":
            test_leg("FR")
        elif choice == "6":
            test_leg("BL")
        elif choice == "7":
            test_leg("BR")
        elif choice == "8":
            try:
                ch = int(input("Channel (0-15): "))
                ang = int(input("Angle (0-180): "))
                set_servo(ch, ang)
            except:
                print("Invalid input")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

# -------- MAIN --------
if __name__ == "__main__":
    print("Starting Robot Dog Test Program...")
    stand()  # go to neutral on start
    time.sleep(1)
    menu()
