# All button leds are GPIO BCM pins
LEFT_LED = 20     # blue wire
PING_OUT_LED = 26      # green wire
BRAKE_LED = 19     # 13 yellow wire
PING_ACK_LED = 5    # orange wire
RIGHT_LED = 6  # 5 was 18       # red wire

# List of button leds to make it easier to change them all at once
button_leds = [LEFT_LED, PING_OUT_LED, BRAKE_LED, PING_ACK_LED, RIGHT_LED]

LEFT_PWM_CHANNEL = LEFT_LED
RIGHT_PWM_CHANNEL = RIGHT_LED
BRAKE_PWM_CHANNEL = BRAKE_LED
pwm_channels = [LEFT_PWM_CHANNEL, RIGHT_PWM_CHANNEL, BRAKE_PWM_CHANNEL]

# Button pins are GPIO BCM pins that are used where pressed is GPIO.HIGH
# so they will be set up using pull-down GPIO calls
WHITE_BUTTON_PIN = 14    # red wire
RIGHT_SIGNAL_PIN = 27     # brown wire
LEFT_SIGNAL_PIN = 17    # black wire
BRAKE_SIGNAL_PIN = 24   # white wire
WARNING_PIN = 25       # gray wire

# List of button pins to make it easier to change them all at once
button_pins = [WHITE_BUTTON_PIN, RIGHT_SIGNAL_PIN, LEFT_SIGNAL_PIN, BRAKE_SIGNAL_PIN, WARNING_PIN]

