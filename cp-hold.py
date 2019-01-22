import RPi.GPIO as GPIO
import time
from threading import Thread

from cp_pins import *
from signalcontroller import *

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


import rgbcontroller

MQTT_SERVER = 'pithreedev.local'
MQTT_SYNC_PATH = 'synchronize'
MQTT_CMD_PATH = "commands"


RIGHT_SIGNAL = 'r'
RECORD_SIGNAL = 'g'
LEFT_SIGNAL = 'w'
WARNING_SIGNAL = 'b'

def on_connect(client, userdata, flags, rc):
    print('SyncProcessor connected with rc = ', rc, ' Ready to receive sync messages.')
    client.subscribe(MQTT_SYNC_PATH)

def on_message(client, userdata, msg):
    # print (msg.topic,': '+str(msg.payload))
    if msg.payload == b'on:r':
        rgb.turn_on(RIGHT_SIGNAL)
        sig_ctl.arrow('right', 'on')
    if msg.payload == b'on:l':
        rgb.turn_on(LEFT_SIGNAL)
        sig_ctl.arrow('left', 'on')
    if msg.payload == b'off:r':
        rgb.turn_off(RIGHT_SIGNAL)
        sig_ctl.arrow('right', 'off')
    if msg.payload == b'off:l':
        rgb.turn_off(LEFT_SIGNAL)
        sig_ctl.arrow('left', 'off')
    if msg.payload == b'stop:both':
        rgb.turn_off(RIGHT_SIGNAL)
        rgb.turn_off(LEFT_SIGNAL)
        sig_ctl.arrow('right', 'off')
        sig_ctl.arrow('left', 'off')
    if msg.payload == b'start-recording':
        GPIO.output(PING_ACK_LED, GPIO.HIGH)
        # rgb.turn_on(RECORD_SIGNAL)
    if msg.payload == b'stop-recording':
        GPIO.output(PING_ACK_LED, GPIO.LOW)
        # rgb.turn_off(RECORD_SIGNAL)
    """
    if msg.payload == b'ping:ack':
        GPIO.output(PING_ACK_LED, GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(PING_ACK_LED, GPIO.LOW)
    """

    if msg.payload == b'warning:ack':
        # flash ping leds for 2 seconds
        warningThread = Thread(target=show_warning)
        warningThread.start()


def syncprocessor():
    client = mqtt.Client('syncprocessor')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()

def show_warning():
    rgb = rgbcontroller.RGBController()
    for counter in range(0, 10):
        counter += 1
        rgb.turn_on(WARNING_SIGNAL)
        time.sleep(1)
        rgb.turn_off(WARNING_SIGNAL)
    publish.single(MQTT_CMD_PATH, 'warning:off', hostname=MQTT_SERVER)



# main execution block starts here
if __name__ == '__main__':

    def ping_mqtt_server():
        while True:
            publish.single(MQTT_CMD_PATH, 'ping', hostname=MQTT_SERVER)
            GPIO.output(PING_OUT_LED, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(PING_OUT_LED, GPIO.LOW)
            time.sleep(1.98)

    def process_record_requests():
        while True:
            cmd = None
            if GPIO.input(RECORD_SIGNAL_PIN) == 1:
                cmd = 'record'
            if cmd is not None:
                print(cmd)
                publish.single(MQTT_CMD_PATH, cmd, hostname=MQTT_SERVER)
                if cmd == 'record':
                    while GPIO.input(RECORD_SIGNAL_PIN) == 1:
                        pass
                    cmd = 'record-off'
                print(cmd)
                publish.single(MQTT_CMD_PATH, cmd, hostname=MQTT_SERVER)

            time.sleep(0.2)

    def process_warning_requests():
        while True:
            if GPIO.input(WARNING_PIN) == 1:
                publish.single(MQTT_CMD_PATH, 'warning', hostname=MQTT_SERVER)
            time.sleep(0.2)

    try:

        rgb = rgbcontroller.RGBController()
        sig_ctl = SignalController()

        GPIO.setmode(GPIO.BCM)

        # prepare switch input pins for use
        GPIO.setup(RIGHT_SIGNAL_PIN, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(RECORD_SIGNAL_PIN, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(LEFT_SIGNAL_PIN, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(WARNING_PIN, GPIO.IN, GPIO.PUD_DOWN)

        # prepare to send out pings and to receive ping acks
        GPIO.setup([PING_OUT_LED, PING_ACK_LED], GPIO.OUT)
        GPIO.output([PING_OUT_LED, PING_ACK_LED], GPIO.LOW)


        syncThread = Thread(target=syncprocessor)
        syncThread.start()

        # pingThread = Thread(target=ping_mqtt_server)
        # pingThread.start()

        recordThread = Thread(target=process_record_requests)
        recordThread.start()

        warningThread = Thread(target=process_warning_requests)
        warningThread.start()



        while True:
            cmd = None
            if GPIO.input(LEFT_SIGNAL_PIN) == 1:
                rgb.go_dark()
                cmd = 'left'
            if GPIO.input(RIGHT_SIGNAL_PIN) == 1:
                rgb.go_dark()
                cmd = 'right'


            if cmd is not None:
                publish.single(MQTT_CMD_PATH, cmd, hostname=MQTT_SERVER)
                if cmd == 'left':
                    while GPIO.input(LEFT_SIGNAL_PIN) == 1:
                        pass
                    cmd = 'off'
                if cmd == 'right':
                    while GPIO.input(RIGHT_SIGNAL_PIN) == 1:
                        pass
                    cmd = 'off'
                # if cmd == 'warning':
                # Just tell the rear unit to signal warning,
                # the sync response to the warning turns the ping
                # leds on steady for several seconds
                print(cmd)
                publish.single(MQTT_CMD_PATH, cmd, hostname=MQTT_SERVER)

            time.sleep(0.2)
    finally:
        print('cleanup GPIO')
        GPIO.cleanup()

