import math
import Constants
import time

class Leg:
    def __init__(self, thigh_Pin, hip_Pin, hip_Extended_Angle, hip_Contracted_Angle,
        thigh_Extended_Angle, thigh_Contracted_Angle,servo_Kit):

        self.servo_Kit=servo_Kit
        self.shift = math.pi/2

        self.hip_S=(hip_Extended_Angle+hip_Contracted_Angle)/2
        self.hip_A=(hip_Extended_Angle-hip_Contracted_Angle)/2

        self.thigh_S=(thigh_Extended_Angle+thigh_Contracted_Angle)/2
        self.thigh_A=(thigh_Extended_Angle-thigh_Contracted_Angle)/2

        #config thigh motor
        self.thigh_Motor = self.servo_Kit.servo[thigh_Pin]
        self.thigh_Motor.set_pulse_width_range(
            Constants.KST_PULSE_WIDTH_MIN, Constants.KST_PULSE_WIDTH_MAX
        )
        self.thigh_Motor.frequency = Constants.KST_FREQUENCY
        self.thigh_Motor.actuation_range = Constants.THIGH_ACTUATION_RANGE


        #config hip motor
        self.hip_Motor = self.servo_Kit.servo[hip_Pin]
        self.hip_Motor.set_pulse_width_range(
            Constants.KST_PULSE_WIDTH_MIN, Constants.KST_PULSE_WIDTH_MAX
        )
        self.hip_Motor.frequency = Constants.KST_FREQUENCY
        self.hip_Motor.actuation_range = Constants.HIP_ACTUATION_RANGE

        self.hip_Phase = 0
        self.thigh_Phase = 0

    def move(self, delta_T): #loop of time (delta_t)
        self.hip_Phase += delta_T
        self.thigh_Phase += delta_T

        #reset back to start of loop if time is at the end of cycle -> limit large numbers in calculations
        if self.hip_Phase > 2*math.pi:
            self.hip_Phase -= 2*math.pi

        #same as above for the thigh motors
        if self.thigh_Phase > 2*math.pi:
            self.thigh_Phase -= 2*math.pi

        #set the angles of the servos to follow cosine waves based on the parameters set above
        self.hip_Motor.angle = self.hip_S + self.hip_A*math.cos(self.hip_Phase)
        self.thigh_Motor.angle = self.thigh_S + self.thigh_A*math.cos(self.thigh_Phase)

    #startup sequence to start a gait, move legs into position
    def start(self, hip_Phase):
        self.hip_Phase = hip_Phase
        self.thigh_Phase = hip_Phase - self.shift
        self.hip_Motor.angle = self.hip_S + self.hip_A*math.cos(self.hip_Phase)
        self.thigh_Motor.angle = self.thigh_S + self.thigh_A*math.cos(self.thigh_Phase)
