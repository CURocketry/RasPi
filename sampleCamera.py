import picamera
from time import time, sleep, gmtime
import os.path
import os
import RPi.GPIO as GPIO
import threading

GPIO.setwarnings(False) 
Event2 = threading.Event()
Event3 = threading.Event()
successor = False

#
# Returns the current time as a string with the format:
# mm-dd@hh:mm:ss
#
def getCurrentTimeString ():
    tm = gmtime()

    return "%04d-%02d-%02d_%02d-%02d-%02d" % \
        (tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,
        tm.tm_min,tm.tm_sec)

# use P1 header pin numbering convention
GPIO.setmode(GPIO.BOARD)
# Set up the GPIO channels - one input
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
#GPIO.add_event_detect(29, GPIO.RISING)
#print("START")
# Input from pin 11
#input_value = GPIO.input(29)
GPIO.output(15, GPIO.HIGH)
sleep(1)
GPIO.output(15, GPIO.LOW)

#
# Initialize camera and settings
#
#print("Test")
camera = picamera.PiCamera()
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = True
camera.vflip = True
camera.crop = (0.0, 0.0, 1.0, 1.0)


def cameraCapture():
	#FOLDER_PATH = '/var/lib/crtlvc/media'
	#
	# Duration of video capture, in seconds
	#
	myVid = 1800
    GPIO.output(31, GPIO.HIGH)
    GPIO.output(15, GPIO.HIGH)
	#input_value == GPIO.HIGH):
    #
    # Take initial image
    #
    global camera
    camera.capture('/home/pi/Documents/init_image_' + getCurrentTimeString() + '.jpg')
    #
    # Capture video
    #
    camera.start_recording('/home/pi/Documents/video_' + getCurrentTimeString() + '.h264')

    #
    # Wait predetermined amount of time
    #
	#print("Camera Begin!")
	#success = myEvent.wait(myVid)
	mytime=time()
	notDone=True
	failed=False
	global myVar
	while (notDone):
		sleep(0.1)
		newtime = time()
		if (((newtime-myVid)>mytime) or myVar):
			notDone = False
			if (myVar == True):
				failed=True

	GPIO.output(31, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	#print(success)
	#print("Camera End!")
	global successor
	if (failed == False):
		successor = True
	else:
		successor = False
        #
        # Stop video capture
        #
	camera.stop_recording()
        #
        # Take final image
        #
	camera.capture('/home/pi/Documents/video_' + 'fin_image' + getCurrentTimeString() + '.jpg')
	Event2.set()
	return

# stops cameraCapture() if GPIO pin falls from high to low
def detectFallingPin():
	GPIO.wait_for_edge(29, GPIO.FALLING)
	#print("Falling")
	global myVar
	myVar = True
	return

# starts cameraCapture() if GPIO pin rises from low to high
def detectRisingPin():
    GPIO.wait_for_edge(29, GPIO.RISING)
    #print("RISING")
	Event3.set()
	return

while (successor == False):
	Event2.clear()
	Event3.clear()
	myVar = False
	riseThread = threading.Thread(target=detectRisingPin)
	riseThread.start()
	Event3.wait(10000)
	pinThread = threading.Thread(target=detectFallingPin)
	pinThread.setDaemon(True)
	pinThread.start()
	camThread = threading.Thread(target=cameraCapture)
	camThread.run()
	Event2.wait(10000)
GPIO.output(31, GPIO.LOW)
while (1):
	GPIO.output(15, GPIO.LOW)
	sleep(0.5)
	GPIO.output(15, GPIO.HIGH)
	sleep(0.5)

