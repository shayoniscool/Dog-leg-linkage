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
pulsein = pulseio.PulseIn(board.GP6, maxlen=120, idle_state=True)
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

digit = -100
while digit < 0:
    pulses = decoder.read_pulses(pulsein)
    try :
      code = decoder.decode_bits(pulses)
      digit = codes.index(code)
    except :
      pass

#makes an object that contains many parameters used above
leftLeg = Leg(Constants.left_Leg_Pin, Constants.left_Hip_Pin,Constants.rHipExt,Constants.rHipCon,Constants.rThExt,Constants.rThCon,kit)
rightLeg = Leg(Constants.right_Leg_Pin, Constants.right_Hip_Pin,Constants.lHipExt,Constants.lHipCon,Constants.lThExt,Constants.lThCon,kit)

leftLeg.hipA *= 0.5
rightLeg.hipA *= 0.5


if digit % 2 == 0:#even
    '''Walk cycle'''
    leftLeg.hipA *= 0.5
    rightLeg.hipA *= 0.5
    leftLeg.thighA *= 0.5
    rightLeg.thighA *= 0.5
    leftLeg.hipS+=20
    rightLeg.hipS-=20
    leftLeg.start(0)
    rightLeg.start(math.pi)
else:
    leftLeg.hipA *= 0.5
	rightLeg.hipA *= 0.5
	leftLeg.thighA *= 1
	rightLeg.thighA *= 1
	leftLeg.hipS+=20
	rightLeg.hipS-=20
	leftLeg.start(0)
	rightLeg.start(math.pi)

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

while True: #forever
    leftLeg.move(speed*Constants.delta_t) #move the left leg
    rightLeg.move(speed*Constants.delta_t)  #move the right leg
    if speed < max_Speed:
        speed += 0.1 #increase speed; accelerate until max speed is reached
    #time.sleep(Constants.delta_t)
