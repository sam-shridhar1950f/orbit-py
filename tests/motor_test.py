from RpiMotorLib import RpiMotorLib
import RPi.GPIO as GPIO
print("r")
#stepper motor example code
direction_r = 5 # Direction (DIR) GPIO Pin
step_r = 12 # Step GPIO Pin
# EN_pin_r = 24 # enable pin (LOW to enable)
direction_m = 26  # Direction (DIR) GPIO Pin
step_m = 13 # Step GPIO Pin
CLOCKWISE = True

rotate_motor = RpiMotorLib.A4988Nema(direction_r, step_r, (21, 21, 21), "DRV8825")
magnet_motor = RpiMotorLib.A4988Nema(direction_m, step_m, (21, 21, 21), "DRV8825")


#magnet_motor.motor_go(not CLOCKWISE, 'Full', 200, 0.001, False, 0)

#rotate_motor.motor_go(not CLOCKWISE, 'Full', 200, 0.001, False, 0)

for i in range(200):
    rotate_motor.motor_go(not CLOCKWISE, 'Full', 1, 0, False, 0.001)
    magnet_motor.motor_go(not CLOCKWISE, 'Full', 1, 0, False, 0.001)
