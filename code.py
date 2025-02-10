import board
import busio
import math
import Constants
from adafruit_servokit import ServoKit
import time
#get everything special
i2c = busio.I2C(board.GP1, board.GP0)
kit = ServoKit(channels=16, i2c=i2c)
#configure the board

rHipExt = 10
rHipCon = 90
rThExt = 90
rThCon = 0
#right leg min and max angles

lHipExt = 80
lHipCon = 0
lThExt = 0
lThCon = 90
#left leg min and max angles

offset = math.pi # alternate
#offset = math.pi/2 # together

class Leg:
    def __init__(self, thighPin, hipPin, legOffset, hipExtendedAngle, hipContractedAngle,
        thighExtendedAngle, thighContractedAngle):

        self.legOffset = legOffset
        self.shift = math.pi/2

        self.hipS=(hipExtendedAngle+hipContractedAngle)/2
        self.hipA=(hipExtendedAngle-hipContractedAngle)/2

        self.thighS=(thighExtendedAngle+thighContractedAngle)/2
        self.thighA=(thighExtendedAngle-thighContractedAngle)/2

        #config thigh motor
        self.thigh_Motor = kit.servo[thighPin]
        self.thigh_Motor.set_pulse_width_range(
            Constants.KST_Pulse_Width_Min, Constants.KST_Pulse_Width_Max
        )
        self.thigh_Motor.frequency = Constants.KST_Frequency
        self.thigh_Motor.actuation_range = Constants.leg_actuation_range


        #config hip motor
        self.hip_Motor = kit.servo[hipPin]
        self.hip_Motor.set_pulse_width_range(
            Constants.KST_Pulse_Width_Min, Constants.KST_Pulse_Width_Max
        )
        self.hip_Motor.frequency = Constants.KST_Frequency
        self.hip_Motor.actuation_range = Constants.hip_actuation_range

        self.hip_Phase = 0
        self.thigh_Phase = 0

    def move(self, delta_t): #loop of time (delta_t)
        self.hip_Phase += delta_t
        self.thigh_Phase += delta_t

        #reset back to start of loop if time is at the end of cycle -> limit large numbers in calculations
        if self.hip_Phase > 2*math.pi:
            self.hip_Phase -= 2*math.pi

        #same as above for the thigh motors
        if self.thigh_Phase > 2*math.pi:
            self.thigh_Phase -= 2*math.pi

        #set the angles of the servos to follow cosine waves based on the parameters set above
        self.hip_Motor.angle = self.hipS + self.hipA*math.cos(self.hip_Phase)
        self.thigh_Motor.angle = self.thighS + self.thighA*math.cos(self.thigh_Phase)

    #startup sequence to start a gait, move legs into position
    def start(self, hip_Phase):
        self.hip_Phase = hip_Phase
        self.thigh_Phase = hip_Phase - self.shift
        self.hip_Motor.angle = self.hipS + self.hipA*math.cos(self.hip_Phase)
        self.thigh_Motor.angle = self.thighS + self.thighA*math.cos(self.thigh_Phase)

#makes an object that contains many parameters used above
leftLeg = Leg(Constants.left_Leg_Pin, Constants.left_Hip_Pin, 0,rHipExt,rHipCon,rThExt,rThCon)
rightLeg = Leg(Constants.right_Leg_Pin, Constants.right_Hip_Pin, offset, lHipExt,lHipCon,lThExt,lThCon)


leftLeg.hipA *= 0.5
rightLeg.hipA *= 0.5
leftLeg.thighA *= 0.5
rightLeg.thighA *= 0.5

speed = 0
max_Speed = 12
#start with low speed
leftLeg.start(0)
rightLeg.start(math.pi) #offset by half cycle, so legs will move opposite each other

while True: #forever
    leftLeg.move(speed*Constants.delta_t) #move the left leg
    rightLeg.move(speed*Constants.delta_t)  #move the right leg
    if speed < max_Speed:
        speed += 0.1 #increase speed; accelerate until max speed is reached
    #time.sleep(Constants.delta_t)
