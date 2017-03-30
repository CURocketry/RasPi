import RPi.GPIO as GPIO
import os
from multiprocessing import Process, Queue
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def detectInitialPress():
    print("init press")
    GPIO.wait_for_edge(18, GPIO.FALLING)
    print("init press finish")

def detectButtonRelease(q):
    print("button release")
    q.put(GPIO.wait_for_edge(18, GPIO.RISING, timeout=5000))
    print("button release finish")
    
inc=0
while (inc<2):
    print("start")
    buttonPress = Process(target=detectInitialPress)
    buttonPress.start()
    buttonPress.join()
    result = Queue()
    buttonRelease = Process(target=detectButtonRelease, args=(result,))
    buttonRelease.start()
    buttonRelease.join()
    print("1")
    if (result.get() is None):
        print("result is none")
        result1 = Queue()
        buttonRelease1 = Process(target=detectButtonRelease, args=(result1,))
        buttonRelease1.start()
        print("2")
        if (result1.get() is not None):
            print("result1 is not none")
            inc=inc+1
        else:
            print("result1 is none")
            inc = 0
            buttonRelease1.terminate()
    else:
        print("result is not none")
        inc = 0
        buttonRelease.terminate()

os.system("shutdown now -h")
