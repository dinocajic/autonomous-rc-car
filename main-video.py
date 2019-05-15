#!/user/bin/env python
#
# Dino Cajic
# Autonomous RC Vehicle
# Embedded Systems
# Project due: April 30, 2019
#
# OVERVIEW
# The following file allows the rc vehicle to navigate based on a video clip.
# The video footage is loaded and a segment is isolated from the shot. As the
# line moves left or right, instructions are sent to the steering servo to
# make the necessary adjustments.
#
# DETAILED INFORMATION
# The serial port is initialized to allow for communication between the
# Raspberry Pi and the Arduino. The video footage is loaded. A loop exists
# that goes through each frame of the video. The frame is then cropped to 50px
# high and 90px wide. The width of 90px is important for the steering instructions.
# We'll discuss that shortly. The cropped image is converted into a gray image and
# a blur is applied to it so that line segments can be easily seen.
#
# The findContours() function is called so that the outlines can easily be found.
# This function is built into OpenCV. If a line is detected, then the next step
# is to find the center of the line. This provides the x and y pixel values.
#
# The x value is sent to the Arduino for further processing. The x value is printed
# on the screen and the large image and cropped images are displayed on the screen.
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
import cv2
import numpy as np
import serial
import time

# Setup the serial port to be used. On the Raspberry Pi, this can vary and usually
# changes between ttyACM0 and tty ACM1
#
# https://raspberrypi.stackexchange.com/questions/67840/send-data-from-python-to-arduino-through-serial-port
usbCom = serial.Serial('/dev/ttyACM0', 9600)
usbCom.close()
usbCom.open()

# The video file is captured
cap = cv2.VideoCapture("road-clip.mp4")
cap.set(3,500)
cap.set(4,350)

while True:
    ret, frame = cap.read()

    # The frame is cropped to 50x90px in a specific location that starts at 300px from the top and 400px from the left.
    # This is specific to this video clip
    #
    # http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
    crop_img = frame[300:350,400:490]

    # Color is stripped and the line is found
    gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, thresh_img = cv2.threshold(blur,60,255,cv2.THRESH_BINARY)

    contours = cv2.findContours(thresh_img.copy(),1,cv2.CHAIN_APPROX_NONE)[0]

    # If the line is found, the x and y coordinates of the center of the line are calculated
    # and the x coordinate is sent to the Arduino. The large and cropped images are displayed.
    if len(contours) > 0:
        c = contours[0]
        
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

        usbCom.write( str(cx).encode('ascii') )

        print cx

        cv2.imshow('frame',frame)
        cv2.imshow('frame',crop_img)

        time.sleep(.300)
    else:
        print "I don't see the line"
    
    key = cv2.waitKey(25)

    if key == 27:
        break

video.release()
cv2.destroyAllWindows()