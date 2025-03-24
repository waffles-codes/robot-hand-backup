import vision as vis
import motor
import RPi.GPIO as GPIO
import pynput.keyboard as keyboard
from enum import Enum
from pynput import keyboard
from pynput.keyboard import Key
from multiprocessing import Value

class Finger(Enum):
    THUMB = 1
    INDEX = 2
    MIDDLE = 3
    RING = 4
    PINKIE = 5

motor1 = motor.Motor(4, 17, 27, 22, Finger.THUMB, Value('i', 0), Value('i', 0))
motor2 = motor.Motor(18, 23, 24, 25, Finger.INDEX, Value('i', 0), Value('i', 0))
motor3 = motor.Motor(9, 5, 6, 13, Finger.MIDDLE, Value('i', 0), Value('i', 0))
motor4 = motor.Motor(8, 7, 12, 16, Finger.RING, Value('i', 0), Value('i', 0))
motor5 = motor.Motor(19, 26, 20, 21, Finger.PINKIE, Value('i', 0), Value('i', 0))

def move_thumb(key):
    if (key == keyboard.Key.up):
        motor1.run(25)
    if (key == keyboard.Key.down):
        motor1.run(-25)
    if (key == keyboard.Key.space):
        return False

def move_index(key):
    if (key == keyboard.Key.up):
        motor2.run(25)
    if (key == keyboard.Key.down):
        motor2.run(-25)
    if (key == keyboard.Key.space):
        return False

def move_middle(key):
    if (key == keyboard.Key.up):
        motor3.run(25)
    if (key == keyboard.Key.down):
        motor3.run(-25)
    if (key == keyboard.Key.space):
        return False

def move_ring(key):
    if (key == keyboard.Key.up):
        motor4.run(25)
    if (key == keyboard.Key.down):
        motor4.run(-25)
    if (key == keyboard.Key.space):
        return False

def move_pinkie(key):
    if (key == keyboard.Key.up):
        motor5.run(25)
    if (key == keyboard.Key.down):
        motor5.run(-25)
    if (key == keyboard.Key.space):
        return False

def main():
    class Mode(Enum):
        DEFAULT = 0
        HAND_COPY = 1
        RPS = 2
    
    vision = vis.Vision
    
    while True:
        print('Does the hand need manual calibration?')
        print('Enter \'1\' for yes and \'0\' for no')
        usr_input = input()
        if (usr_input == '1'):
            print('Moving Thumb')
            print('Press SPACEBAR to stop')
            with keyboard.Listener(on_press = move_thumb) as listener:
                    listener.join()
            print()
            
            print('Moving Index')
            print('Press SPACEBAR to stop')
            with keyboard.Listener(on_press = move_index) as listener:
                    listener.join()
            print()

                    
            print('Moving Middle')
            print('Press SPACEBAR to stop')
            with keyboard.Listener(on_press = move_middle) as listener:
                    listener.join()
            print()
            
            print('Moving Ring')
            print('Press SPACEBAR to stop')
            with keyboard.Listener(on_press = move_ring) as listener:
                    listener.join()
            print()
            
            print('Moving Pinkie')
            print('Press SPACEBAR to stop')
            with keyboard.Listener(on_press = move_pinkie) as listener:
                    listener.join()
            print()
            
            break
        
        if (usr_input == '0'):
            break

    
    while True:
        print('Enter the mode you would like to use: ')
        print('\'0\' to quit')
        print('\'1\' is copy hand motion')
        print('\'2\' is rock paper scissors')
        usr_input = input()
        if (usr_input == '0'):
            print('Okay, quitting!')
            break
        elif (usr_input == '1'):
            vision.mode(vision, Mode.HAND_COPY)
            vision.motors(vision, motor1, motor2, motor3, motor4, motor5)
            vision.run(vision)
            break
        elif (usr_input == '2'):
            vision.mode(vision, Mode.RPS)
            vision.motors(vision, motor1, motor2, motor3, motor4, motor5)
            vision.run(vision)
            break
        else:
            print()
            print('That is an invalid input, try again.')
            print()
            print()

    GPIO.cleanup()
    
if __name__ == "__main__":
    main()