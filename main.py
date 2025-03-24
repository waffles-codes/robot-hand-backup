import vision as vis
import motor
import RPi.GPIO as GPIO
import pynput.keyboard as keyboard
from enum import Enum 

def main():
    class Mode(Enum):
        DEFAULT = 0
        HAND_COPY = 1
        RPS = 2
    
    class Finger(Enum):
        THUMB = 1
        INDEX = 2
        MIDDLE = 3
        RING = 4
        PINKIE = 5
    
    motor1 = motor.Motor(4, 17, 27, 22, Finger.THUMB)
    motor2 = motor.Motor(18, 23, 24, 25, Finger.INDEX)
    motor3 = motor.Motor(9, 5, 6, 13, Finger.MIDDLE)
    motor4 = motor.Motor(8, 7, 12, 16, Finger.RING)
    motor5 = motor.Motor(19, 26, 20, 21, Finger.PINKIE)
    
    vision = vis.Vision
    
    while True:
        print('Enter the mode you would like to use: ')
        print('(0 is just hand tracking)')
        print('(1 is copy hand motion)')
        print('(2 is rock paper scissors)')
        usr_input = input()
        if (usr_input == '0'):
            vision.mode(vision, Mode.DEFAULT)
            break
        elif (usr_input == '1'):
            vision.mode(vision, Mode.HAND_COPY)
            break
        elif (usr_input == '2'):
            vision.mode(vision, Mode.RPS)
            break
        else:
            print()
            print('This is an invalid input, try again.')
            print()

    vision.motors(vision, motor1, motor2, motor3, motor4, motor5)
    vision.run(vision)
    GPIO.cleanup()
    
if __name__ == "__main__":
    main()