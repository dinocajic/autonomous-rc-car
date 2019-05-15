#!/user/bin/env python
#
# Dino Cajic
# Autonomous RC Vehicle
# Embedded Systems
# Project due: April 30, 2019
#
# OVERVIEW
# The following file allows the rc vehicle to navigate based on a captured
# video footage that it receives from the PiCamera. A line segment is isolated
# from the shot. As the line moves left or right, instructions are sent to the
# steering servo to make the necessary adjustments.
#
# DETAILED INFORMATION
# The serial port is initialized to allow for communication between the
# Raspberry Pi and the Arduino. The PiCamera is initialized. A loop exists
# that goes through each frame of the video. The width of 90px is
# important for the steering instructions. We'll discuss that in the Arduino code.
# The cropped image is converted into a gray image and a blur is applied to it so
# that line segments can be easily seen.
#
# The findContours() function is called so that the outlines can easily be found.
# This function is built into OpenCV. If a line is detected, then the next step
# is to find the center of the line. This provides the x and y pixel values.
#
# The x value is sent to the Arduino for further processing. The x value is printed
# on the screen and the cropped image is displayed on the screen.
# A small delay is introduced so that the Arduino is not overloaded with information.
#
# OTHER DETAILS
# Written in: JetBrains PyCharm
# Language details: Python 2.7
# Code implemented and modified from the following websites:
#
# https://raspberrypi.stackexchange.com/questions/67840/send-data-from-python-to-arduino-through-serial-port
# http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
#

# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import serial

# Setup the serial port to be used. On the Raspberry Pi, this can vary and usually
# changes between ttyACM0 and tty ACM1
#
# https://raspberrypi.stackexchange.com/questions/67840/send-data-from-python-to-arduino-through-serial-port
usbCom = serial.Serial('/dev/ttyACM0', 9600)
usbCom.close()
usbCom.open()
 
# Initialize the camera
camera = PiCamera()
camera.resolution = (90, 90)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(90, 90))
 
# Camera warm-up delay
time.sleep(0.1)

# Capture the frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        #
        # http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
        image = frame.array

        # Color is stripped and the line is found
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh_img = cv2.threshold(blur,60,255,cv2.THRESH_BINARY)

        contours = cv2.findContours(thresh_img.copy(),1,cv2.CHAIN_APPROX_NONE)[0]

        # If the line is found, the x and y coordinates of the center of the line are calculated
        # and the x coordinate is sent to the Arduino.
        if len(contours) > 0:
                c = contours[0]
                M = cv2.moments(c)

                # An error may arise where m00 is 0. We cannot delete by zero so we'll just skip
                # that calculation.
                if M['m00'] == 0:
                        key = cv2.waitKey(1) & 0xFF
                        rawCapture.truncate(0)
                        if key == ord("q"):
                                break
                        
                        continue

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                cv2.line(gray,(cx,0),(cx,720),(255,0,0),1)
                cv2.line(gray,(0,cy),(1280,cy),(255,0,0),1)

                usbCom.write( str(cx).encode('ascii') )
                print cx                
                
        # The image is displayed on the screen
        cv2.imshow("Frame", image)

        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
                break

        time.sleep(0.1)

cv2.destroyAllWindows()