import numpy
import time
try:
    import queue as Queue
except ImportError:
    import Queue as Queue


class VeroLedPattern(object):
    def __init__(self, show=None):
        self.basis = [0] * 4 * 12
        self.basis[0 * 4 + 1] = 2
        self.basis[3 * 4 + 1] = 1
        self.basis[3 * 4 + 2] = 1
        self.basis[6 * 4 + 2] = 2
        self.basis[9 * 4 + 3] = 2

        self.pixels = self.basis * 24

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):

        position = int((direction + 15) / 30) % 12
        #wake postion 0
        basis = numpy.roll(self.basis, position * 4)
        #not shift basis

        for i in range(1, 25):
            #loop basis range
            pixels = basis * i
            self.show(pixels)
            time.sleep(0.1)

        pixels =  numpy.roll(pixels, 4)
        self.show(pixels)
        time.sleep(0.1)
        pixels =  numpy.roll(pixels, 4)
        self.show(pixels)
        time.sleep(0.1)
        pixels =  numpy.roll(pixels, 4)
        self.show(pixels)
        time.sleep(0.1)
        pixels =  numpy.roll(pixels, 4)
        self.show(pixels)
        time.sleep(0.1)
                
        # for i in range(2):
        #     new_pixels = numpy.roll(pixels, 4)
        #     self.show(new_pixels * 0.5 + pixels)
        #     pixels = new_pixels
        #     time.sleep(0.1)

        # self.show(pixels)
        # self.pixels = pixels

    def listen(self):
        pixels = self.pixels
        for i in range(1, 25):
            self.show(pixels * i / 24)
            time.sleep(0.01)

    def think(self):
        pixels = self.pixels

        while not self.stop:
            pixels = numpy.roll(pixels, 4)
            self.show(pixels)
            time.sleep(0.2)

        t = 0.1
        for i in range(0, 5):
            pixels = numpy.roll(pixels, 4)
            self.show(pixels * (4 - i) / 4)
            time.sleep(t)
            t /= 2

        self.pixels = pixels

    def speak(self):
        pixels = self.pixels
        step = 1
        brightness = 5
        while not self.stop:
            self.show(pixels * brightness / 24)
            time.sleep(0.02)

            if brightness <= 5:
                step = 1
                time.sleep(0.4)
            elif brightness >= 24:
                step = -1
                time.sleep(0.4)

            brightness += step

    def off(self):
        self.show([0] * 4 * 12)