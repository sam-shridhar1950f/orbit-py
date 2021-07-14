import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from math import cos, pi

EARTH_E = 0.017 #eccentricities
EARTH_MASS = 5.97216787e+24 #kg
SUN_MASS = 1.989e+30 #kg
A = 18 * 2.54 / 100 #m
PERIOD = 45 #s
EARTH_A = 149.60e+9 #m
EARTH_PERIOD = 365 #days
PRESET = 'EARTH'
THETA = 0

ORBIT_STATUS = True #orbit status for turning on and off servo motor

G = 6.67408e-11

b_calc = lambda a, e: a*((1+e)*(1-e))**(1/2) # Derive b with a known a
distance_calc = lambda a, b, theta: ((a ** 2) - ((a ** 2 - b ** 2) ** (1 / 2)) ** (2)) / (a + ((a ** 2 - b ** 2) ** (1 / 2)) * (cos(theta)))
velocity_calc = lambda g, m, r, a: (g * m * ((2 / r) - (1 / a))) ** (1 / 2)
aphelion_calc = lambda a, e: a*(1+e)
perihelion_calc = lambda a, e: a*(1-e)
period_calc = lambda g, a, m: ((4 * pi**2 * a**3)/(g * m))**(1/2)

def earth_calc(period=PERIOD):
    sf = A / EARTH_A
    b = b_calc(A, EARTH_E) #m
    d = distance_calc(A, b, THETA) #m
    v = velocity_calc(G, (EARTH_MASS + SUN_MASS) * (sf) ** (3), d, A) #m/s
    v *= (EARTH_PERIOD * 24 * 60 * 60) / period
    w = v/d # maybe factor in height of planet
    print(f"Distance: {d}, Velocity: {v}, Angular Velocity: {w}")
    return d, v, w


#stepper motor example code
direction = 16 # Direction (DIR) GPIO Pin
step = 13 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
magnet_motor = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
STEPS_PER_REVOLUTION_R = 200
magnet_motor_steps = 0
rotate_motor_steps = 0
METERS_PER_STEP = 0.0011 # todo find actual value
CLOCKWISE = True

while True:
    if ORBIT_STATUS:
        d, v, w = -1, -1, -1
        if PRESET == 'EARTH':
            d, v, w = earth_calc()
        if d == -1:
            break
        print('distance', d)
        rotate_motor_steps += 1
        THETA = (2 * pi / STEPS_PER_REVOLUTION_R) * rotate_motor_steps
        #extension
        desired_steps = (int) (d / METERS_PER_STEP)
        print('desired steps:', desired_steps)
        print('current steps:', magnet_motor_steps)
        time_between_steps_m = 0.0005
        if desired_steps > magnet_motor_steps:
            magnet_motor.motor_go(not CLOCKWISE, 'Full', abs(desired_steps - magnet_motor_steps), max(0.0005, time_between_steps_m), False, max(0.0005, time_between_steps_m))
        elif desired_steps < magnet_motor_steps:
            magnet_motor.motor_go(CLOCKWISE, 'Full', abs(desired_steps - magnet_motor_steps), max(0.0005, time_between_steps_m), False, max(0.0005, time_between_steps_m))
        magnet_motor_steps = desired_steps
    else:
        magnet_motor.motor_stop()
        # GPIO.cleanup()
            
            