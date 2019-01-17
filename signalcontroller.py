import apa

right_range = range (0, 12)
left_range = range (12, 24)

animation_left_on = [  [0,                     11],
                       [0,1,                10,11],
                       [0,1,2,            9,10,11],
                       [0,1,2,3,        8,9,10,11],
                       [0,1,2,3,4,    7,8,9,10,11],
                       [0,1,2,3,4,5,6,7,8,9,10,11] ]

animation_left_off = [  [  1,2,3,4,5,6,7,8,9,10    ],
                        [    2,3,4,5,6,7,8,9       ],
                        [      3,4,5,6,7,8         ],
                        [        4,5,6,7           ],
                        [          5,6             ],
                        [                          ] ]

animation_right_on = [ [12,                              23],
                       [12,13,                        22,23],
                       [12,13,14,                  21,22,23],
                       [12,13,14,15,            20,21,22,23],
                       [12,13,14,15,16,      19,20,21,22,23],
                       [12,13,14,15,16,17,18,19,20,21,22,23] ]

animation_right_off = [ [  13,14,15,16,17,18,19,20,21,22    ],
                        [    14,15,16,17,18,19,20,21       ],
                        [      15,16,17,18,19,20           ],
                        [         16,17,18,19              ],
                        [            17,18                 ],
                        [                                  ] ]

class SignalController(object):

    def __init__(self):
        self.__led_arrows = apa.Apa(24)
        self.__led_arrows.flush_leds()
        self.__led_arrows.zero_leds()
        self.__led_arrows.write_leds()

    def display_arrow(self, active_range, inactive_range, on_off):
        if on_off == 'on':
            intensity = 31
        else:
            intensity = 0
        for led in active_range:
            self.__led_arrows.led_set(led, intensity, 0, 255, 255)
        for led in inactive_range:
            self.__led_arrows.led_set(led, 0, 0, 0, 0)
        self.__led_arrows.write_leds()

    def animate_arrow(self, animation_on, animation_off, dark_range, on_off):
        if on_off == 'on':
            self.__led_arrows.zero_leds()

            for idx in range(0,6):
                on_leds = animation_on[idx]
                off_leds = animation_off[idx]

                for jdx in range(0, len(on_leds)):
                    self.__led_arrows.led_set(on_leds[jdx], 31, 0, 255, 255)

                for jdx in range(0, len(off_leds)):
                    self.__led_arrows.led_set(off_leds[jdx], 0, 0, 0, 0)

                for led in dark_range:
                    self.__led_arrows.led_set(led, 0, 0,0,0)

                self.__led_arrows.write_leds()

        else:
            for led in right_range:
                self.__led_arrows.led_set(led, 0,0,0,0)
            for led in left_range:
                self.__led_arrows.led_set(led, 0,0,0,0)
            self.__led_arrows.write_leds()

    def arrow(self, direction, on_off):
        if direction == 'left':
            # print('left arrow: ', on_off)
            # self.display_arrow(left_range, right_range, on_off)
            self.animate_arrow(animation_left_on, animation_left_off, left_range, on_off)
        else:
            # print('right arrow: ', on_off)
            # self.display_arrow(right_range, left_range, on_off)
            self.animate_arrow(animation_right_on, animation_right_off, right_range, on_off)



