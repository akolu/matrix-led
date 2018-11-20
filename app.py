import os
import threading
import time
from matrixled import MatrixLed, get_led
from ledrunner import LedRunner

standby = False
standby_thread = None
matrix = MatrixLed()
runner = LedRunner()
matrix.connect()

def get_color(number=1):
    selection = input('Insert color %d (RGBW value separated by space, e.g. 12 0 125 30): ' % number)
    colors = [int(c) for c in selection.split()]
    red = colors[0] if len(colors) > 0 else 0
    green = colors[1] if len(colors) > 1 else 0
    blue = colors[2] if len(colors) > 2 else 0
    white = colors[3] if len(colors) > 3 else 0
    return get_led(red=red, green=green, blue=blue, white=white)

def display_title():
    print('*****************************************')
    print('**** MATRIX ONE Everloop LED blinker ****')
    print('*****************************************\n')
    
def standby_loop(color):
    index = 0
    while standby:
        runner.once(matrix.single, color, index)
        time.sleep(1)
        index = (index + 1) % 35
    

choice = ''
while choice != 'q':
    os.system('clear')
    display_title()
    print('[1] Set LED array mode SOLID (once)\n')
    print('[2] Set LED array mode LOADING (repeat)\n')
    print('[3] Set LED array mode SINGLE (once)\n')
    print('[4] Shutdown LED array\n')
    print('[5] Start STANDBY mode\n')
    print('[q] Quit program\n')

    choice = input('> ')
    
    if standby_thread is not None and standby_thread.isAlive():
        standby = False
        standby_thread.join()
        
    if choice == '1':
        runner.once(matrix.solid, get_color())
    elif choice == '2':
        color = get_color(1)
        base = get_color(2)
        runner.start(matrix.loading_bar, color, base)
    elif choice == '3':
        position = input('Insert LED position: ')
        runner.once(matrix.single, get_color(), int(position))
    elif choice == '4':
        runner.once(matrix.solid)
    elif choice == '5':
        color = get_color()
        standby = True
        standby_thread = threading.Thread(target=standby_loop, args=(color,))
        standby_thread.start()
    elif choice == 'q':
        runner.stop()
        runner.once(matrix.solid)
        matrix.disconnect()
        os.system('clear')
        print('Bye...\n')
