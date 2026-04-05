# main.py

import time
from robot.dog import SpotMicroDog

if __name__ == "__main__":
    dog = SpotMicroDog()
    print("Standing...")
    dog.stand()
    time.sleep(2)

    # print("Sitting...")
    # dog.sit()
    # time.sleep(2)

    # print("Back to stand...")
    # dog.stand()
    # time.sleep(2)

    print("Done.")
