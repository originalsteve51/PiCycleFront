import time
from threading import Thread

import RPi.GPIO as GPIO

from cp_pins import *

class RGBController(object):

    __pwm_left_channel = None
    __pwm_right_channel = None
    __pwm_brake_channel = None

    def __init__(self):

        # Pulse-width modulation @ 50 Hz
        if RGBController.__pwm_left_channel is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pwm_channels, GPIO.OUT)
            RGBController.__pwm_left_channel = GPIO.PWM(LEFT_PWM_CHANNEL, 50)
            RGBController.__pwm_right_channel = GPIO.PWM(RIGHT_PWM_CHANNEL, 50)
            RGBController.__pwm_brake_channel = GPIO.PWM(BRAKE_PWM_CHANNEL, 50)

            # Fully dimmed to begin
            RGBController.__pwm_left_channel.start(0)
            RGBController.__pwm_right_channel.start(0)
            RGBController.__pwm_brake_channel.start(0)

    def turn_on(self, channel):
        duty_cycle = 100
        if (channel == 'w'):
            RGBController.__pwm_left_channel.ChangeDutyCycle(duty_cycle)
        if (channel == 'r'):
            RGBController.__pwm_right_channel.ChangeDutyCycle(duty_cycle)
        if (channel == 'g'):
            RGBController.__pwm_brake_channel.ChangeDutyCycle(duty_cycle)
        if (channel == 'b'):
            RGBController.__pwm_left_channel.ChangeDutyCycle(duty_cycle)
            RGBController.__pwm_right_channel.ChangeDutyCycle(duty_cycle)
            RGBController.__pwm_brake_channel.ChangeDutyCycle(duty_cycle)


    def turn_off(self, channel):
        duty_cycle = 0
        if (channel == 'w'):
            RGBController.__pwm_left_channel.ChangeDutyCycle(duty_cycle)
        if (channel == 'r'):
            RGBController.__pwm_right_channel.ChangeDutyCycle(duty_cycle)
        if (channel == 'g'):
            RGBController.__pwm_brake_channel.ChangeDutyCycle(duty_cycle)
        if (channel == 'b'):
            RGBController.__pwm_left_channel.ChangeDutyCycle(duty_cycle)
            RGBController.__pwm_right_channel.ChangeDutyCycle(duty_cycle)
            RGBController.__pwm_brake_channel.ChangeDutyCycle(duty_cycle)

    def go_dark(self):
        time_on = 0
        RGBController.__pwm_left_channel.ChangeDutyCycle(time_on)
        RGBController.__pwm_right_channel.ChangeDutyCycle(time_on)


    def close(self):
        RGBController.__pwm_left_channel.stop()
        RGBController.__pwm_right_channel.stop()


