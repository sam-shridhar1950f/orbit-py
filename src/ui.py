
from guizero import *
from math import cos, pi
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
from sys import exit
import threading

G = 6.67408e-11

EARTH_E = 0.017 #eccentricities
MOON_E = 0.0549 #relative to earth
MERCURY_E = 0.2056
EARTH_MASS = 5.97216787e+24 #kg
MOON_MASS = 7.34767309e+22 #kg
SUN_MASS = 1.989e+30 #kg
MERCURY_MASS = 3.285e+23 #kg
A = 18 * 2.54 / 100 #m todo make shorter to like 15
PERIOD = 45 #s
EARTH_A = 149.60e+9 #m
MOON_A = 384748000 #m
MERCURY_A = 57.909e+9 #m
EARTH_PERIOD = 365 #days
MOON_PERIOD = 28 #days
MERCURY_PERIOD = 88 #days
PRESET = None
THETA = 0

ORBIT_STATUS = False #orbit status for turning on and off servo motor

# Preset Functions
b_calc = lambda a, e: a*((1+e)*(1-e))**(1/2) # Derive b with a known a
distance_calc = lambda a, b, theta: ((a ** 2) - ((a ** 2 - b ** 2) ** (1 / 2)) ** (2)) / (a + ((a ** 2 - b ** 2) ** (1 / 2)) * (cos(theta)))
velocity_calc = lambda g, m, r, a: (g * m * ((2 / r) - (1 / a))) ** (1 / 2)
aphelion_calc = lambda a, e: a*(1+e)
perihelion_calc = lambda a, e: a*(1-e)
period_calc = lambda g, a, m: ((4 * pi**2 * a**3)/(g * m))**(1/2)


app = App(title='test')

message = Text(app, text='Orbit Simulator', size=20)

def earth_select():
    global PRESET
    global ORBIT_STATUS
    global THETA
    global rotate_motor_steps
    PRESET = 'EARTH'
    ORBIT_STATUS = True
    THETA, rotate_motor_steps = 0

def moon_select():
    global PRESET
    global ORBIT_STATUS
    global THETA
    global rotate_motor_steps
    PRESET = 'MOON'
    ORBIT_STATUS = True
    THETA, rotate_motor_steps = 0

def mercury_select():
    global PRESET
    global ORBIT_STATUS
    global THETA
    global rotate_motor_steps
    PRESET = 'MERCURY'
    ORBIT_STATUS = True
    THETA, rotate_motor_steps = 0

def stop_select():
    global PRESET
    global ORBIT_STATUS
    global THETA
    global rotate_motor_steps
    PRESET = None
    ORBIT_STATUS = False
    THETA, rotate_motor_steps = 0
    

def earth_calc(period=PERIOD):
    sf = A / EARTH_A
    b = b_calc(A, EARTH_E) #m
    d = distance_calc(A, b, THETA) #m
    v = velocity_calc(G, (EARTH_MASS + SUN_MASS) * (sf) ** (3), d, A) #m/s
    v *= (EARTH_PERIOD * 24 * 60 * 60) / period
    w = v/d # maybe factor in height of planet
    print(f"Distance: {d}, Velocity: {v}, Angular Velocity: {w}")
    return d, v, w

def moon_calc(period=PERIOD):
    sf = A / MOON_A
    b = b_calc(A, MOON_E)
    d = distance_calc(A, b, THETA)
    v = velocity_calc(G, (MOON_MASS + EARTH_MASS) * (sf) ** (3), d, A) #m/s
    v *= (MOON_PERIOD * 24 * 60 * 60) / period
    w = v/d
    print(f"Distance: {d}, Velocity: {v}, Angular Velocity: {w}")
    return d, v, w

def mercury_calc(period=PERIOD):
    sf = A / MERCURY_A
    b = b_calc(A, MERCURY_E)
    d = distance_calc(A, b, THETA)
    v = velocity_calc(G, (MERCURY_MASS + SUN_MASS) * (sf) ** (3), d, A)  # m/s
    v *= (MERCURY_PERIOD * 24 * 60 * 60) / period
    w = v / d
    print(f"Distance: {d}, Velocity: {v}, Angular Velocity: {w}")
    return d, v, w

def kill_select():
    exit()

def check(semimajor_axis, E):
    # Table Diameter: 48 Inches
    # calculate its aphelion and check if it exceeds 48 inches (relative to its starting position)
    aphelion = aphelion_calc(semimajor_axis, E)
    perihelion = perihelion_calc(semimajor_axis, E)
    return aphelion, perihelion
    
def end(issue):
    print(issue)
    time.sleep(3)
    exit()
    
def user_ellipse_select():
    global PRESET
    global ORBIT_STATUS
    global THETA
    global rotate_motor_steps
    PRESET = "USER_SELECT"
    THETA, rotate_motor_steps = 0
    ORBIT_STATUS = True
    d, v, w = user_ellipse_calc()
    if d == -1:
        ORBIT_STATUS = False


def user_ellipse_calc(period=PERIOD):
    global ORBIT_STATUS
    a = float(startBox.value) * 2.54 / 100  # semi-major axis in m
    # satellite_mass = float(satelliteBox.value)
    mainbody_mass = float(mainbodyBox.value)
    # Planetary_PERIOD = float(PlanetaryPeriodBox.value)
    E = float(eccentricityBox.value)
    b = b_calc(a, E)
    d = distance_calc(a, b, THETA)
    v = velocity_calc(G, mainbody_mass, d, a)
    p = period_calc(G, a, mainbody_mass)
    v *= p / period
    w = v / d

    aphelion, perihelion = check(a, E)

    if aphelion > 23 * 2.54 / 100 or perihelion < 0:  # 0 is an arbitrary value for now
        ORBIT_STATUS = False
        return -1, -1, -1
    else:
        return d, v, w  # returns distance, velocity, and angular velocity

earthPresetButton = PushButton(master=app, command=earth_select, text='Earth', align="left")
moonPresetButton = PushButton(master=app, command=moon_select, text='Moon', align="left")
mercuryPresetButton = PushButton(master=app, command=mercury_select, text='Mercury', align="left")
stopPresetButton = PushButton(master=app, command=stop_select, text='Stop', align='left')
killPresetButton = PushButton(master=app, command=kill_select, text='Kill', align='left')

# User Input Text Boxes
startBox = TextBox(master=app, text="Starting Position", align="left", width="fill")
# satelliteBox = TextBox(master=app, text="Satellite Mass", align="left",width="fill")
mainbodyBox = TextBox(master=app, text="Main Body Mass", align="left",width="fill")
# PlanetaryPeriodBox = TextBox(master=app, text="Period", align="left",width="fill")
eccentricityBox = TextBox(master=app, text="Eccentricity", align="left", width="fill")
userSubmit = PushButton(master=app, text="Submit", command=user_ellipse_select, align="left")


app.display()

#stepper motor example code
direction_r = 16 # Direction (DIR) GPIO Pin
step_r = 13 # Step GPIO Pin
EN_pin_r = 24 # enable pin (LOW to enable)
direction_m = 16 # Direction (DIR) GPIO Pin
step_m = 13 # Step GPIO Pin
EN_pin_m = 24 # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
rotation_motor = RpiMotorLib.A4988Nema(direction_r, step_r, (21, 21, 21), "DRV8825")
GPIO.setup(EN_pin_r, GPIO.OUT) # set enable pin as output (may not be necessary)
GPIO.setup(EN_pin_m, GPIO.OUT) # set enable pin as output (may not be necessary)
STEPS_PER_REVOLUTION_R = 800 # todo find actual value, may be 400
rotate_motor_steps = 0
magnet_motor = RpiMotorLib.A4988Nema(direction_m, step_m, (21, 21, 21), "DRV8825")
STEPS_PER_REVOLUTION_M = 200
magnet_motor_steps = 0
METERS_PER_STEP = 0.0011 # todo find actual value
CLOCKWISE = True # todo find actual value (change to false if spinning wrong direction)

#Possible fail points
#1. Inaccurate steps (loop causes motor to spin only half as much)
#Possible fix: test experimentally and check if taking 2 steps at a time makes a difference
#2. Spinning is choppy
#Possible fix: have constant speed (last resort)

def turn_motor(motor, direction, type, steps, stepdelay, initdelay):
    motor.motor_go(direction, type, steps, stepdelay, initdelay)

def turn_rotate_motor():
    global THETA
    global rotate_motor_steps
    # d, v, w = -1
    # if PRESET == 'EARTH':
    #     d, v, w = earth_calc()
    # if PRESET == 'MOON':
    #     d, v, w = moon_calc()
    # if PRESET == 'MERCURY':
    #     d, v, w = mercury_calc()
    # if PRESET == "USER_SELECT":
    #     d, v, w = user_ellipse_calc()
    # time_between_steps_r = 2 * pi / w / STEPS_PER_REVOLUTION_R
    time_between_steps_r = 0.01
    while True:
        rotation_motor.motor_go(not CLOCKWISE, 'Full', STEPS_PER_REVOLUTION_R, time_between_steps_r, False, 0.001)
        rotate_motor_steps += 1
        THETA = (2 * pi / STEPS_PER_REVOLUTION_R) * rotate_motor_steps

def turn_magnet_motor():
    global magnet_motor_steps
    while True:
        d, v, w = -1
        if PRESET == 'EARTH':
            d, v, w = earth_calc()
        if PRESET == 'MOON':
            d, v, w = moon_calc()
        if PRESET == 'MERCURY':
            d, v, w = mercury_calc()
        if PRESET == "USER_SELECT":
            d, v, w = user_ellipse_calc()
        desired_steps = (int)(d / METERS_PER_STEP)
        time_between_steps_m = 0.01
        if desired_steps > magnet_motor_steps:
            magnet_motor.motor_go(not CLOCKWISE, 'Full', abs(desired_steps - magnet_motor_steps) + 1, #may need to change to - 1
                                      time_between_steps_m, False, 0.001)
        elif desired_steps < magnet_motor_steps:
            magnet_motor.motor_go(CLOCKWISE, 'Full', abs(desired_steps - magnet_motor_steps) - 1, #may need to change to + 1
                                            time_between_steps_m, False, 0.001)
        magnet_motor_steps = desired_steps

while True:
    if ORBIT_STATUS:
        t1 = threading.Thread(target=turn_rotate_motor)
        t2 = threading.Thread(target=turn_magnet_motor)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        rotation_motor.motor_stop()
        magnet_motor.motor_stop()
        # GPIO.cleanup()