import cv2
import mediapipe as mp
import numpy as np
import time
import math
import identifier
from multiprocessing import Process
from multiprocessing import Value
from enum import Enum

class Vision:
    def mode(self, mode):
        self._mode = mode
    
    def motors(self, motor1, motor2, motor3, motor4, motor5):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor3 = motor3
        self.motor4 = motor4
        self.motor5 = motor5
        
        self.MAX_RANGE = 2048
        
        self.id = identifier.Identifier(motor1, motor2, motor3, motor4, motor5)
        self.id_state = Value('i', True)
        self.f1_prev = Value('i', 0)
        self.f2_prev = Value('i', 0)
        self.f3_prev = Value('i', 0)
        self.f4_prev = Value('i', 0)
        self.f5_prev = Value('i', 0)
        
        self.t_state = Value('i', True)
        self.t_accum = Value('d', 0.0)
        self.t_start = 0.0
        
        self.i_state = Value('i', True)
        self.i_accum = Value('d', 0.0)
        self.i_start = 0.0
        
        self.m_state = Value('i', True)
        self.m_accum = Value('d', 0.0)
        self.m_start = 0.0
        
        self.r_state = Value('i', True)
        self.r_accum = Value('d', 0.0)
        self.r_start = 0.0
        
        self.p_state = Value('i', True)
        self.p_accum = Value('d', 0.0)
        self.p_start = 0.0


    def flash(self, frame):
        #(input, pt1, pt2, color, line thickness, line type)
        flash = cv2.rectangle(frame, (0, 0), (400, 300), (174, 250, 92), 10, 8)
        cv2.imshow('Hand Tracker', flash)
    
    #0.25 is TUNED (for this camera at least)
    def raw_closed(self, array):
        if (array[0] < 0.25 and array[0] > 0.0):
            return True
        
    def raw_open(self, array):
        #print(array[0])
        if (array[0] > 0.25 and array[0] < 1.0):
            return True
    
    def run(self):        
        class Mode(Enum):
            DEFAULT = 0
            HAND_COPY = 1
            RPS = 2
        
        hands_solution = mp.solutions.hands
        overlay = mp.solutions.drawing_utils
        hand = hands_solution.Hands(static_image_mode=False,
                         max_num_hands=1,
                         min_detection_confidence=0.1,
                         min_tracking_confidence=0.5)

        need_to_calibrate = True
        count = -1
        init_motors = True
        id_wait = Value('i', 0)
        
        end = False
        capture = cv2.VideoCapture(0)

        cols = 30
        thumb = ([0.0] * cols)
        index = ([0.0] * cols)
        middle = ([0.0] * cols)
        ring = ([0.0] * cols)
        pinkie = ([0.0] * cols)
        max_t = 0.0
        min_t = 1.0
        max_i = 0.0
        min_i = 1.0
        max_m = 0.0
        min_m = 1.0
        max_r = 0.0
        min_r = 1.0
        max_p = 0.0
        min_p = 1.0
 
        previous_cycle_time = time.perf_counter()
        
        while end == False:
            
            tv, image = capture.read()
            #read returns false if there is no image, store in tv
            #image stores the image vector from the camera

            frame = cv2.resize(image, (400, 300))
            #make image easier to process
            
            color_change = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #better tracking, colors to RGB for mediapipe
            
            hand_landmarks = hand.process(color_change).multi_hand_landmarks
            #process the image and make landmarks on each joint

            if (count == -1):
                print('- Please keep your hand in a closed position')
                print('- Put your thumb on the first joint of your index finger')
                print('- Fully open your hand when the screen flashes green')
                print('- Have fun!')
                count = 0

            if hand_landmarks != None:
                #if there is hand in frame
                
                for handLandmarks in hand_landmarks:
                    
                    #draw the hand landmarks onto the frame
                    overlay.draw_landmarks(frame, handLandmarks)
                    
                    x = [landmark.x for landmark in handLandmarks.landmark]
                    y = [landmark.y for landmark in handLandmarks.landmark]
                    z = [landmark.z for landmark in handLandmarks.landmark]
                    
                    scale_x = max(x) - min(x)
                    scale_y = max(y) - min(y)
                    scale_z = max(z) - min(z)

                    if (scale_x > scale_y):
                        scale = 1/scale_x
                    elif (scale_y > scale_z):
                        scale = 1/scale_y
                    else:
                        scale = 1/scale_z
                    
                    
                    coordinates = handLandmarks.landmark[4]
                    distance = math.sqrt(
                          #landmark 6 is an index finger joint
                          math.pow((coordinates.x - handLandmarks.landmark[6].x) * scale, 2)
                        + math.pow((coordinates.y - handLandmarks.landmark[6].y) * scale, 2)
                        + math.pow((coordinates.z - handLandmarks.landmark[6].z) * scale, 2)
                        )
                    thumb.pop(cols - 1)
                    thumb.insert(0, round(distance, 5))
                    if (need_to_calibrate and count < 50):
                        if (np.min(thumb) < min_t):
                            min_t = np.min(thumb)
                        if (np.max(thumb) > max_t):
                            max_t = np.max(thumb)
                    thumb_n = (thumb - min_t) / (max_t - min_t)
                    
                    
                    #calibration is needed to normalize values accurately
                    if (need_to_calibrate):
                        if(self.raw_closed(self, thumb)):
                            if (count <= 10):
                                print('Closed')
                                count += 1
                        if(count == 7):
                            self.flash(self, frame)
                        if(count == 10):
                            self.flash(self, frame)
                            
                        if(count > 10 and self.raw_open(self, thumb)):
                            if (count <= 20):
                                print('Open')
                            count += 1
                        if(count == 18):
                            self.flash(self, frame)
                        if(count == 21):
                            self.flash(self, frame)
                        if(count == 24):
                            print('Calibrated')
                            print()
                            self.flash(self, frame)
                            need_to_calibrate = False
                    
                    coordinates = handLandmarks.landmark[8]
                    #landmark 5 is base of index
                    #landmark 0 is wrist
                    reference_x = (handLandmarks.landmark[5].x + handLandmarks.landmark[1].x) / 2
                    reference_y = (handLandmarks.landmark[5].y + handLandmarks.landmark[1].y) / 2
                    reference_z = (handLandmarks.landmark[5].z + handLandmarks.landmark[1].z) / 2
                    distance = math.sqrt(
                          math.pow((coordinates.x - reference_x) * scale, 2)
                        + math.pow((coordinates.y - reference_y) * scale, 2)
                        + math.pow((coordinates.z - reference_z) * scale, 2)
                        )
                    index.pop(cols - 1)
                    index.insert(0, round(distance, 5))
                    if (need_to_calibrate and count < 50):
                        if (np.min(index) < min_i):
                            min_i = np.min(index)
                        if (np.max(index) > max_i):
                            max_i = np.max(index)
                    index_n = (index - min_i) / (max_i - min_i)                    
                    
                    
                    coordinates = handLandmarks.landmark[12]
                    #landmark 9 is base of middle
                    #landmark 0 is wrist
                    reference_x = (handLandmarks.landmark[9].x + handLandmarks.landmark[0].x) / 2
                    reference_y = (handLandmarks.landmark[9].y + handLandmarks.landmark[0].y) / 2
                    reference_z = (handLandmarks.landmark[9].z + handLandmarks.landmark[0].z) / 2
                    distance = math.sqrt(
                          math.pow((coordinates.x - reference_x) * scale, 2)
                        + math.pow((coordinates.y - reference_y) * scale, 2)
                        + math.pow((coordinates.z - reference_z) * scale, 2)
                        )
                    middle.pop(cols - 1)
                    middle.insert(0, round(distance, 5))
                    if (need_to_calibrate and count < 50):
                        if (np.min(middle) < min_m):
                            min_m = np.min(middle)
                        if (np.max(middle) > max_m):
                            max_m = np.max(middle)
                    middle_n = (middle - min_m) / (max_m - min_m)
                    
                    
                    coordinates = handLandmarks.landmark[16]
                    #landmark 13 is base of ring
                    #landmark 0 is wrist
                    reference_x = (handLandmarks.landmark[13].x + handLandmarks.landmark[0].x) / 2
                    reference_y = (handLandmarks.landmark[13].y + handLandmarks.landmark[0].y) / 2
                    reference_z = (handLandmarks.landmark[13].z + handLandmarks.landmark[0].z) / 2
                    distance = math.sqrt(
                          math.pow((coordinates.x - reference_x) * scale, 2)
                        + math.pow((coordinates.y - reference_y) * scale, 2)
                        + math.pow((coordinates.z - reference_z) * scale, 2)
                        )
                    ring.pop(cols - 1)
                    ring.insert(0, round(distance, 5))
                    if (need_to_calibrate and count < 50):                    
                        if (np.min(ring) < min_r):
                            min_r = np.min(ring)
                        if (np.max(ring) > max_r):
                            max_r = np.max(ring)
                    ring_n = (ring - min_r) / (max_r - min_r)
                    
                    
                    coordinates = handLandmarks.landmark[20]
                    #landmark 17 is base of pinkie
                    #landmark 0 is wrist
                    reference_x = (handLandmarks.landmark[17].x + handLandmarks.landmark[0].x) / 2
                    reference_y = (handLandmarks.landmark[17].y + handLandmarks.landmark[0].y) / 2
                    reference_z = (handLandmarks.landmark[17].z + handLandmarks.landmark[0].z) / 2
                    distance = math.sqrt(
                          math.pow((coordinates.x - reference_x) * scale, 2)
                        + math.pow((coordinates.y - reference_y) * scale, 2)
                        + math.pow((coordinates.z - reference_z) * scale, 2)
                        )
                    pinkie.pop(cols - 1)
                    pinkie.insert(0, round(distance, 5))
                    if (need_to_calibrate and count < 50):
                        if (np.min(pinkie) < min_p):
                            min_p = np.min(pinkie)
                        if (np.max(pinkie) > max_p):
                            max_p = np.max(pinkie)
                    pinkie_n = (pinkie - min_p) / (max_p - min_p)
                    
                    if (count >= 24):
                         count += 1
        
#             print('Cycle Time Difference')
#             print(time.perf_counter() - previous_cycle_time)
#             previous_cycle_time = time.perf_counter()

            if(self._mode.value == Mode.HAND_COPY.value and not need_to_calibrate and init_motors):
                self.t_accum.value = (1 - (thumb_n[0] + thumb_n[1] + thumb_n[2])/3)    * self.MAX_RANGE * 0.8
                self.i_accum.value = (1 - (index_n[0] + index_n[1] + index_n[2])/3)    * self.MAX_RANGE * 1.6
                self.m_accum.value = (1 - (middle_n[0] + middle_n[1] + middle_n[2])/3) * self.MAX_RANGE * 1.7
                self.r_accum.value = (1 - (ring_n[0] + ring_n[1] + ring_n[2])/3)       * self.MAX_RANGE * 1.3
                self.p_accum.value = (1 - (pinkie_n[0] + pinkie_n[1] + pinkie_n[2])/3) * self.MAX_RANGE * 0.9             
                self.t_start = self.t_accum.value
                self.i_start = self.i_accum.value
                self.m_start = self.m_accum.value
                self.r_start = self.r_accum.value
                self.p_start = self.p_accum.value
                
                init_motors = False
                
            if(self._mode.value == Mode.HAND_COPY.value and not need_to_calibrate):
                if (self.t_state.value):
                    Process(
                        target = self.motor1.set_pos,
                        args = (
                            (thumb_n[0] + thumb_n[1] + thumb_n[2])/3,
                            self.t_state,
                            self.t_accum,
                            )
                        ).start()

                if (self.i_state.value):
                    Process(
                        target = self.motor2.set_pos,
                        args = (
                            (index_n[0] + index_n[1] + index_n[2])/3,
                            self.i_state,
                            self.i_accum,
                            )
                        ).start()
                
                if (self.m_state.value):
                    Process(
                        target = self.motor3.set_pos,
                        args = (
                            (middle_n[0] + middle_n[1] + middle_n[2])/3,
                            self.m_state,
                            self.m_accum,
                            )
                        ).start()
                    
                
                if (self.r_state.value):
                    Process(
                        target = self.motor4.set_pos,
                        args = (
                            (ring_n[0] + ring_n[1] + ring_n[2])/3,
                            self.r_state,
                            self.r_accum,
                            )
                        ).start()
                
                if (self.p_state.value):
                    Process(
                        target = self.motor5.set_pos,
                        args = (
                            (pinkie_n[0] + pinkie_n[1] + pinkie_n[2])/3,
                            self.p_state,
                            self.p_accum,
                            )
                        ).start()
            
            if(self._mode.value == Mode.RPS.value and not need_to_calibrate):
                if (self.id_state.value and id_wait.value > 60):
                    Process(target=self.id.identify, args=(
                        (thumb_n[0] + thumb_n[1] + thumb_n[2])/3,
                        (index_n[0] + index_n[1] + index_n[2])/3,
                        (middle_n[0] + middle_n[1] + middle_n[2])/3,
                        (ring_n[0] + ring_n[1] + ring_n[2])/3,
                        (pinkie_n[0] + pinkie_n[1] + pinkie_n[2])/3,
                        self.id_state,
                        id_wait,
                        self.f1_prev,
                        self.f2_prev,
                        self.f3_prev,
                        self.f4_prev,
                        self.f5_prev,
                        )).start()
                else:
                    if (id_wait.value == 0):
                        print('Be ready in 3')
                    if (id_wait.value == 20):
                        print('Be ready in 2')
                    if (id_wait.value == 40):
                        print('Be ready in 1')
                    id_wait.value += 1

            cv2.imshow('Hand Tracker', frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                print(self.motor2.fwd_amt.value)
                print(self.motor2.bwd_amt.value)
                p1 = Process(target=self.motor1.reset, args=(self.t_accum.value - self.t_start + self.f1_prev.value,))
                p2 = Process(target=self.motor2.reset, args=(self.i_accum.value - self.i_start + self.f2_prev.value,))
                p3 = Process(target=self.motor3.reset, args=(self.m_accum.value - self.m_start + self.f3_prev.value,))
                p4 = Process(target=self.motor4.reset, args=(self.r_accum.value - self.r_start + self.f4_prev.value,))
                p5 = Process(target=self.motor5.reset, args=(self.p_accum.value - self.p_start + self.f5_prev.value,))
                
                processes = [p1, p2, p3, p4, p5]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                print('Vision End')
                print(self.motor2.fwd_amt.value)
                print(self.motor2.bwd_amt.value)
                end = True
                
        capture.release()
        cv2.destroyAllWindows()
        return