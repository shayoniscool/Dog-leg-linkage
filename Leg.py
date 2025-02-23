import math
import Constants
import time

class Leg:
    def __init__(self, thighPin, hipPin, hipExtendedAngle, hipContractedAngle,
        thighExtendedAngle, thighContractedAngle,servoKit):
        self.servoKit=servoKit
        self.shift = math.pi/2

        self.hipS=(hipExtendedAngle+hipContractedAngle)/2
        self.hipA=(hipExtendedAngle-hipContractedAngle)/2

        self.thighS=(thighExtendedAngle+thighContractedAngle)/2
        self.thighA=(thighExtendedAngle-thighContractedAngle)/2

        #config thigh motor
        self.thigh_Motor = self.servoKit.servo[thighPin]
        self.thigh_Motor.set_pulse_width_range(
            Constants.KST_Pulse_Width_Min, Constants.KST_Pulse_Width_Max
        )
        self.thigh_Motor.frequency = Constants.KST_Frequency
        self.thigh_Motor.actuation_range = Constants.leg_actuation_range


        #config hip motor
        self.hip_Motor = self.servoKit.servo[hipPin]
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
        print(self.hipS + self.hipA*math.cos(self.hip_Phase))
        self.hip_Motor.angle = self.hipS + self.hipA*math.cos(self.hip_Phase)
        self.thigh_Motor.angle = self.thighS + self.thighA*math.cos(self.thigh_Phase)

    #startup sequence to start a gait, move legs into position
    def start(self, hip_Phase):
        self.hip_Phase = hip_Phase
        self.thigh_Phase = hip_Phase - self.shift
        self.hip_Motor.angle = self.hipS + self.hipA*math.cos(self.hip_Phase)
        self.thigh_Motor.angle = self.thighS + self.thighA*math.cos(self.thigh_Phase)
