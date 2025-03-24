import RPi.GPIO as GPIO
import time

class Motor(object):    
    def __init__(self, in1, in2, in3, in4, finger):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        
        self.delay = 0.0012
        
        self.direction = False
        
#         self.sequence = [[1, 0, 0, 0],
#                          [0, 1, 0, 0],
#                          [0, 0, 1, 0],
#                          [0, 0, 0, 1]]
    
        self.sequence = [[1, 0, 0, 1],
                         [1, 0, 0, 0],
                         [1, 1, 0, 0],
                         [0, 1, 0, 0],
                         [0, 1, 1, 0],
                         [0, 0, 1, 0],
                         [0, 0, 1, 1],
                         [0, 0, 0, 1]]
        
        self.output_pins = [self.in1,self.in2,self.in3,self.in4]
        self.counter = 0;
        
        self.MAX_RANGE = 4096
        
        if (finger.value == 1):
            self.MAX_RANGE = round(4096 * 1.7)
        if (finger.value == 2):
            self.MAX_RANGE = round(4096 * 2)
        if (finger.value == 3):
            self.MAX_RANGE = round(4096 * 2.1)
        if (finger.value == 4):
            self.MAX_RANGE = round(4096 * 1.9)
        if (finger.value == 5):
            self.MAX_RANGE = round(4096 * 1.7)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def set_direction(self, direction):
        self.direction = direction

    def cleanup(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def reset(self, accum_pos):
        print('Resetting', -(accum_pos))
        self.run(-(accum_pos))
        self.cleanup()

    def set_pos(self, pos, state, accum_pos):
        state.value = False
        #pos is given from 
        curr_pos = (1 - pos) * self.MAX_RANGE
        target_pos = curr_pos - accum_pos.value
        if (target_pos > 200 or target_pos < -200):
            accum_pos.value += target_pos/2
            self.run(target_pos)
            accum_pos.value += target_pos/2
        else:
            for pin in range(4):
                GPIO.output(self.output_pins[pin], GPIO.LOW)
        state.value = True

    def run(self, steps):
        if (steps > 0):
            self.direction = False
        else:
            self.direction = True
            
        try:
            for i in range(abs(round(steps))):
                for pin in range(4):
                    GPIO.output(self.output_pins[pin], self.sequence[self.counter][pin])
                
                if (self.direction == True):
                    self.counter = (self.counter - 1) % 8
                elif (self.direction == False):
                    self.counter = (self.counter + 1) % 8
                else:
                    print("Direction Error")
                    self.cleanup()
                    exit(1)
                time.sleep(self.delay)

        except KeyboardInterrupt:
            self.cleanup()
            exit(1)