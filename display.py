#!/usr/bin/python2

import threading
import time
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from random import randint, shuffle
import locale

class Display(threading.Thread):
    def __init__(self, dimmer):
    #def __init__(self, weather, dimmer):
        threading.Thread.__init__(self)
        self.setDaemon(True)

	# Options
        options = RGBMatrixOptions()
        options.pwm_lsb_nanoseconds = 400
        options.rows = 32
        options.cols = 64


        #self._weather = weather
        self._dimmer = dimmer

        # Configure LED matrix driver
        #self._matrix = RGBMatrix(32, 2, 1)
        self._matrix = RGBMatrix(options = options)
        self._matrix.pwmBits = 11
        self._matrix.brightness = 20

        # Load fonts
        self._font_large = graphics.Font()
        self._font_large.LoadFont("rpi-rgb-led-matrix/fonts/10x20.bdf")
        self._font_small = graphics.Font()
        self._font_small.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")
        self._font_tiny = graphics.Font()
        self._font_tiny.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")

        # Define colors
        self._white = graphics.Color(255, 255, 255)
        self._red = graphics.Color(255, 32, 32)
        self._blue = graphics.Color(64, 64, 255)
        rgbtupl = self.random_color()
        #rgbtupl = self.colorsX(3)
        self._randcolorH = graphics.Color(int(rgbtupl[0]),int(rgbtupl[1]),int(rgbtupl[2]))
        rgbtupl = self.random_color()
        self._randcolorCollon = graphics.Color(int(rgbtupl[0]),int(rgbtupl[1]),int(rgbtupl[2]))
        rgbtupl = self.random_color()
        self._randcolorM = graphics.Color(int(rgbtupl[0]),int(rgbtupl[1]),int(rgbtupl[2]))
        #self._randcolorH = graphics.Color(randint(100, 255), randint(100, 255), randint(100, 255))
        #self._randcolorCollon = graphics.Color(randint(100, 255), randint(100, 255), randint(100, 255))
        #self._randcolorM = graphics.Color(randint(100, 255), randint(100, 255), randint(100, 255))
	
    def random_color(self):
        num1 = randint(100, 255)
        num2 = randint(10, 255)
        num3 = 250 % num1
        rgbl=[num1,num2,num3]
        shuffle(rgbl)
        print rgbl
        return tuple(rgbl)

    def colorsX(n):
	ret = []
	r = int(random.random() * 256)
	g = int(random.random() * 256)
	b = int(random.random() * 256)
	step = 256 / n
	for i in range(n):
	  r += step
	  g += step
	  b += step
	  r = int(r) % 256
	  g = int(g) % 256
	  b = int(b) % 256
	  ret.append((r,g,b)) 
	  return ret

    def _draw(self, canvas):
	# Remember this is a loop so dont generate colors here 
	# otherwise they will be blinking and changing constantly
	# do it in above function instead
        canvas.Clear()
        locale.setlocale(locale.LC_TIME, "sv_SE.utf8")

        #graphics.DrawText(canvas, self._font_large, 1, 13, self._white, time.strftime("%-2I:%M"))
        graphics.DrawText(canvas, self._font_large, 5, 16, self._randcolorH, time.strftime("%H"))
        graphics.DrawText(canvas, self._font_large, 25, 16, self._randcolorCollon, time.strftime(":"))
        graphics.DrawText(canvas, self._font_large, 35, 16, self._randcolorM, time.strftime("%M"))
        #graphics.DrawText(canvas, self._font_small, 53, 13, self._white, time.strftime("%p"))

	# day of the month
        #graphics.DrawText(canvas, self._font_small, 2, 22, self._white, time.strftime("%a %-d %b"))

	# Remove these lines when temp is implemented
        hi_str = "Vilken dag idag?"
        #hi_str = "%3.0f" % self._weather.high_temp
        graphics.DrawText(canvas, self._font_tiny, 1, 30, self._red, hi_str)
	#graphics.DrawText(canvas, self._font_tiny, 40, 30, self._red, "F")

	'''
	# For future use when temps added

        temp_str = "Tm"
        #temp_str = "%3.0f" % self._weather.cur_temp
        #graphics.DrawText(canvas, self._font_small, 0, 31, self._white, u'A good idea\u00AE')
        graphics.DrawText(canvas, self._font_tiny, 18, 30, self._white, "F")

        hi_str = "Hi"
        #hi_str = "%3.0f" % self._weather.high_temp
        graphics.DrawText(canvas, self._font_small, 22, 30, self._white, hi_str)
        graphics.DrawText(canvas, self._font_tiny, 40, 30, self._red, "F")

        low_str = "Lo"
        #low_str = "%3.0f" % self._weather.low_temp
        graphics.DrawText(canvas, self._font_small, 43, 30, self._white, low_str)
        graphics.DrawText(canvas, self._font_tiny, 61, 30, self._blue, "F")
	'''

    def run(self):
        canvas = self._matrix.CreateFrameCanvas()

        while True:
            self._draw(canvas)
            time.sleep(0.05)
            canvas = self._matrix.SwapOnVSync(canvas)
            self._matrix.brightness = self._dimmer.brightness
