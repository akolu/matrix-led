import os
import time
import zmq
import sys
import threading
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2

# MATRIX Everloop LED array port
PORT = 20021
LED_COUNT = 35

def get_led(**args):
    ledValue = io_pb2.LedValue()
    ledValue.red = args.get('red', 0)
    ledValue.green = args.get('green', 0)
    ledValue.blue = args.get('blue', 0)
    ledValue.white = args.get('white', 0)
    return ledValue

class MatrixLed:

    _dark = get_led()

    def __init__(self, matrix_ip='127.0.0.1'):
        context = zmq.Context()
        self.address = 'tcp://{0}:{1}'.format(matrix_ip, PORT)
        self.socket = context.socket(zmq.PUSH)

    def __show(self, leds):
        config = driver_pb2.DriverConfig()
        config.image.led.extend(leds)
        self.socket.send(config.SerializeToString())

    def connect(self):
        self.socket.connect(self.address)

    def disconnect(self):
        self.socket.disconnect(self.address)

    def solid(self, color=_dark):
        """ Light all leds in single colour """
        leds = []
        for led in range(LED_COUNT):
            leds.append(color)
        self.__show(leds)

    def loading_bar(self, color, base=_dark, delay=0.01):
        """ Light one led at a time until all leds are lit """
        if color == base:
            self.disconnect()
            sys.exit('Color and base cannot be identical')
        count = 0
        while count < LED_COUNT:
            count += 1
            lit_leds = [color for led in range(count)]
            base_leds = [base for led in range(LED_COUNT - count)]
            leds = lit_leds + base_leds
            self.__show(leds)
            time.sleep(0.01)
            
    def single(self, color, position=0):
        """ Light a single led """
        if position < 0 or position >= LED_COUNT:
            self.disconnect()
            sys.exit('Position must be a number between 0 and 34')
        leds = [self._dark for led in range(LED_COUNT)]
        leds[position] = color
        self.__show(leds)
        
        
        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
