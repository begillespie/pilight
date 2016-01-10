import pigpio, re, time

class RGB:
    '''Uses software PWM to control a RGB LED on Raspberry Pi. Declare the
    class with the RGB pin numbers. Call setColor(color) to use. Accepts color
    values in three ways:
       1) RGB list:                    [255,255,255]
       2) W3C CSS color keyword:       'white'
       3) Hex color code as a string:  '#FFFFFF'
    Call stop() to stop PWM and clean up the GPIO before exiting.
    '''

    PWMfrequency = 100 #Hz
    pi = pigpio.pi() # Initialize gpio library

    # Precompile the regexp to validate color input
    hexMatchPattern = re.compile(r"^#[0-9a-fA-F]{6}")

    def __init__(self, red, green, blue):
        #Pin definitions
        self.pins = {
                'red':red,
                'green':green,
                'blue':blue
                }

        #Set up pins and initialize to low
        for pin in self.pins:
            self.pi.set_mode(self.pins[pin], pigpio.OUTPUT)
            self.pi.set_PWM_frequency(self.pins[pin], self.PWMfrequency)
            self.pi.set_PWM_dutycycle(self.pins[pin], 0)

        self.state = 'ready'

    def setColor(self, color):
        '''Accepts a color as either a RGB list: [255,255,255], hex color code
        '#09afAF' or CSS color keyword: 'blue' and shows it.'''
        try:
            if isinstance(color, list):
                msg = self.setRGB(int(color[0]), int(color[1]), int(color[2]))
            elif color.lower() in self.cssColors:
                rgbV = self.hextoRGB(self.cssColors[color.lower()])
                if rgbV:
                    msg = self.setRGB(rgbV['r'], rgbV['g'], rgbV['b'])
            elif color[0] == '#':
                rgbV = self.hextoRGB(color)
                if rgbV:
                    msg = self.setRGB(rgbV['r'], rgbV['g'], rgbV['b'])
            else:
                print('invalid input')
                msg = 'invalid input'
            return msg

        except (TypeError, ValueError) as e:
            print('Invalid input', e)
            return 'input error'

    def limitValue(self, value, low, high):
        '''Constrains value between low and high'''
        if value < low:
            value = low
        if value > high:
            value = high
        return value

    def mapValue(self, value, fromLow, fromHigh, toLow, toHigh):
        '''It's the Arduino map function. Maps a value from
        one scale to the other'''
        return (value - fromLow) * (toHigh - toLow) // (fromHigh - fromLow) + toLow

    def setRGB(self, rV, gV, bV):
        '''Takes RGB values as integers from 0 - 255'''
        try:
            self.pi.set_PWM_dutycycle(self.pins['red'], self.gamma[self.limitValue(rV, 0, 255)])
            self.pi.set_PWM_dutycycle(self.pins['green'], self.gamma[self.limitValue(gV, 0, 255)])
            self.pi.set_PWM_dutycycle(self.pins['blue'], self.gamma[self.limitValue(bV, 0, 255)])
            return 'Set RGB ({}, {}, {})'.format(rV, gV, bV)

        except TypeError:
            print('RGB values must be integers')
            return False

    def hextoRGB(self, hexValue):
        '''Takes a 6-character hex string such as #ffffff
        and converts to rgb {'r':255,'g':255,'b':255]
        hexMatchPattern was precompiled in the setup'''

        try:
            if len(hexValue) == 7 and re.match(self.hexMatchPattern, hexValue):
                r = int(hexValue[-6:-4],16)
                g = int(hexValue[-4:-2],16)
                b = int(hexValue[-2:],16)
                return {'r':r, 'g':g, 'b':b}
            else:
                print('Invalid color name. Must be #09afAF')
                return False
        except TypeError:
            print('Color code must be a string')
            return False

    def stop(self):
        for pin in self.pins:
            self.pi.set_PWM_dutycycle(self.pins[pin], 0)

        self.pi.stop()
        return 'stopped'

    # Hex definitions for the 147 W3C CSS colors
    cssColors={
        'aliceblue':'#f0f8ff',
        'antiquewhite':'#faebd7',
        'aqua':'#00ffff',
        'aquamarine':'#7fffd4',
        'azure':'#f0ffff',
        'beige':'#f5f5dc',
        'bisque':'#ffe4c4',
        'black':'#000000',
        'blanchedalmond':'#ffe4c4',
        'blue':'#0000ff',
        'blueviolet':'#8a2be2',
        'brown':'#a52a2a',
        'burlywood':'#deb887',
        'cadetblue':'#5f9ea0',
        'chartreuse':'#7fff00',
        'chocolate':'#d2691e',
        'coral':'#ff7f50',
        'cornflowerblue':'#6495ed',
        'cornsilk':'#fff8dc',
        'crimson':'#dc143c',
        'darkblue':'#00008b',
        'darkcyan':'#008b8b',
        'darkgoldenrod':'#b8860b',
        'darkgray':'#a9a9a9',
        'darkgreen':'#006400',
        'darkgrey':'#a9a9a9',
        'darkkhaki':'#bdb76b',
        'darkmagenta':'#8b008b',
        'darkolivegreen':'#556b2f',
        'darkorange':'#ff8c00',
        'darkorchid':'#9932cc',
        'darkred':'#8b0000',
        'darksalmon':'#e9967a',
        'darkseagreen':'#8fbc8f',
        'darkslateblue':'#483d8b',
        'darkslategray':'#2f4f4f',
        'darkslategrey':'#2f4f4f',
        'darkturquoise':'#00ced1',
        'darkviolet':'#9400d3',
        'deeppink':'#ff1493',
        'deepskyblue':'#00bfff',
        'dimgray':'#696969',
        'dimgrey':'#696969',
        'dodgerblue':'#1e90ff',
        'firebrick':'#b22222',
        'floralwhite':'#fffaf0',
        'forestgreen':'#228b22',
        'fuchsia':'#ff00ff',
        'gainsboro':'#dcdcdc',
        'ghostwhite':'#f8f8ff',
        'gold':'#ffd700',
        'goldenrod':'#daa520',
        'gray':'#808080',
        'green':'#008000',
        'greenyellow':'#adff2f',
        'grey':'#808080',
        'honeydew':'#f0fff0',
        'hotpink':'#ff69b4',
        'indianred':'#cd5c5c',
        'indigo':'#4b0082',
        'ivory':'#fffff0',
        'khaki':'#f0e68c',
        'lavender':'#e6e6fa',
        'lavenderblush':'#fff0f5',
        'lawngreen':'#7cfc00',
        'lemonchiffon':'#fffacd',
        'lightblue':'#add8e6',
        'lightcoral':'#f08080',
        'lightcyan':'#e0ffff',
        'lightgoldenrodyellow':'#fafad2',
        'lightgray':'#d3d3d3',
        'lightgreen':'#90ee90',
        'lightgrey':'#d3d3d3',
        'lightpink':'#ffb6c1',
        'lightsalmon':'#ffa07a',
        'lightseagreen':'#20b2aa',
        'lightskyblue':'#87cefa',
        'lightslategray':'#778899',
        'lightslategrey':'#778899',
        'lightsteelblue':'#b0c4de',
        'lightyellow':'#ffffe0',
        'lime':'#00ff00',
        'limegreen':'#32cd32',
        'linen':'#faf0e6',
        'maroon':'#800000',
        'mediumaquamarine':'#66cdaa',
        'mediumblue':'#0000cd',
        'mediumorchid':'#ba55d3',
        'mediumpurple':'#9370db',
        'mediumseagreen':'#3cb371',
        'mediumslateblue':'#7b68ee',
        'mediumspringgreen':'#00fa9a',
        'mediumturquoise':'#48d1cc',
        'mediumvioletred':'#c71585',
        'midnightblue':'#191970',
        'mintcream':'#f5fffa',
        'mistyrose':'#ffe4e1',
        'moccasin':'#ffe4b5',
        'navajowhite':'#ffdead',
        'navy':'#000080',
        'oldlace':'#fdf5e6',
        'olive':'#808000',
        'olivedrab':'#6b8e23',
        'orange':'#ffa500',
        'orangered':'#ff4500',
        'orchid':'#da70d6',
        'palegoldenrod':'#eee8aa',
        'palegreen':'#98fb98',
        'paleturquoise':'#afeeee',
        'palevioletred':'#db7093',
        'papayawhip':'#ffefd5',
        'peachpuff':'#ffdab9',
        'peru':'#cd853f',
        'pink':'#ffc0cb',
        'plum':'#dda0dd',
        'powderblue':'#b0e0e6',
        'purple':'#800080',
        'rebeccapurple':'#663399',
        'red':'#ff0000',
        'rosybrown':'#bc8f8f',
        'royalblue':'#4169e1',
        'saddlebrown':'#8b4513',
        'salmon':'#fa8072',
        'sandybrown':'#f4a460',
        'seagreen':'#2e8b57',
        'seashell':'#fff5ee',
        'sienna':'#a0522d',
        'silver':'#c0c0c0',
        'skyblue':'#87ceeb',
        'slateblue':'#6a5acd',
        'slategray':'#708090',
        'slategrey':'#708090',
        'snow':'#fffafa',
        'springgreen':'#00ff7f',
        'steelblue':'#4682b4',
        'tan':'#d2b48c',
        'teal':'#008080',
        'thistle':'#d8bfd8',
        'tomato':'#ff6347',
        'turquoise':'#40e0d0',
        'violet':'#ee82ee',
        'wheat':'#f5deb3',
        'white':'#ffffff',
        'whitesmoke':'#f5f5f5',
        'yellow':'#ffff00',
        'yellowgreen':'#9acd32'
    }

    '''Used to apply gamma correction to LED input values so colors
    appear correct. Call gamma[n] to get the gamma-corrected output.
    See https://learn.adafruit.com/led-tricks-gamma-correction/the-quick-fix'''
    gamma = \
    [0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
    10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
    17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
    25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
    37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
    51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
    69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
    90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
    115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
    144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
    177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
    215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255]
