import time
from multiprocessing import Process

class Identifier:
    def __init__(self, motor1, motor2, motor3, motor4, motor5):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor3 = motor3
        self.motor4 = motor4
        self.motor5 = motor5
        
        self.MAX_RANGE = 4096
        
        #0.X is to make sure it doesn't go too far
        #because the motors are calibrated with tolerance
        #for hand tracking/copy function
        self.f1 = round(0.9 * self.MAX_RANGE * 1.7)
        self.f2 = round(0.9 * self.MAX_RANGE * 2)
        self.f3 = round(0.9 * self.MAX_RANGE * 2.1)
        self.f4 = round(0.9 * self.MAX_RANGE * 1.9)
        self.f5 = round(0.9 * self.MAX_RANGE * 1.7)
    
    def identify(self, thumb, index, middle, ring, pinkie, state, wait, f1_prev, f2_prev, f3_prev, f4_prev, f5_prev):
        state.value = False        
        processes = []
        
        if (
            thumb < 0.5 and
            index < 0.3 and
            middle < 0.3 and
            ring < 0.3 and
            pinkie < 0.3
            ):
            print('You went ROCK')
#             print(self.f1, f1_prev.value)
#             print(self.f2, f2_prev.value)
#             print(self.f3, f3_prev.value)
#             print(self.f4, f4_prev.value)
#             print(self.f5, f5_prev.value)
            if (not f1_prev.value == 0):
                p1 = Process(target = self.motor1.run, args = (-self.f1,))
                f1_prev.value = 0
                processes.append(p1)
                
            if (not f2_prev.value == 0):
                p2 = Process(target = self.motor2.run, args = (-self.f2,))
                f2_prev.value = 0
                processes.append(p2)
                
            if (not f3_prev.value == 0):
                p3 = Process(target = self.motor3.run, args = (-self.f3,))
                f3_prev.value = 0
                processes.append(p3)
                
            if (not f4_prev.value == 0):
                p4 = Process(target = self.motor4.run, args = (-self.f4,))
                f4_prev.value = 0
                processes.append(p4)
                
            if (not f5_prev.value == 0):
                p5 = Process(target = self.motor5.run, args = (-self.f5,))
                f5_prev.value = 0
                processes.append(p5)
                                
            for p in processes:
                p.start()
                
            for p in processes:
                p.join()
            
            processes.clear()
            print('I went PAPER HAHA YOU LOSE!!!')
            
        elif (
            thumb > 0.8 and
            index > 0.8 and
            middle > 0.8 and
            ring > 0.8 and
            pinkie > 0.8
            ):
            print('you went PAPER')
            if (not f1_prev.value == self.f1):
                p1 = Process(target = self.motor1.run, args = (self.f1,))
                f1_prev.value = self.f1
                processes.append(p1)
                
            if (not f2_prev.value == 0):
                p2 = Process(target = self.motor2.run, args = (-self.f2,))
                f2_prev.value = 0
                processes.append(p2)
                
            if (not f3_prev.value == 0):
                p3 = Process(target = self.motor3.run, args = (-self.f3,))
                f3_prev.value = 0
                processes.append(p3)
                
            if (not f4_prev.value == self.f4):
                p4 = Process(target = self.motor4.run, args = (self.f4,))
                f4_prev.value = self.f4
                processes.append(p4)
                
            if (not f5_prev.value == self.f5):
                p5 = Process(target = self.motor5.run, args = (self.f5,))
                f5_prev.value = self.f5
                processes.append(p5)
                                
            for p in processes:
                p.start()
                
            for p in processes:
                p.join()
            
            processes.clear()
            print('I went SCISSORS HAHA YOU LOSE!!!')
            
        elif (
            index > 0.8 and
            middle > 0.8 and
            ring < 0.3 and
            pinkie < 0.3
            ):
            print('You went SCISSORS')
            if (not f1_prev.value == self.f1):
                p1 = Process(target = self.motor1.run, args = (self.f1,))
                f1_prev.value = self.f1
                processes.append(p1)
                
            if (not f2_prev.value == self.f2):
                p2 = Process(target = self.motor2.run, args = (self.f2,))
                f2_prev.value = self.f2
                processes.append(p2)
                
            if (not f3_prev.value == self.f3):
                p3 = Process(target = self.motor3.run, args = (self.f3,))
                f3_prev.value = self.f3
                processes.append(p3)
                
            if (not f4_prev.value == self.f4):
                p4 = Process(target = self.motor4.run, args = (self.f4,))
                f4_prev.value = self.f4
                processes.append(p4)
                
            if (not f5_prev.value == self.f5):
                p5 = Process(target = self.motor5.run, args = (self.f5,))
                f5_prev.value = self.f5
                processes.append(p5)
                                
            for p in processes:
                p.start()
                
            for p in processes:
                p.join()
            
            processes.clear()
            print('I went ROCK HAHA YOU LOSE!!!')
            
        print()
        wait.value = 0
        state.value = True