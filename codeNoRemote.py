import pulseio
import board
import adafruit_irremote
import busio
import math
import Constants
from adafruit_servokit import ServoKit
import time
from Leg import Leg

#configure the board
#get everything special
i2c = busio.I2C(board.GP1, board.GP0)
kit = ServoKit(channels=16, i2c=i2c)


#makes an object that contains many parameters used above
leftLeg = Leg(Constants.left_Leg_Pin, Constants.left_Hip_Pin,Constants.rHipExt,Constants.rHipCon,Constants.rThExt,Constants.rThCon,kit)
rightLeg = Leg(Constants.right_Leg_Pin, Constants.right_Hip_Pin,Constants.lHipExt,Constants.lHipCon,Constants.lThExt,Constants.lThCon,kit)

'''FlyingTrot cycle'''
leftLeg.hipA *= 0.5
rightLeg.hipA *= 0.5
leftLeg.thighA *= 1
rightLeg.thighA *= 1
speed = 0
max_Speed = 18
leftLeg.hipS+=20
rightLeg.hipS-=20
leftLeg.start(0)
rightLeg.start(math.pi)

while True: #forever
    leftLeg.move(speed*Constants.delta_t) #move the left leg
    rightLeg.move(speed*Constants.delta_t)  #move the right leg
    if speed < max_Speed:
        speed += 0.1 #increase speed; accelerate until max speed is reached
    #time.sleep(Constants.delta_t)
