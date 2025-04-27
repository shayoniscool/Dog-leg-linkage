
#right leg min and max angles
RIGHT_HIP_EXTENDED = 10
RIGHT_HIP_CONTRACTED = 90
RIGHT_THIGH_EXTENDED = 90
RIGHT_THIGH_CONTRACTED = 0

#left leg min and max angles
LEFT_HIP_EXTENDED = 80
LEFT_HIP_CONTRACTED = 0
LEFT_THIGH_EXTENDED = 0
LEFT_THIGH_CONTRACTED = 90

#adafruit pin configuration
LEFT_THIGH_PIN=13
LEFT_HIP_PIN=12
RIGHT_THIGH_PIN=15
RIGHT_HIP_PIN=14

#motor constants

#feetech motor properties:

'''FEETECH_PULSE_WIDTH_MIN=420
FEETECH_PULLSE_WIDTH_MAX=2550
FEETECH_FREQUENCY=250'''

#KST motor properties
KST_PULSE_WIDTH_MIN=900
KST_PULSE_WIDTH_MAX=2100
KST_FREQUENCY=333

#offsets and movement data
DELTA_T=0.0015
HIP_OFFSET=0.5

#all leg offsets are based off of the left back leg.
RIGHT_THIGH_OFFSET=0.5#we don't use this?
THIGH_ACTUATION_RANGE=90
HIP_ACTUATION_RANGE=90

#decoder constants

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


