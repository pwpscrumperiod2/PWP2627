#!/usr/bin/python

#imports the PWM driver for the motor board
from PCA9685 import PCA9685
import time

#the two directions a motor can spin
Dir = [
    'forward',
    'backward',
]
#connects to the PWM chip at I2C address 0x40 and sets it to 50Hz
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

#controls the two motors (A and B) on the motor driver board
class MotorDriver():
    def __init__(self):
        #PWM channels for each motor
        #PWMA/PWMB set the speed, IN1/IN2 set the direction
        #Motor A
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        #Motor B
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    #spins a motor (0 = A, 1 = B) in a direction at a speed from 0 to 100
    def MotorRun(self, motor, index, speed):
        #ignore invalid speeds
        if speed > 100:
            return
        if(motor == 0):
            #Motor A
            pwm.setDutycycle(self.PWMA, speed)
            if(index == Dir[0]):
                #forward
                print ("1")
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                #backward
                print ("2")
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            #Motor B
            pwm.setDutycycle(self.PWMB, speed)
            if(index == Dir[0]):
                #forward
                print ("3")
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                #backward
                print ("4")
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    #stops a motor (0 = A, 1 = B) by setting its speed and direction pins to 0
    def MotorStop(self, motor):
        if motor == 0:
            # Stop Motor A
            pwm.setDutycycle(self.PWMA, 0)
            pwm.setLevel(self.AIN1, 0)
            pwm.setLevel(self.AIN2, 0)

        elif motor == 1:
            # Stop Motor B
            pwm.setDutycycle(self.PWMB, 0)
            pwm.setLevel(self.BIN1, 0)
            pwm.setLevel(self.BIN2, 0)
