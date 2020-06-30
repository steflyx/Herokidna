# Test version
import RPi.GPIO as GPIO
import time
import telepot
import random
import math
import cv2
import imutils
import numpy as np
import emo_functions
import threading
import pygame
import subprocess
import sys
import os
from telegramCredentials import token

#Music
MusicDirectory = "MusicEffects/"
omxprocess = 0
omxprocess_started = False

GPIO.setmode(GPIO.BCM)

#Color sensors
signal_pond = 5
signal_targ = 6
S2 = 26
S3 = 2
NUM_CYCLES = 10
blue_treshold = 700
red_treshold  = 700
COLOR_BLUE = 0
COLOR_RED  = 1
redexcesslight = 0
GPIO.setup(signal_pond, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(signal_targ, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(S2,GPIO.OUT)
GPIO.setup(S3,GPIO.OUT)
print("Color sensor ok")

#Motors wheels
IN1_WHEEL = 17
IN2_WHEEL = 27
IN3_WHEEL = 23
IN4_WHEEL = 22
ENA_WHEEL = 19
ENB_WHEEL = 12
GPIO.setup(IN1_WHEEL, GPIO.OUT)
GPIO.setup(IN2_WHEEL, GPIO.OUT)
GPIO.setup(IN3_WHEEL, GPIO.OUT)
GPIO.setup(IN4_WHEEL, GPIO.OUT)
GPIO.setup(ENA_WHEEL, GPIO.OUT)
GPIO.setup(ENB_WHEEL, GPIO.OUT)
GPIO.output(ENA_WHEEL,GPIO.HIGH)
GPIO.output(ENB_WHEEL,GPIO.HIGH)
print("Wheel ok")

#Motors target
IN1_TARGET = 14
IN2_TARGET = 15
ENA_TARGET = 18
GPIO.setup(IN1_TARGET, GPIO.OUT)
GPIO.setup(IN2_TARGET, GPIO.OUT)
GPIO.setup(ENA_TARGET, GPIO.OUT)
target_pwm = GPIO.PWM(ENA_TARGET,100)
print("Target ok")

#Motors spines
IN1_SPINES = 24
IN2_SPINES = 16
ENB_SPINES = 20
GPIO.setup(IN1_SPINES, GPIO.OUT)
GPIO.setup(IN2_SPINES, GPIO.OUT)
GPIO.setup(ENB_SPINES, GPIO.OUT)
spines_pwm = GPIO.PWM(ENB_SPINES,100)
print("Spines ok")

#Target
PIN_t = 3
GPIO.setup(PIN_t, GPIO.OUT)
print("Target ok")

#ServoMotor
servoPin = 13
SERVO_MAX = 12.5
SERVO_MID = 7.5
SERVO_MIN = 2.5
GPIO.setup(servoPin, GPIO.OUT)
servo_pwm = GPIO.PWM(servoPin, 50)
servo_pwm.start(SERVO_MAX)
time.sleep(1)
servo_pwm.ChangeDutyCycle(0)
print("Servo ok")

#Ultrasonic sensor
ULTRA_TRIGGER          = 25
ULTRA_ECHO_FRONT       = 8
ULTRA_ECHO_BACK        = 10
ULTRA_ECHO_RIGHT       = 9
ULTRA_ECHO_LEFT_FRONT  = 11
ULTRA_ECHO_LEFT_BACK   = 7
GPIO.setup(ULTRA_TRIGGER, GPIO.OUT)
GPIO.setup(ULTRA_ECHO_FRONT, GPIO.IN)
GPIO.setup(ULTRA_ECHO_BACK, GPIO.IN)
GPIO.setup(ULTRA_ECHO_LEFT_FRONT, GPIO.IN)
GPIO.setup(ULTRA_ECHO_LEFT_BACK, GPIO.IN)
GPIO.setup(ULTRA_ECHO_RIGHT, GPIO.IN)
offset = 0
print("Ultrasonic ok")

#Game info
POINTS_FOR_DRINKING = 20
POINTS_FOR_EATING   = 30
POINTS_FOR_EATEN    = -30
POINTS_FOR_INACTIVE = -1
GAME_DURATION       = 20

#Emotions
EMOTION_DRINKING  = 0
EMOTION_EATING    = 1
EMOTION_ATTACKING = 2
EMOTION_DEFENDING = 3
EMOTION_EATEN     = 4
EMOTION_SLEEP     = 5
EMOTION_NORMAL    = 6
EMOTION_POND_NEAR = 7
current_emotion   = EMOTION_NORMAL

#Set the camera
camera = cv2.VideoCapture(0)
camera.set(3,600)
HUE_VALUE = 170 #red
colorLower = np.array([HUE_VALUE - 5, 100, 100], dtype=np.uint8) #Lower and upper boundary target color
colorUpper = np.array([HUE_VALUE + 5, 255, 255], dtype=np.uint8)
print("Camera ok")


#Functions to control the wheels
def forward():
    GPIO.output(IN1_WHEEL, GPIO.HIGH)
    GPIO.output(IN2_WHEEL, GPIO.LOW)
    GPIO.output(IN3_WHEEL, GPIO.HIGH)
    GPIO.output(IN4_WHEEL, GPIO.LOW)

def right():
    GPIO.output(IN1_WHEEL, GPIO.LOW)
    GPIO.output(IN2_WHEEL, GPIO.LOW)
    GPIO.output(IN3_WHEEL, GPIO.HIGH)
    GPIO.output(IN4_WHEEL, GPIO.LOW)

def left():
    GPIO.output(IN1_WHEEL, GPIO.HIGH)
    GPIO.output(IN2_WHEEL, GPIO.LOW)
    GPIO.output(IN3_WHEEL, GPIO.LOW)
    GPIO.output(IN4_WHEEL, GPIO.LOW)

def backward():
    GPIO.output(IN1_WHEEL, GPIO.LOW)
    GPIO.output(IN2_WHEEL, GPIO.HIGH)
    GPIO.output(IN3_WHEEL, GPIO.LOW)
    GPIO.output(IN4_WHEEL, GPIO.HIGH)

def stop():
    GPIO.output(IN1_WHEEL, GPIO.LOW)
    GPIO.output(IN2_WHEEL, GPIO.LOW)
    GPIO.output(IN3_WHEEL, GPIO.LOW)
    GPIO.output(IN4_WHEEL, GPIO.LOW)
stop()

#Returns whether from input 'signal' the specified color is detected
def is_color(signal, color):

    if color == COLOR_BLUE:
        return get_color(signal, color) > blue_treshold
    if (redexcesslight == 0):
        return get_color(signal, color) > red_treshold
    else:
        return get_color(signal, color) < red_treshold

#Returns the value of the color from "signal" sensor
#low_high for BLUE      #high_high for RED
def get_color(signal, color):

    if color == COLOR_BLUE:
        GPIO.output(S2,GPIO.LOW)
        GPIO.output(S3,GPIO.HIGH)
    else:
        GPIO.output(S2,GPIO.LOW)
        GPIO.output(S3,GPIO.LOW)

    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal,GPIO.FALLING)
    duration = time.time() - start
    result = NUM_CYCLES/duration
    return result

#Used to calibrate the sensors
def calibrate(chat_id):
    bot.sendMessage(chat_id, "I will need you to place me in sequence:\n\
     - on the pond\n\
     - outside of the pond\n\
     - in front of a target\n\
     - away from a target\n\
     You will have ten seconds between each step")
    time.sleep(5)

    #In pond calibration
    bot.sendMessage(chat_id, "Place me on pond")
    time.sleep(10)
    bot.sendMessage(chat_id, "Detecting blue")
    i = 0
    blue = []
    while(i < 100):
        blue.append(get_color(signal_pond, COLOR_BLUE))
        i += 1
    avg_blue = sum(blue)/100

    #Outside pond calibration
    bot.sendMessage(chat_id, "Place me out of the pond")
    time.sleep(10)
    bot.sendMessage(chat_id, "Detecting not blue")
    i = 0
    not_blue = []
    while(i < 100):
        not_blue.append(get_color(signal_pond, COLOR_BLUE))
        i += 1
    avg_not_blue = sum(not_blue)/100

    #Check if red is detected
    bot.sendMessage(chat_id, "Place red target in front of the beak")
    time.sleep(10)
    bot.sendMessage(chat_id, "Detecting red")
    i = 0
    red = []
    while(i < 100):
        red.append(get_color(signal_targ, COLOR_RED))
        i += 1
    avg_red = sum(red)/100

    #Check if red is detected
    bot.sendMessage(chat_id, "Remove red target in front of the beak")
    time.sleep(10)
    bot.sendMessage(chat_id, "Detecting not red")
    i = 0
    not_red = []
    while(i < 100):
        not_red.append(get_color(signal_targ, COLOR_RED))
        i += 1
    avg_not_red = sum(not_red)/100


    #Treshold computation
    global blue_treshold
    global red_treshold
    global redexcesslight
    blue_treshold = avg_not_blue + (avg_blue - avg_not_blue)/2
    red_treshold = avg_not_red + (avg_red - avg_not_red)/2 - 100
    if (avg_not_red > avg_red):
        redexcesslight = 1
        red_treshold = min(red_treshold, avg_red * 2)
    

    #Done
    bot.sendMessage(chat_id, "Calibration done! Here's the results:\n\
        - Blue average: {0:.2f}\n\
        - Not-blue average: {1:.2f}\n\
        - Blue treshold: {2:.2f}\n\
        - Red average: {3:.2f}\n\
        - Not-red average: {4:.2f}\n\
        - Red treshold: {5:.2f}\n".format(avg_blue, avg_not_blue, blue_treshold, avg_red, avg_not_red, red_treshold))


#Function to calibrate ultrasonic sensors
def calibrateUltra(measures, chat_id):
    i = 0
    discarded = 0
    distLeftFront = []
    distLeftBack = []
    #Compute the first mean values
    while (i < 5):
        distLeftFront.append(computeDistance(ULTRA_ECHO_LEFT_FRONT)*100)
        time.sleep(0.03)
        distLeftBack.append(computeDistance(ULTRA_ECHO_LEFT_BACK)*100)
        time.sleep(0.03)
        i += 1
    avgLF = sum(distLeftFront)/i
    avgLB = sum(distLeftBack)/i
    #bot.sendMessage(chat_id, "first avgLF: {0} cm\n first avgLB: {1} cm".format(avgLF,avgLB))
    while(i < measures):
        newLB = computeDistance(ULTRA_ECHO_LEFT_BACK)*100
        time.sleep(0.03)
        newLF = computeDistance(ULTRA_ECHO_LEFT_FRONT)*100
        time.sleep(0.03)
        if (discarded > measures):
            bot.sendMessage(chat_id, "Please try again".format(avgLF,avgLB))
            return 0
        if (newLF > (avgLF*1.1) or newLF < (avgLF*0.9) or newLB > (avgLB*1.1) or newLB < (avgLB*0.9)):
            discarded += 1
            continue
        else:
            distLeftFront.append(newLF)
            distLeftBack.append(newLB)
            i += 1
            avgLF = sum(distLeftFront)/i
            avgLB = sum(distLeftBack)/i
    bot.sendMessage(chat_id, "Left Front: {0} cm\nLeft Back: {1} cm\nDiscarded: {2}".format(avgLF,avgLB,discarded))
    return (avgLF-avgLB)


#Moves the servomotor
#Angle from 0 to 180
def rotateServo(angle):

    pulse = angle * (SERVO_MAX - SERVO_MIN) / 180 + SERVO_MIN
    servo_pwm.ChangeDutyCycle(pulse)
    time.sleep(0.03)
    servo_pwm.ChangeDutyCycle(0)

#Computes distance from ultrasonic sensor
#Trigger is the same for all sensors, echo changes
def computeDistance(echo):

    #Trigger up for 0.01ms
    GPIO.output(ULTRA_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(ULTRA_TRIGGER, False)

    Start = time.time()
    StartWaveTime = time.time()
    StopWaveTime = time.time()

    #Save StartTime
    while GPIO.input(echo) == 0 and (StartWaveTime - Start) < 0.2:
        StartWaveTime = time.time()

    #Save time of arrival
    while GPIO.input(echo) == 1 and (StopWaveTime - Start) < 0.2:
        StopWaveTime = time.time()

    #Time difference between start and arrival
    TimeElapsed = StopWaveTime - StartWaveTime
    distance = (TimeElapsed * 343) / 2

    #To avoid interferences beetween consecutive calls
    time.sleep(0.005)

    #Add the offset for correcting measures on left side
    if (echo == 7):
        distance += offset
    return distance



#Sends a message with the new emotion
def changeEmotion(emotion, chat_id):

    if emotion == EMOTION_DRINKING:
        msg = "I'm drinking!"
        playMusic("Drinking.mp3")
    if emotion == EMOTION_SLEEP:
        msg = "Going to sleep zzzz"
        playMusic("End.mp3")
    if emotion == EMOTION_NORMAL:
        msg = "Just hanging around"
        playMusic("Normal.mp3")
    if emotion == EMOTION_EATEN:
        msg = "Oh no! I've been hit :("
        playMusic("Eaten.mp3")
    if emotion == EMOTION_EATING:
        msg = "Gnam! I'm eating a really good tasting robot! Bon appetit to me :)"
    if emotion == EMOTION_DEFENDING:
        msg = "Damn! I saw something"
    if emotion == EMOTION_POND_NEAR:
        msg = "Sniff sniff... water is close"
    if emotion == EMOTION_ATTACKING:
        msg = "Sniff sniff... someone is close"
        playMusic("Attacking.mp3")


    global current_emotion
    current_emotion = emotion
    bot.sendMessage(chat_id, msg)

#Thread which takes care of spawning the correct emotion thread
def emotionsHandlerTh():
    while True:
        if (current_emotion == EMOTION_NORMAL or current_emotion == EMOTION_POND_NEAR):
            emoTh = threading.Thread(target=emo_functions.standardTh, args=())
        elif (current_emotion == EMOTION_ATTACKING or current_emotion == EMOTION_EATING):
            emoTh = threading.Thread(target=emo_functions.attackTh, args=())
        elif (current_emotion == EMOTION_DRINKING):
            emoTh = threading.Thread(target=emo_functions.drinkTh, args=())
        elif (current_emotion == EMOTION_DEFENDING or current_emotion == EMOTION_EATEN):
            emoTh = threading.Thread(target=emo_functions.defenseTh, args=())
        else:   #elif GAME_ENDED
            emoTh = threading.Thread(target=emo_functions.idleTh, args=())
        emoTh.start()
        emoTh.join()


#Updates score
def updateScore(startTime, stopTime, points, score):
    difTime = int(math.floor(stopTime - startTime)) / 5
    score += difTime * points
    return score



#Checks if target is our being touched
def checkTarget():
    value = GPIO.input(PIN_t)
    return (value == 1)



#Returns False only if all three of them are false
def threeMeasuresResults(measures):
    return (measures[0] or measures[1] or measures[2])


#Lowers neck
def lowerNeck():

    delta_angle = -2.8
    current_angle = 180

    while current_angle > 90:
        rotateServo(current_angle + delta_angle)
        current_angle += delta_angle



#Raises neck
def raiseNeck():
    delta_angle = 3.0
    current_angle = 90

    while current_angle < 180:
        rotateServo(current_angle + delta_angle)
        current_angle += delta_angle




#Checks with camera if enemy is nearby
def checkEnemy(frame):
    #Resize the frame, inverted ("vertical flip" w/ 180degrees),
    #Blur it, and convert it to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Construct a mask for the target color, then perform
    #a series of dilations and erosions to remove any small
    #blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    #Find contours in the mask and initialize the current
    #(x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) == 0:
        return (False, 0)
    else:
        return (True, cnts)


#Tells where the enemy is with respect to the camera
def checkEnemyDirection(cnts, isLastRight, enemy_in_sight):

    if enemy_in_sight:
        #Find the largest contour in the mask, then use
        #it to compute the minimum enclosing circle and
        #centroid
        c = max(cnts, key=cv2.contourArea)
        c = cnts[0]
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        # only proceed if the radius meets a minimum size
        if radius > 5 and radius < 200:

            if x > 400:
                left()
                return False
            if x < 200:
                right()
                return True
            if (x > 200 and x < 400):
                forward()
                return isLastRight

    else:
        if not isLastRight:
            left()
        else:
            right()

    return isLastRight


#Complete version of checkEnemy (merges checkEnemy and checkEnemyDirection)
#NOTE: if we have time, it would be better to implement this version (to check enemy size)
def checkEnemyComplete(frame, isLastRight):

    MIN_RADIUS = 20

    #Resize the frame, inverted ("vertical flip" w/ 180degrees),
    #Blur it, and convert it to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Construct a mask for the target color, then perform
    #a series of dilations and erosions to remove any small
    #blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    #Find contours in the mask and initialize the current
    #(x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) == 0:
        return (False, isLastRight)

    #Find the largest contour in the mask, then use
    #it to compute the minimum enclosing circle and centroid

    c = max(cnts, key=cv2.contourArea)
    c = cnts[0]
    ((x, y), radius) = cv2.minEnclosingCircle(c)

    # only proceed if the radius meets a minimum size
    if radius > MIN_RADIUS and radius < 200:

        if x > 400:
            return (True, False)
        if x < 200:
            return (True, True)
        if (x > 200 and x < 400):
            return (True, True)

    return (False, isLastRight)

#Complete version of checkEnemy (merges checkEnemy and checkEnemyDirection)
#NOTE: if we have time, it would be better to implement this version (to check enemy size)
def checkEnemyComplete(frame, direction):

    MIN_RADIUS = 20
    RIGHT = 0
    FORWARD = 1
    LEFT = 2

    #Resize the frame, inverted ("vertical flip" w/ 180degrees),
    #Blur it, and convert it to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Construct a mask for the target color, then perform
    #a series of dilations and erosions to remove any small
    #blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    #Find contours in the mask and initialize the current
    #(x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) == 0:
        return (False, direction)

    #Find the largest contour in the mask, then use
    #it to compute the minimum enclosing circle and centroid

    c = max(cnts, key=cv2.contourArea)
    c = cnts[0]
    ((x, y), radius) = cv2.minEnclosingCircle(c)

    # only proceed if the radius meets a minimum size
    if radius > MIN_RADIUS and radius < 200:

        if x > 400:
            return (True, RIGHT)
        if x < 200:
            return (True, LEFT)
        if (x > 200 and x < 400):
            return (True, FORWARD)

    return (False, direction)

#Looks for an enemy and attacks him if found
def attack(chat_id):
    
    global camera
    camera.release()
    camera = cv2.VideoCapture(0)
    camera.set(3,600)
    
    ATTACK_DISTANCE = 0.2
    TIME_TO_DROP_ATTACK = 5.0
    isNeckLow = False
    isLastRight = False

    bot.sendMessage(chat_id, "Looking...")
    
    #Looks around to see if it manages to find an enemy
    searchTime = time.time()
    while time.time() < searchTime + 10:
        (grabbed, frame)    = camera.read()
        (enemy_in_sight, _) = checkEnemy(frame)
        right()

        #Enemy found!
        if enemy_in_sight:
            lastTimeEnemyWasSeen = time.time()
            changeEmotion(EMOTION_ATTACKING, chat_id)
            break

    #If 10 seconds go by and no enemy is found, drop search
    if not enemy_in_sight:
        bot.sendMessage(chat_id, "No enemy found :(")
        return


    #Attacking state (in final code is inside the big while)
    while True:

        #Checks if an attack was successful
        is_touching = is_color(signal_targ, COLOR_RED)
        if is_touching:
            changeEmotion(EMOTION_EATING, chat_id)
            bot.sendMessage(chat_id,"Attack successful!")
            return

        (grabbed, frame)  = camera.read()
        (enemy_in_sight, cnts)    = checkEnemy(frame)

        ### Check if enemy is still in sight
        if enemy_in_sight:
            lastTimeEnemyWasSeen = time.time()



        ### Attack not yet performed
        if (not isNeckLow):
            distFront = computeDistance(ULTRA_ECHO_FRONT)

            ###### Enemy can be attacked
            if (distFront <= ATTACK_DISTANCE):
                stop()
                lowerNeck()
                isNeckLow = True

            ###### Enemy needs to be approached
            else:
                isLastRight = checkEnemyDirection(cnts, isLastRight, enemy_in_sight)



        ### Attack performed unsuccessfully
        else:
            raiseNeck()
            isNeckLow = False

            ### Drop attack
        if time.time() > lastTimeEnemyWasSeen + TIME_TO_DROP_ATTACK:
            #state = WALKING
            changeEmotion(EMOTION_NORMAL, chat_id)
            bot.sendMessage(chat_id, "Attack failed :(")
            break

 #This version implements the merged function checkEnemyComplete
def attackComplete(chat_id):
    
    global camera
    camera.release()
    camera = cv2.VideoCapture(0)
    camera.set(3,600)
    
    ATTACK_DISTANCE = 0.2
    TIME_TO_DROP_ATTACK = 5.0

    RIGHT = 0
    FORWARD = 1
    LEFT = 2

    isNeckLow = False
    direction = FORWARD

    #Looks around to see if it manages to find an enemy
    searchTime = time.time()
    bot.sendMessage(chat_id, "Looking...")
    while time.time() < searchTime + 10:
        (grabbed, frame)  = camera.read()
        (enemy_in_sight, direction)    = checkEnemyComplete(frame, direction)
        right()

        #Enemy found!
        if enemy_in_sight:
            lastTimeEnemyWasSeen = time.time()
            changeEmotion(EMOTION_ATTACKING, chat_id)
            break

    #If 10 seconds go by and no enemy is found, drop search
    if not enemy_in_sight:
        bot.sendMessage(chat_id, "No enemy found :(")
        return

    #Attacking state (in final code is inside the big while)
    while True:

        #Checks if an attack was successful
        is_touching = is_color(signal_targ, COLOR_RED)
        if is_touching:
            changeEmotion(EMOTION_EATING, chat_id)
            bot.sendMessage(chat_id,"Attack successful!")
            return

        (grabbed, frame)  = camera.read()
        (enemy_in_sight, direction)    = checkEnemyComplete(frame, direction)

        ### Check if enemy is still in sight
        if enemy_in_sight:
            lastTimeEnemyWasSeen = time.time()

        #Change direction according to the camera
        if direction == FORWARD:
            forward()
        if direction == RIGHT:
            right()
        if direction == LEFT:
            left()

        ### Attack not yet performed
        if (not isNeckLow):
            distFront = computeDistance(ULTRA_ECHO_FRONT)

            ###### Enemy can be attacked
            if (distFront <= ATTACK_DISTANCE):
                stop()
                lowerNeck()
                isNeckLow = True


        ### Attack performed unsuccessfully
        else:
            raiseNeck()
            isNeckLow = False

        ### Drop attack
        if time.time() > lastTimeEnemyWasSeen + TIME_TO_DROP_ATTACK:
            state = WALKING
            changeEmotion(EMOTION_NORMAL, chat_id)
            bot.sendMessage(chat_id, "Attack failed :(")
            break


#Checks whether the robot is parallel to the wall on its left (with a tolerance of 5%)
def isParallel():
    distBackLeft = computeDistance(ULTRA_ECHO_LEFT_BACK)
    time.sleep(0.01)
    distFrontLeft = computeDistance(ULTRA_ECHO_LEFT_FRONT)

    tolerance = 0.05 * (distBackLeft + distFrontLeft)/2
    return (abs(distBackLeft - distFrontLeft) < tolerance)



#Checks the distance from the wall at its left and corrects trajectory accordingly
def adjustParallel(chat_id):
    distBackLeft = computeDistance(ULTRA_ECHO_LEFT_BACK)
    distFrontLeft = computeDistance(ULTRA_ECHO_LEFT_FRONT)
    TIME_TO_SMOOTH_ROTATE = 0.4

    difference = distFrontLeft - distBackLeft
    if (difference > 0.30):
        left()
        time.sleep(TIME_TO_SMOOTH_ROTATE*3)
        bot.sendMessage(chat_id, str("wrongLeft"))
    elif (difference > 0.08):
        left()
        time.sleep(TIME_TO_SMOOTH_ROTATE*2)
        bot.sendMessage(chat_id, str("left"))
    elif (difference > 0.03):
        left()
        time.sleep(TIME_TO_SMOOTH_ROTATE)
        bot.sendMessage(chat_id, str("smoothLeft"))
    elif (difference < -0.30):
        right()
        time.sleep(TIME_TO_SMOOTH_ROTATE*4)
        bot.sendMessage(chat_id, str("wrongRight"))
    elif (difference < -0.08):
        right()
        time.sleep(TIME_TO_SMOOTH_ROTATE*2)
        bot.sendMessage(chat_id, str("right"))
    elif (difference < -0.03):
        right()
        time.sleep(TIME_TO_SMOOTH_ROTATE)
        bot.sendMessage(chat_id, str("smoothRight"))
    else:
        bot.sendMessage(chat_id, str("nothing to do"))
        return
    stop()
    #a discrepancy of 0.003m is tollerated



#Plays the music contained in file_name
def playMusic(file_name):
    global omxprocess
    global omxprocess_started
    if omxprocess_started:
        omxprocess.stdin.write(b'q')
    omxprocess = subprocess.Popen(['omxplayer', MusicDirectory + file_name, '--loop'],  stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)
    omxprocess_started = True

def stopMusic():
    global omxprocess
    global omxprocess_started
    if omxprocess_started:
        omxprocess.stdin.write(b'q')
    omxprocess_started = False

#Make sure that opening and closing of the spines happens correctly
def openSpines(spinesOpenedAt, spinesClosedAt):

    now = time.time()

    #It completed any previous closing, so we can proceed to start opening the spines
    if(spinesClosedAt > spinesOpenedAt and now - spinesClosedAt > 0.5):
        spines_pwm.stop()
        GPIO.output(IN1_SPINES,False)
        GPIO.output(IN2_SPINES,True)
        return (now, spinesClosedAt)


    #It already completed any opening
    if(spinesClosedAt < spinesOpenedAt and now - spinesOpenedAt > 0.5):
        spines_pwm.stop()

    return (spinesOpenedAt, spinesClosedAt)

def closeSpines(spinesOpenedAt, spinesClosedAt):

    now = time.time()

    #It completed any previous opening, so we can proceed to start closing the spines
    if(spinesOpenedAt > spinesClosedAt and now - spinesOpenedAt > 0.5):
        spines_pwm.stop()
        GPIO.output(IN1_SPINES,True)
        GPIO.output(IN2_SPINES,False)
        return (spinesOpenedAt, now)

    #It already completed any closing
    if(spinesOpenedAt < spinesClosedAt and now - spinesClosedAt > 0.5):
        spines_pwm.stop()

    return (spinesOpenedAt, spinesClosedAt)


#Waits for commands from telegram
#If we make the start a separate thread, this could become more complicated
def wait_msg(msg):
    global camera
    global current_emotion
    chat_id = msg['chat']['id']
    command_text = msg['text'].split(" ")
    command = command_text[0]

    spinesOpenedAt = 0.0
    spinesClosedAt = 0.1

    if command == '/help':
        bot.sendMessage(chat_id,
"/setup - Used to calibrate the sensors\n\
/photo - Sends a picture\n\n\
---------------------> SENSORS <------------------------\n\
/pond - Checks if on pond\n\
/eating - Checks if eating\n\
/calibrate - Calibrates the color sensors\n\
/eaten - Checks if eaten\n\
/ultra - Returns distance from ultrasonic sensors\n\n\
---------------------> MOTORS <-------------------------\n\
/moveTarget - Moves the target of 90°\n\
/moveSpines - Moves the spines for 2s\n\
/openSpines - Opens the spines\n\
/closeSpines - Closes the spined\n\
/neck - Lowers and then raises the neck\n\
/moveForward - Moves forward for 1.5 s\n\
/moveRight - Moves right 90°\n\
/moveLeft - Moves left 90°\n\
/moveBackward - Moves backward for 1.5 s\n\
/rotate90 - used to calibrate TIME_TO_ROTATE_90\n\
/rotate135 - used to calibrate TIME_TO_ROTATE_135\n\
/stop - Stops the robot\n\n\
---------------------> EMOTIONS <-------------------------\n\
/em1 - Normal emotions\n\
/em2 - Attacking emotions\n\
/em3 - Drinking emotions\n\
/em4 - Sleeping emotions\n\
/em5 - Defending emotions\n\n\
---------------------> FUNCTIONS <-------------------------\n\
/playMusic - plays some music\n\
/stopMusic - stops playing music \n\
/checkEnemy - checks if an enemy is in sight\n\
/attack - looks around for enemies and attacks them if found\n\
/attackAlternative - alternative code for attacking\n\
/IP - returns the IP address of the robot\n\
/controls - Simplified controls\n\
/exit - turns off the robot\n\
")

    if command == '/controls':
        bot.sendMessage(chat_id,
"/go - go forwards\n\
/back - go backwards\n\
/left - rotate left\n\
/right - rotate right\n\
/stop - stop moving\n\
")

    if command == '/photo':
        (grabbed, frame) = camera.read()
        cv2.imwrite('photo.jpg',frame)
        camera.release()
        camera = cv2.VideoCapture(0)
        camera.set(3,600)
        bot.sendPhoto(chat_id, photo = open('photo.jpg','rb'))

    if command == '/calibrate':
        bot.sendMessage(chat_id, "Blue treshold is now: {0}\n\
            Red treshold is now: {1}\n\
            Proceeding to calibration".format(blue_treshold, red_treshold))
        calibrate(chat_id)
    if command == '/pond':
        result = is_color(signal_pond, COLOR_BLUE)
        bot.sendMessage(chat_id, str(result))
    if command == '/eating':
        result = is_color(signal_targ, COLOR_RED)
        bot.sendMessage(chat_id, str(result))

    if command == '/eaten':
        result = checkTarget()
        bot.sendMessage(chat_id, str(result))

    if command == '/moveForward':
        forward()
        time.sleep(1.5)
        stop()
    if command == '/moveRight':
        right()
        time.sleep(2.8)
        stop()
    if command == '/moveLeft':
        left()
        time.sleep(2.6)
        stop()
    if command == '/moveBackward':
        backward()
        time.sleep(1.5)
        stop()

    if command == '/go':
        forward()
    if command == '/back':
        backward()
    if command == '/left':
        left()
    if command == '/right':
        right()
    if command == '/stop':
        stop()

    if command == '/ultra':
        distLeftFront = computeDistance(ULTRA_ECHO_LEFT_FRONT)*100
        time.sleep(0.03)
        distLeftBack  = computeDistance(ULTRA_ECHO_LEFT_BACK)*100
        distRight     = computeDistance(ULTRA_ECHO_RIGHT)*100
        distFront     = computeDistance(ULTRA_ECHO_FRONT)*100
        distBack      = computeDistance(ULTRA_ECHO_BACK)*100
        bot.sendMessage(chat_id, "Front: {0} cm\nBack: {1} cm\nRight: {2} cm\nLeft Front: {3} cm\nLeft Back: {4} cm".format(distFront,distBack,distRight,distLeftFront,distLeftBack))

    if command == '/calibrateUltra':
        global offset
        offset = 0
        i = 0
        diff = []

        bot.sendMessage(chat_id, "Place the robot with its left side parallel to a smooth wall distant 30cm\n\
You have 10seconds before the calibration begins")
        time.sleep(10)
        bot.sendMessage(chat_id, "Calibrating .....")
        while (i < 5):
            diff.append(calibrateUltra(50, chat_id))
            i += 1
        i = 0
        time.sleep(1)
        offset = sum(diff)/500
        bot.sendMessage(chat_id, "Calibration succesfull!\nDifference: {0} cm".format(diff))
        bot.sendMessage(chat_id, "New offset: {0} cm".format(offset*100))

    if command == '/moveTarget':
        target_pwm.start(70.0)
        GPIO.output(IN1_TARGET,True)
        GPIO.output(IN2_TARGET,False)
        time.sleep(0.20)
        target_pwm.stop()

    if command == '/moveSpines':
        spines_pwm.start(50.0)
        GPIO.output(IN1_SPINES,True)
        GPIO.output(IN2_SPINES,False)
        time.sleep(2)
        spines_pwm.stop()
    if command == '/closeSpines':
        (spinesOpenedAt, spinesClosedAt) = closeSpines(spinesOpenedAt, spinesClosedAt)
    if command == '/openSpines':
        (spinesOpenedAt, spinesClosedAt) = openSpines(spinesOpenedAt, spinesClosedAt)

    if command == '/neck':
        lowerNeck()
        time.sleep(2)
        raiseNeck()

    if command == '/em1':
        changeEmotion(EMOTION_NORMAL, chat_id)
    if command == '/em2':
        changeEmotion(EMOTION_ATTACKING, chat_id)
    if command == '/em3':
        changeEmotion(EMOTION_DRINKING, chat_id)
    if command == '/em4':
        changeEmotion(EMOTION_SLEEP, chat_id)
    if command == '/em5':
        changeEmotion(EMOTION_EATEN, chat_id)

    if command == '/isParallel':
        result = isParallel()
        bot.sendMessage(chat_id, str(result))
    if command == '/adjustParallel':
        adjustParallel(chat_id)

    if command == '/playMusic':
        if len(command_text) > 1:
            args = command_text[1]
        else:
            args = "Normal.mp3"
        playMusic(args)
    if command == '/stopMusic':
        stopMusic()

    if command == '/checkEnemy':
        (grabbed, frame) = camera.read()
        (isEnemy, _) = checkEnemy(frame)
        bot.sendMessage(chat_id, "{0}".format(str(isEnemy)))

    if command == '/attack':
        attack(chat_id)
        bot.sendMessage(chat_id, "Attack terminated")

    if command == '/attackVersion2':
        attackComplete(chat_id)
        bot.sendMessage(chat_id, "Attack terminated")

    if command == '/IP':
        cli_command = "hostname -I"
        proc = subprocess.Popen(cli_command, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE)
        line = proc.stdout.readLine()
        address = line.rstrip().decode("utf-8")
        bot.sendMessage(chat_id, address)

    if command == '/exit':
        bot.sendMessage(chat_id, "Bye!\nRemember to switch off the motors, turn off the speaker and unplug the powerbank")
        stop()
        stopMusic()
        sys.exit()
    
    if command == '/rotate90':
        bot.sendMessage(chat_id, "Right-rotating 90° with time.sleep({0})".format(TIME_TO_ROTATE_90))
        right()
        time.sleep(TIME_TO_ROTATE_90)
        stop()
    
    if command == '/rotate135':
        bot.sendMessage(chat_id, "Right-rotating 135° with time.sleep({0})".format(TIME_TO_ROTATE_135))
        right()
        time.sleep(TIME_TO_ROTATE_135)
        stop()
    



#Thread of the emotions
emotionsHandler = threading.Thread(target=emotionsHandlerTh, args=())
emotionsHandler.start()

if __name__ == '__main__':

    print("Activating bot!")

    bot = telepot.Bot(token)
    print("Bot activated!")
    bot.message_loop(wait_msg)
    while 1:
        time.sleep(10)
