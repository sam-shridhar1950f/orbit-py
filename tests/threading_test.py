from RpiMotorLib import RpiMotorLib
import threading
#stepper motor example code
direction_r = 5 # Direction (DIR) GPIO Pin
step_r = 12 # Step GPIO Pin
# EN_pin_r = 24 # enable pin (LOW to enable)
direction_m = 26 # Direction (DIR) GPIO Pin
step_m = 13 # Step GPIO Pin
CLOCKWISE = True
print("v")
rotate_motor = RpiMotorLib.A4988Nema(direction_r, step_r, (21, 21, 21), "DRV8825")
magnet_motor = RpiMotorLib.A4988Nema(direction_m, step_m, (21, 21, 21), "DRV8825")

def turn_motor(motor, direction, type, steps, stepdelay,boolean,initdelay):
    motor.motor_go(direction, type, steps, stepdelay, boolean, initdelay)

def turn_rotate_motor():
    rotate_motor.motor_go(CLOCKWISE, 'Full', 800, 0.005, False, 0.001)
def turn_magnet_motor():
    magnet_motor.motor_go(not CLOCKWISE, 'Full', 100, 0.006, False, 0.001)
    magnet_motor.motor_go(CLOCKWISE, 'Full', 100, 0.003, False, 0.001)
    magnet_motor.motor_go(not CLOCKWISE, 'Full', 100, 0.006, False, 0.001)
    magnet_motor.motor_go(CLOCKWISE, 'Full', 100, 0.003, False, 0.001)
    magnet_motor.motor_go(not CLOCKWISE, 'Full', 100, 0.006, False, 0.001)
    magnet_motor.motor_go(CLOCKWISE, 'Full', 100, 0.003, False, 0.001)
    magnet_motor.motor_go(not CLOCKWISE, 'Full', 100, 0.006, False, 0.001)
    magnet_motor.motor_go(CLOCKWISE, 'Full', 100, 0.003, False, 0.001)

t1 = threading.Thread(target=turn_rotate_motor)
t2 = threading.Thread(target=turn_magnet_motor)

t1.start()
t2.start()
t1.join()
t2.join()

