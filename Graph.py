from msilib.schema import MsiAssembly
from turtle import width

from Calculator import LIMIT_INFINITY


COLOR_RED = (255, 0, 0, 255)
COLOR_GREEN = (0, 255, 0, 255)
COLOR_BLUE = (0, 0, 255, 255)

#returns a color with a reduced alpha value
def reduce_color_alpha(color, multiplier):
    return (color[0], color[1], color[2], int(color[3] * multiplier))

def map_to_new_range(x, oldMin, oldMax, newMin, newMax):
    return (x - oldMin) / (oldMax - oldMin) * (newMax - newMin) + newMin

class Canvas:
    #width and height of the canvas in pixels, xviewport and yviewport are tuples that define min and max values on the canvas
    def __init__(self, width, height, xviewport, yviewport):
        self.width = width
        self.height = height
        self.xviewport = xviewport
        self.yviewport = yviewport

        self.xinc = (xviewport[1] - xviewport[0]) / self.width
        self.yinc = (yviewport[1] - yviewport[0]) / self.height

        self.pixels = [0 for i in range(width * height * 4)]

    def set_x_viewport(self, xviewport):
        self.xviewport = xviewport

    def set_y_viewport(self, yviewport):
        self.yviewport = yviewport

    def zoom(self, factor):
        self.xviewport = (self.xviewport[0] * factor, self.xviewport[1] * factor)
        self.yviewport = (self.yviewport[0] * factor, self.yviewport[1] * factor)
        self.xinc = (self.xviewport[1] - self.xviewport[0]) / self.width
        self.yinc = (self.yviewport[1] - self.yviewport[0]) / self.height

    #moves the viewport by the given pixels
    def move_viewport(self, px, py):
        self.xviewport = (self.xviewport[0] + self.xinc * px, self.xviewport[1] + self.xinc * px)
        self.yviewport = (self.yviewport[0] + self.yinc * py, self.yviewport[1] + self.yinc * py)

    #sets all of the pixels on the canvas to black
    def clear(self):
        self.pixels[:] = [0]*(self.width * self.height * 4)

    def set_pixel(self, x, y, color):
        #inverse y (flip graph to have (0, 0) in the bottom left)
        iy = self.height - y
        
        if x >= self.width or x < 0 or iy >= self.height or iy < 0:
            return

        index = self.width * 4 * iy + x * 4
        for i in range(4):
            self.pixels[index + i] = color[i]

    def set_square(self, x, y, color):
        self.set_pixel(x, y, color)
        self.set_pixel(x + 1, y, reduce_color_alpha(color, 0.5))
        self.set_pixel(x - 1, y, reduce_color_alpha(color, 0.5))
        self.set_pixel(x, y + 1, reduce_color_alpha(color, 0.5))
        self.set_pixel(x, y - 1, reduce_color_alpha(color, 0.5))
        self.set_pixel(x + 1, y + 1, reduce_color_alpha(color, 0.25))
        self.set_pixel(x - 1, y - 1, reduce_color_alpha(color, 0.25))
        self.set_pixel(x + 1, y - 1, reduce_color_alpha(color, 0.25))
        self.set_pixel(x - 1, y + 1, reduce_color_alpha(color, 0.25))        

def graph(canvas, f, color):
    x = canvas.xviewport[0]

    ly = f(x)

    for px in range(canvas.width):
        fx = f(x)

        if abs(ly) == LIMIT_INFINITY:
            ly = fx
            x += canvas.xinc
            continue

        #mapped values
        mly = map_to_new_range(ly, canvas.yviewport[0], canvas.yviewport[1], 0, canvas.height)
        mfx = map_to_new_range(fx, canvas.yviewport[0], canvas.yviewport[1], 0, canvas.height)

        yStart = max(min(mly, mfx), 0)
        yEnd = min(max(mly, mfx), canvas.height) + 1

        for py in range(int(yStart), int(yEnd)):
            canvas.set_pixel(px, py, color)

        ly = fx
        x += canvas.xinc

def graph2(canvas, f, color):
    get_sample = lambda x: f(map_to_new_range(canvas.xviewport[0] + canvas.xinc * x, canvas.yviewport[0], canvas.yviewport[1], 0, canvas.height))
    samples = [get_sample(x) for x in range(canvas.width)]
    
    for i in range(len(samples)):
        start = 0
        end = 0
        if i == 0:
            start = samples[0]
            end = start
        else:
            start = max(min(samples[i - 1], samples[i]), 0)
            end = min(max(samples[i - 1], samples[i]), canvas.height)

        for n in range(int(start), int(end + 1)):
            canvas.set_pixel(i, n, color)