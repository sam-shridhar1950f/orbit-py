from RpiMotorLib import RpiMotorLib
#stepper motor example code
direction= 16 # Direction (DIR) GPIO Pin
step = 13 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)
CLOCKWISE = True
rotate_motor = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")


#rotate_motor.motor_go(not CLOCKWISE, 'Full', 200, 0.0005, False, 0.005)

for x in range(0, 400):
   rotate_motor.motor_go(not CLOCKWISE, 'Full', 1, 0, False, 0.0005)