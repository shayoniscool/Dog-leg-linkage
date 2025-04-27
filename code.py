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
pulse_In = pulseio.PulseIn(board.GP6, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# 0,1,2,3,...,9,*,#,left,up,right,down,ok
codes = [(0, 255, 74, 181),
    (0, 255, 104, 151),
    (0, 255, 152, 103),
    (0, 255, 176, 79),
    (0, 255, 48, 207),
    (0, 255, 24, 231),
    (0, 255, 122, 133),
    (0, 255, 16, 239),
    (0, 255, 56, 199),
    (0, 255, 90, 165),
    (0, 255, 66, 189),
    (0, 255, 82, 173),
    (0, 255, 34, 221),
    (0, 255, 98, 157),
    (0, 255, 194, 61),
    (0, 255, 168, 87),
    (0, 255, 2, 253)]

print("Waiting for RC...")
digit = -100
while digit < 0:
    pulses = decoder.read_pulses(pulse_In)
    try :
      code = decoder.decode_bits(pulses)
      digit = codes.index(code)
      print("digit = %d"%digit)
    except :
      pass

#makes an object that contains many parameters used above
left_Leg = Leg(Constants.LEFT_THIGH_PIN, Constants.LEFT_HIP_PIN,Constants.RIGHT_HIP_EXTENDED,Constants.RIGHT_HIP_CONTRACTED,Constants.RIGHT_THIGH_EXTENDED,Constants.RIGHT_THIGH_CONTRACTED,kit)
right_Leg = Leg(Constants.RIGHT_THIGH_PIN, Constants.RIGHT_HIP_PIN,Constants.LEFT_HIP_EXTENDED,Constants.LEFT_HIP_CONTRACTED,Constants.LEFT_THIGH_EXTENDED,Constants.LEFT_THIGH_CONTRACTED,kit)

left_Leg.hip_A *= 0.5
right_Leg.hip_A *= 0.5

if digit % 2 == 0:#even
    '''Walk cycle'''
    print("walk")
    left_Leg.hip_A *= 0.5
    right_Leg.hip_A *= 0.5
    left_Leg.thigh_A *= 0.5
    right_Leg.thigh_A *= 0.5
    left_Leg.hip_S+=20
    right_Leg.hip_S-=20
    left_Leg.start(0)
    right_Leg.start(math.pi)
else:
    print("trot")
    left_Leg.hip_A *= 0.5
    right_Leg.hip_A *= 0.5
    left_Leg.thigh_A *= 1
    right_Leg.thigh_A *= 1
    left_Leg.hip_S+=20
    right_Leg.hip_S-=20
    left_Leg.start(0)
    right_Leg.start(math.pi)

if digit==0 or digit==1:
    max_Speed = 12
elif digit==2 or digit==3 :
    max_Speed = 14
elif digit==4 or digit==5:
    max_Speed = 16
elif digit==6 or digit==7:
    max_Speed = 18
elif digit==8 or digit==9:
    max_Speed = 20

print("max_Speed = %g"%max_Speed)

speed=0
while True: #forever
    left_Leg.move(speed*Constants.DELTA_T) #move the left leg
    right_Leg.move(speed*Constants.DELTA_T)  #move the right leg
    if speed < max_Speed:
        speed += 0.1 #increase speed; accelerate until max speed is reached
    #time.sleep(Constants.DELTA_T)
